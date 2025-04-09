from fastapi import FastAPI, HTTPException
import uvicorn
from typing import List

# Importar modelos y scraper
from models.job_models import JobListing, ScrapingRequest
from scrapers.computrabajo_scraper import scrap_computrabajo_co

app = FastAPI(
    title="API de Scraping de Empleos",
    description="API para extraer ofertas de empleo de diversas plataformas.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Scraping de Empleos"}

# --- Endpoint para Computrabajo ---
@app.post("/scrape/computrabajo",
          response_model=List[JobListing],
          tags=["Scraping"],
          summary="Realiza scraping en Computrabajo Colombia",
          description="Inicia el proceso de scraping en co.computrabajo.com con las palabras clave y ubicación dadas.")
def run_computrabajo_scraper(request: ScrapingRequest):
    """Endpoint para ejecutar el scraper de Computrabajo."""
    try:
        jobs = scrap_computrabajo_co(keyword=request.keyword, location=request.location)
        if not jobs:
            # Devolver 204 No Content si no se encontraron trabajos pero el scraping fue exitoso
            # O podríamos devolver 404 Not Found, depende de la semántica preferida.
            # Optaremos por una lista vacía y código 200 por ahora.
            return []
        return jobs
    except Exception as e:
        # Captura general de errores durante el scraping
        # Idealmente, se manejarían excepciones más específicas
        raise HTTPException(status_code=500, detail=f"Error durante el scraping de Computrabajo: {str(e)}")

# Aquí agregaremos los endpoints para cada scraper

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
