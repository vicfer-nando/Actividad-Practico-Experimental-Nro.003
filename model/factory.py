from model.escenarios import Escenarios
from model.strategy import EstrategiaSimulada, EstrategiaTeorica


class FabricaEscenarios:
    
    @staticmethod
    def crear_todos():
        return [
            Escenarios(1, 2.0, 3.0, "Sistema estable"),
            Escenarios(2, 2.5, 3.0, "Mayor utilización"),
            Escenarios(3, 2.9, 3.0, "Cerca de saturación"),
        ]


class FabricaEstrategias:

    @staticmethod
    def crear(tipo):
        if tipo == "teorico":
            return EstrategiaTeorica()
        if tipo == "simulado":
            return EstrategiaSimulada()
        raise ValueError("Estrategia desconocida: " + tipo)
