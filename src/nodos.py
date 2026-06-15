from tavily import TavilyClient
import anthropic
from dotenv import load_dotenv
import os
from src.estado import EstadoInvestigacion

load_dotenv()

client = anthropic.Anthropic()
Tavily_Client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


def nodo_planificador(estado):
    mensajes = [{"role":"user","content": estado["tema"]}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                    Sos un agente dedicado a clasificar subtemas, el formato de tu respuesta debe ser descomponiendo 
                    la oracion recibida en 5 sub-temas para que otro bot pueda buscarlos.
                    Solo podes responder con los subtemas, separado por saltos de linea, nada de texto adicional ni decoradores
                 """,
        messages = mensajes
    )

    estado["subtemas"] = answer.content[0].text.split("\n")
    return estado


def nodo_buscador(estado):
    listaResultado = []
    for subtema in estado["subtemas"]:
        resultado = Tavily_Client.search(query=subtema)
        for item in resultado["results"]:
            listaResultado.append(item["content"])    
    estado["resultados"] = listaResultado
    return estado


def nodo_analista(estado):
    mensajes = [{"role":"user","content": f"Tema: {estado['tema']}\n\nInformación encontrada:\n{chr(10).join(estado['resultados'])}"}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                 Sos un editor que recibe informacion y tu objetivo es convertir todo 
                 el contenido que recibis en un resumen coherente y util, 
                 quedandote solo con lo mas importante y relevante del tema original   
                 """,
        messages = mensajes
    )

    estado["analisis"] = answer.content[0].text
    return estado

def nodo_redactor(estado):
    mensajes = [{"role":"user", "content": f"Tema: {estado['tema']}\n\nAnálisis:\n{estado['analisis']}"}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                    Sos un redactor especializado en investigación y análisis. 
                    Tu tarea es generar un reporte estructurado y profesional basándote en el análisis provisto.

                    El reporte debe estar en formato Markdown con:
                    - Un título principal con el tema
                    - Secciones organizadas por subtema
                    - Conclusiones al final

                    Respondé únicamente con el reporte en Markdown. Sin texto adicional ni explicaciones.
                    No hagas preguntas de seguimiento.
                 """,
        messages = mensajes 
    )
    estado["reporte"] = answer.content[0].text
    return estado