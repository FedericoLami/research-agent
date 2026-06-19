# Research Agent — Sistema Multi-Agente de Investigación Automática

Sistema de investigación automática construido con **LangGraph**, **Claude AI** y **Tavily** que genera reportes estructurados sobre cualquier tema. Un pipeline de cuatro agentes especializados planifica, busca en internet, analiza y redacta — todo de forma autónoma, sin intervención humana.

A diferencia de un chatbot que responde con su conocimiento entrenado, este sistema busca información actualizada en internet en tiempo real, la filtra y la sintetiza en un reporte profesional en formato Markdown.

🌐 **Demo en vivo:** https://research-agent-production-4a93.up.railway.app

---

## Demo

![Demo del sistema](demo.gif)

---

## Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Orquestación de agentes | LangGraph |
| Modelo de lenguaje | Claude Haiku (Anthropic API) |
| Búsqueda web | Tavily API |
| Backend / API REST | FastAPI + Uvicorn |
| Frontend | HTML · CSS · JavaScript vanilla |
| Contenedorización | Docker |
| Despliegue | Railway |
| Configuración | python-dotenv |
| Entorno | Python 3.11 + venv |

---

## Arquitectura del sistema

```
research-agent/
├── src/
│   ├── estado.py          # Estado compartido del grafo
│   ├── nodos.py           # Funciones de los 4 agentes
│   ├── agente.py          # Construcción y compilación del grafo LangGraph
│   └── main_api.py        # API REST con FastAPI
├── index.html             # Interfaz web
├── Dockerfile             # Configuración para despliegue en contenedor
├── .env                   # Variables de entorno (no se sube a GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ¿Cómo funciona el pipeline?

```
tema ingresado por el usuario
        ↓
[1. Planificador] — descompone el tema en 5 subtemas de investigación
        ↓
[2. Buscador] — busca información web para cada subtema usando Tavily
        ↓
[3. Analista] — filtra y sintetiza la información más relevante
        ↓
[4. Redactor] — genera el reporte final estructurado en Markdown
        ↓
reporte entregado al usuario
```

**Estado compartido entre nodos:**

```python
class EstadoInvestigacion(TypedDict):
    tema: str           # tema ingresado por el usuario
    subtemas: List[str] # generados por el planificador
    resultados: List[str] # encontrados por el buscador en internet
    analisis: str        # síntesis filtrada por el analista
    reporte: str          # reporte final del redactor
```

---

## ¿Qué hace diferente a este sistema de un chatbot común?

Un chatbot responde con el conocimiento que el modelo aprendió durante su entrenamiento, que tiene una fecha de corte. Este sistema en cambio:

1. Busca información actual en internet en el momento de la consulta
2. Descompone el tema en múltiples ángulos de investigación en paralelo
3. Filtra y cruza información de varias fuentes antes de responder
4. Entrega un documento estructurado, no una respuesta conversacional

---

## Endpoint de la API

### `POST /analizar`

Recibe un tema en lenguaje natural y devuelve el reporte de investigación completo.

**Request:**
```json
{
  "mensaje": "Impacto de la inteligencia artificial en el empleo"
}
```

**Response:**
```json
{
  "respuesta": "# Impacto de la IA en el empleo\n\n## Introducción...",
  "tema": "Impacto de la inteligencia artificial en el empleo"
}
```

---

## Instalación y uso

### Requisitos previos

- Python 3.11
- API Key de Anthropic ([console.anthropic.com](https://console.anthropic.com))
- API Key de Tavily ([tavily.com](https://tavily.com))

### Opción 1 — Acceso directo

```
https://research-agent-production-4a93.up.railway.app
```

### Opción 2 — Correr localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/FedericoLami/research-agent.git
cd research-agent

# 2. Crear y activar entorno virtual
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env en la raíz del proyecto:
ANTHROPIC_API_KEY=tu-api-key-anthropic
TAVILY_API_KEY=tu-api-key-tavily

# 5. Iniciar el servidor
uvicorn src.main_api:app --reload

# 6. Abrir en el navegador
# http://127.0.0.1:8000
```

### Opción 3 — Correr con Docker

```bash
docker build -t research-agent .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=tu-api-key -e TAVILY_API_KEY=tu-api-key-tavily research-agent
```

### Documentación interactiva de la API

```
https://research-agent-production-4a93.up.railway.app/docs
```

---

## Autor

**Federico Lami**
[LinkedIn](https://www.linkedin.com/in/federicolami/) · [GitHub](https://github.com/FedericoLami/research-agent)