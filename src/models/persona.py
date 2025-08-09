from pydantic import BaseModel, Field
from typing import Optional

class Persona(BaseModel):
    label: str = Field(..., description="Readable persona name")
    description: str = Field(..., description="One–two sentences of context")
    region: Optional[str] = None
    sector: Optional[str] = None
    size: Optional[str] = None
    income_band: Optional[str] = None

DEFAULT_PERSONAS = {
    "High school student": Persona(
        label="High school student",
        description="16-year-old student; cares about school, family budget, local community.",
        income_band="low-to-middle"
    ),
    "Small business owner": Persona(
        label="Small business owner",
        description="Owner of a 12-person retail/service business; cares about compliance, taxes, hiring.",
        region="urban/suburban", sector="retail/services", size="SMB", income_band="middle"
    ),
    "Economist": Persona(
        label="Economist",
        description="Analyst focused on mechanisms, incidence, and second-order effects."
    ),
}