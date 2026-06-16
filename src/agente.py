from langgraph.graph import StateGraph, END
from src.nodos import nodo_planificador, nodo_buscador, nodo_analista, nodo_redactor
from src.estado import EstadoInvestigacion

grafo = StateGraph(EstadoInvestigacion)
grafo.add_node("planificador", nodo_planificador)
grafo.add_node("buscador", nodo_buscador)
grafo.add_node("analizador", nodo_analista)
grafo.add_node("redactor", nodo_redactor)

grafo.set_entry_point("planificador")
grafo.add_edge("planificador", "buscador")
grafo.add_edge("buscador","analizador")
grafo.add_edge("analizador","redactor")
grafo.add_edge("redactor", END)

grafo_app = grafo.compile()