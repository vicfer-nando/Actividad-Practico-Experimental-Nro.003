import queue
import threading

from model.factory import FabricaEscenarios, FabricaEstrategias

FIN = object()     

class ControladorSimulacion:
    """Conecta el modelo con la vista usando dos hilos.

    - Hilo productor: calcula cada escenario (teórico + simulado) y lo deja en una cola.
    - Hilo principal (consumidor): saca los escenarios de la cola y los muestra.
      Se queda en el hilo principal para que Ctrl+C siga saltando la animación.
    """

    def __init__(self, vista):
        self.vista = vista
        self.teorica = FabricaEstrategias.crear("teorico")
        self.simulada = FabricaEstrategias.crear("simulado")

    def producir(self, cola):
        try:
            for esc in FabricaEscenarios.crear_todos():
                if not esc.es_estable():
                    cola.put((esc, None, None))
                    continue
                t = self.teorica.calcular(esc)
                s = self.simulada.calcular(esc)
                cola.put((esc, t, s))       
        except Exception as error:         
            cola.put(error)
        finally:
            cola.put(FIN)

    def ejecutar(self):
        cola = queue.Queue(maxsize=1)
        productor = threading.Thread(target=self.producir, args=(cola,),
                                     name="productor", daemon=True)
        productor.start()

        resultados = []
        while True:
            item = cola.get()
            if item is FIN:
                break
            if isinstance(item, Exception):
                raise item
            esc, t, s = item
            if t is None:
                self.vista.mostrar_inestable(esc)
                continue
            self.vista.mostrar_escenario(esc, t, s)
            resultados.append(item)

        productor.join()
        self.vista.mostrar_tabla_comparativa(resultados)
        return resultados