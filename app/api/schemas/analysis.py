from pydantic import BaseModel


class VulnerabilidadItem(BaseModel):
    id: str
    tipo: str
    titulo: str
    severidad: str
    descripcion: str | None = None
    evidencia: str | None = None
    recomendacion: str | None = None
    archivo_origen: str | None = None
    cwe: str | None = None
    owasp: str | None = None


class ResumenAnalisis(BaseModel):
    total_vulnerabilidades: int
    severidad_maxima: str
    conteo_por_severidad: dict[str, int]


class MetricasCalidad(BaseModel):
    proyecto: str | None = None
    lineas_codigo: int | None = None
    complejidad: int | None = None
    code_smells: int | None = None


class AnalisisResponse(BaseModel):
    estado: str
    tipo_analisis: str
    objetivo: str | None = None
    tamano_bytes: int | None = None
    resumen: ResumenAnalisis
    vulnerabilidades: list[VulnerabilidadItem]
    metricas_calidad: MetricasCalidad | None = None
    fecha_analisis: str
