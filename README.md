# Scraper de Precios de Mantenimiento - Toyota Argentina

Este proyecto es un script automatizado que extrae información de precios de mantenimiento de la página oficial de Toyota Argentina y genera un archivo CSV con los datos recopilados.

## Requisitos
- Python 3.8 o superior
- Google Chrome y una versión compatible de [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads/version-selection)

## Instalación
1. Clona el repositorio:
   ```cmd
   git clone https://github.com/FidelSch/Scraper-Toyota
   cd Scraper-Toyota
   ```
2. Instala las dependencias:
   ```cmd
   pip install -r requirements.txt
   ```
3. Descarga ChromeDriver y asegúrate de que esté en tu PATH.

## Uso
Ejecuta el script con:
```cmd
python scraper.py
```
Esto generará un archivo `precios_toyota.csv` con los datos extraídos.
