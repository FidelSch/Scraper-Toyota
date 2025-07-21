from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_car_prices_to_csv(url, output_file):
    service = Service("C:\\Program Files\\chrome-win64\\chromedriver.exe") ## Cambia la ruta al chromedriver según tu instalación
    driver = webdriver.Chrome(service=service)

    data = []  # Lista para almacenar los datos

    try:
        driver.get(url)

        # Encontrar el menú desplegable y seleccionar un modelo
        select_modelos = Select(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "carModel"))
        ))

        # Iterar sobre las opciones y simular la selección
        for modelo in select_modelos.options:
            if not modelo.is_enabled():
                continue

            model_name = modelo.text.strip()

            print(f"Procesando modelo: {model_name}")
            select_modelos.select_by_visible_text(model_name)

            select_miles = Select(WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "miles"))
            ))

            # Iterar sobre las opciones y simular la selección
            for kilometraje in select_miles.options:
                if not kilometraje.is_enabled():
                    continue

                miles_value = kilometraje.text.strip()
                if not miles_value:
                    continue

                select_miles.select_by_visible_text(miles_value)

                try:
                    # Verificar si los precios están disponibles
                    precios = driver.find_elements(By.CLASS_NAME, "styles_item__value__k_ptW")
                    if len(precios) < 2:
                        print(f"No se encontraron precios para {model_name} con {miles_value} millas.")
                        continue

                    contado = precios[0].text.strip()[:-6]  # Eliminar los últimos 6 caracteres
                    cuotas = precios[1].text.strip()[:-6]  # Eliminar los últimos 6 caracteres

                    # Extraer servicios
                    servicios = []
                    categorias_servicios = driver.find_elements(By.CLASS_NAME, "styles_faq-list__item___CYuN")
                    for categoria in categorias_servicios:
                        try:
                            header = categoria.find_element(By.CLASS_NAME, "styles_toggle-button__label__0GXLV").text.strip()
                            lista = categoria.find_element(By.CLASS_NAME, "styles_faq-list__item-text__XJZec").get_attribute("textContent").strip().split("\n")
                            servicios.append({header: lista})
                        except Exception as e:
                            print(f"Error al procesar servicios para {model_name} con {miles_value}: {e}")

                    # Agregar los datos a la lista
                    data.append({
                        "Modelo": model_name,
                        "Millas": miles_value,
                        "Contado": contado,
                        "3 Cuotas": cuotas,
                        "Servicios": servicios,
                    })
                    print(f"Datos extraídos para {model_name} con {miles_value} millas: Contado: {contado}, 3 Cuotas: {cuotas}, Servicios: {servicios}")

                except Exception as e:
                    print(f"Error al procesar datos para {model_name} con {miles_value}: {e}")

        # Guardar los datos en un archivo CSV
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Datos guardados en {output_file}")

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.toyota.com.ar/mi-toyota/servicios/plan-de-mantenimiento"
    output_file = "precios_toyota.csv"
    scrape_car_prices_to_csv(url, output_file)
