


import folium
import pandas as pd

# Criar dataframe
data = pd.DataFrame({
    'City': ['Johannesburg', 'Pretoria', 'Durban'],  # Adicione todas as cidades
    'Latitude': [-26.2041, -25.7461, -29.8587],  # Coordenadas das cidades
    'Longitude': [28.0473, 28.1881, 31.0218],
    'Volume': [85299, 43656, 36118]
})

# Criar mapa centrado na África do Sul
m = folium.Map(location=[-28, 24], zoom_start=5)

# Adicionar círculos ao mapa
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Volume'] / 10000,  # Ajustar tamanho proporcional
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"{row['City']}: {row['Volume']} M3"
    ).add_to(m)

# Guardar o mapa num ficheiro HTML
m.save("mapa.html")

print("Mapa gerado: abre o ficheiro 'mapa.html' no teu browser.")