from pydantic import BaseModel, HttpUrl
from typing import Optional

class JobListing(BaseModel):
    """Modelo Pydantic para representar una oferta de empleo."""
    title: str
    company: Optional[str] = "N/A"
    location: Optional[str] = "N/A"
    link: HttpUrl
    source: str # De dónde se obtuvo (Computrabajo, ElEmpleo, etc.)
    # Podríamos añadir más campos aquí si los extraemos
    # description: Optional[str] = None
    # salary: Optional[str] = None

class ScrapingRequest(BaseModel):
    """Modelo para los parámetros de la petición de scraping."""
    keyword: str = "desarrollador"
    location: str = "bogota"
