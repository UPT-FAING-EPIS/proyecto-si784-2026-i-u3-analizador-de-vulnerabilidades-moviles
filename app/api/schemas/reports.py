from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    user_id: str = Field(..., min_length=1)
    dispositivo: str = Field(..., min_length=1)
    vulnerabilidad: str = Field(..., min_length=1)
    nivel: str = Field(..., min_length=1)
    descripcion: str | None = None


class ReportResponse(BaseModel):
    id: str | int | None = None
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
