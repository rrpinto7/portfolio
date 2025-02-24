import win32com.client

# Criar email
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)

# Configurar o email
mail.To = "ruben.pinto@sonaearauco.com"
mail.Subject = "Teste de Remetente"
mail.Body = "Este é um e-mail de teste para validar as permissões de remetente."
# Definir o "From" como outro endereço
mail.Sender = "noreply@transportsSWE.com"  # Alterar o endereço do remetente
mail.Send()
