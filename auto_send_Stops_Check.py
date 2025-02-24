import os
import win32com.client
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from datetime import datetime # para trazer o timestamp

# Configurar URL do relatório
URL = "https://otmgtm-a591355.otmgtm.uk-london-1.ocs.oraclecloud.com"

# Caminho para o EdgeDriver
edge_driver_path = r'C:\edge_driver\msedgedriver.exe'  # Atualiza com o caminho correto

# Configurar WebDriver para o Edge
service = Service(edge_driver_path)
options = webdriver.EdgeOptions()
# options.add_argument("--headless")  # Para rodar sem abrir janela (opcional)
driver = webdriver.Edge(service=service, options=options)

# Abrir a página de login
driver.get(URL)
time.sleep(5)  # Esperar o carregamento

# Inserir credenciais
username = driver.find_element(By.ID, "idcs-signin-basic-signin-form-username")  # Confirma se o nome do campo está correto
password = driver.find_element(By.ID, "idcs-signin-basic-signin-form-password|input")  # Confirma se o nome do campo está correto

username.send_keys("ruben.pinto@sonaearauco.com")
password.send_keys("Rubs_otm_2025")
password.send_keys(Keys.RETURN)  # Pressionar Enter para fazer login


# Esperar login completar
time.sleep(3)

# Ir para o relatório específico
driver.get("https://otmgtm-a591355.otmgtm.uk-london-1.ocs.oraclecloud.com/xmlpserver/Custom/Shipment_Report/OTM%20vs%20SAP%20Additional%20Stops.xdo")
time.sleep(5)  # Esperar carregar

# Obter a data e hora atual no formato desejado (dd-mm-aaaa_hh-mm)
timestamp = datetime.now().strftime("%d-%m-%Y_%H.%M")

# Guardar screenshot
screenshot_path = os.path.join(os.getcwd(), f"otm_print_{timestamp}.png")
driver.save_screenshot(screenshot_path)

# Fechar navegador
driver.quit()


# Enviar Email pelo Outlook
def send_email():
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    
    mail.To = "ruben.pinto@sonaearauco.com"
    mail.Subject = "[OPS] - OTM vs SAP Additional Stops - Atualização Semanal"

    # Anexar screenshot
    mail.Attachments.Add(screenshot_path)
    attachment = mail.Attachments.Add(screenshot_path)

    # Definir o Content-ID (CID) para referenciar a imagem no HTML
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "screenshot")

    # Atualizar o HTMLBody para incluir a imagem embutida
    mail.HTMLBody = f"""
        <html>
            <body>
                <p>Olá,</p>
                <p>Segue abaixo e em anexo o relatório de discrepâncias entre OTM e SAP para validação.</p>
                <br>
                <img src="cid:screenshot" style="max-width:600px; height:auto; margin-top:10px;">
                <br>
                <p>Obrigado!</p>
            </body>
        </html>
        """
        
    #Enviar email
    mail.Send()
    print("Email enviado com sucesso!")

# Executar envio de email
send_email()
