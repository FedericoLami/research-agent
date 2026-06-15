from typing import TypedDict, List

class EstadoInvestigacion(TypedDict):
    tema: str
    subtemas: List[str]
    resultados: List[str]
    analisis: str
    reporte: str