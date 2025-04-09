import requests
from bs4 import BeautifulSoup
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
BASE_URL_CO = "https://co.computrabajo.com"

def scrap_computrabajo_co(keyword: str = "desarrollador", location: str = "bogota") -> list[dict]:
    """Realiza scraping de ofertas de empleo en Computrabajo Colombia."""
    search_url = f"{BASE_URL_CO}/trabajo-de-{keyword}-en-{location}"
    logging.info(f"Iniciando scraping para: {search_url}")

    try:
        response = requests.get(search_url, headers={"User-Agent": USER_AGENT}, timeout=15)
        response.raise_for_status()  # Lanza excepción para códigos de error HTTP (4xx o 5xx)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al realizar la petición a {search_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")  # Usar lxml como parser
    jobs = []
    ofertas = soup.select(".box_offer")  # Selector actualizado

    if not ofertas:
        logging.warning(f"No se encontraron ofertas para '{keyword}' en '{location}' en {search_url}")
        return []

    logging.info(f"Se encontraron {len(ofertas)} ofertas preliminares.")

    for oferta in ofertas:
        try:
            # Selectores actualizados con los valores precisos
            title_element = oferta.select_one("h2.fs18 .js-o-link")
            link_element = oferta.select_one("h2.fs18 .js-o-link")
            company_element = oferta.select_one("p.dFlex a.fc_base")
            location_element = oferta.select_one("p.fs16 span.mr10")
            work_type_element = oferta.select_one("div.fs13 span.dIB")

            title = title_element.text.strip() if title_element else "N/A"
            
            # Construir link absoluto correctamente
            link_suffix = link_element.get("href", "") if link_element else ""
            link = BASE_URL_CO + link_suffix if link_suffix and link_suffix.startswith('/') else link_suffix

            company = company_element.text.strip() if company_element else "N/A"
            location_text = location_element.text.strip() if location_element else "N/A"
            
            # Añadir tipo de trabajo si está disponible
            work_type = work_type_element.text.strip() if work_type_element else ""
            
            # Si hay información sobre tipo de trabajo, añadirla a la ubicación
            if work_type:
                location_text = f"{location_text} - {work_type}"

            if link and title != "N/A":  # Solo añadir si tenemos título y link
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link,
                    "source": "Computrabajo"
                })
            else:
                logging.warning("Oferta omitida por falta de título o link.")

        except AttributeError as e:
            logging.warning(f"Error al parsear una oferta: {e}")
            continue  # Saltar a la siguiente oferta si hay error en esta

    logging.info(f"Scraping finalizado para {search_url}. Total de empleos extraídos: {len(jobs)}")
    return jobs

# Ejemplo de uso (para pruebas)
if __name__ == '__main__':
    trabajos = scrap_computrabajo_co(keyword="python", location="medellin")
    if trabajos:
        print(f"Se encontraron {len(trabajos)} trabajos:")
        for job in trabajos:
            print(job)
    else:
        print("No se encontraron trabajos.")