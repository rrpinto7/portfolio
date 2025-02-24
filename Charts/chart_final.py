
# passo 1: importar a tabela de excel para ambiente python
import folium
import pandas as pd


# Carregar dados do Excel 
file_path = r"C:\Users\rpinto\Documents\Sources\source_W.River.xlsx"

# Ler os dados da folha Excel "detail"
data = pd.read_excel(file_path, sheet_name="detail", engine="openpyxl")  # 

# Verificar se os dados foram carregados corretamente
#print(df.head())  # Mostra as primeiras linhas para conferência

# Criar a nova coluna com o valor tratado de '% WEIGHT'
data['N_WEIGHT'] = (data['% WEIGHT'].astype(float) * 100).round(2)

#print(df.head())

## Criar os mapas
## Mapa 1 - Círculos proporcionais ao volume

# Criar mapa base centrado na África do Sul
m = folium.Map(location=[-28, 24], zoom_start=6)

# Adicionar círculos ao mapa
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['DES_LAT'], row['DES_LON']],
        radius=row['M3'] / 1000,  # Ajustar tamanho proporcional
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        #popup=f"{row['City']}: {row['Volume']} M3"
        popup=f"<b>Destino:</b> {row['DESTINY']}<br><b>Volume:</b> {row['M3']} m³<br><b>Peso Relativo:</b> {row['N_WEIGHT']} %<br><b>Coordenadas:</b> {row['DES_LAT']}, {row['DES_LON']}"
    ).add_to(m)

# Guardar o mapa num ficheiro HTML
m.save("mapa_círculos.html")

print("Mapa gerado: abre o ficheiro 'mapa.html' no teu browser.")

## Segundo mapa

# Criar o mapa base
m_network = folium.Map(location=[-28, 24], zoom_start=6)

# Adicionar linhas (arcos) entre a origem e os destinos
for index, row in data.iterrows():
    folium.PolyLine(
        locations=[
            [row['ORI_LAT'], row['ORI_LON']],  # Origem
            [row['DES_LAT'], row['DES_LON']]  # Destino
        ],
        weight=row['M3'] / 1000,  # Espessura da linha proporcional ao volume
        color='green',
        opacity=0.6
    ).add_to(m_network)

    # Adicionar pop-up com informações detalhadas
    folium.Marker(
        location=[row['DES_LAT'], row['DES_LON']],
        popup=f"<b>Destino:</b> {row['DESTINY']}<br><b>Volume:</b> {row['M3']} m³<br><b>Peso Relativo:</b> {row['N_WEIGHT']} %<br><b>Coordenadas:</b> {row['DES_LAT']}, {row['DES_LON']}"
    ).add_to(m_network)

# Salvar o mapa de network
m_network.save("mapa_network.html")

print("Mapa de network gerado: abre o ficheiro 'mapa_network.html' no teu browser.")

from folium.plugins import HeatMap

# Preparar os dados para o heatmap
heat_data = [[row['DES_LAT'], row['DES_LON'], row['M3']] for index, row in data.iterrows()]

# Criar o heatmap
m_heatmap = folium.Map(location=[-28, 24], zoom_start=6)

HeatMap(
    heat_data, 
    radius=25,         # Ajusta o tamanho da mancha - Default 25 - Valores maiores fazem as manchas mais largas
    blur=15,           # Ajusta o desfoque - D 15 - Valores maiores fazem a transição entre manchas mais suaves.
    min_opacity=0.5,   # Ajusta a opacidade mínima - 0.5 
    max_zoom=18       # Ajustar o zoom - D 18 - Controla o nível de zoom em que o heatmap será visível. Pode ajudar a controlar o detalhamento no mapa.
).add_to(m_heatmap)
# Adicionar uma legenda explicativa
legend_html = """
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 150px; height: 100px;
                 border:2px solid grey; background-color:white; z-index:9999;
                 font-size:14px; padding: 10px;">
     <b>Legenda</b><br>
     <i style="background:blue; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Menor Volume<br>
     <i style="background:red; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></i> Maior Volume
     </div>
     """
m_heatmap.get_root().html.add_child(folium.Element(legend_html))

# Salvar o heatmap
m_heatmap.save("mapa_calor.html")

print("Heatmap gerado: abre o ficheiro 'heatmap.html' no teu browser.")