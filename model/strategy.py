from abc import ABC, abstractmethod

import numpy as np
import simpy

from model.matricas import Metricas


class EstrategiaMetricas(ABC):

    @abstractmethod
    def calcular(self, esc):
        pass


class EstrategiaTeorica(EstrategiaMetricas):

    def calcular(self, esc):
        lam = esc.lam
        mu = esc.mu

        rho = lam / mu
        L = lam / (mu - lam)
        Lq = lam ** 2 / (mu * (mu - lam))
        W = 1 / (mu - lam)
        Wq = lam / (mu * (mu - lam))

        return Metricas(rho, L, Lq, W, Wq)


class EstrategiaSimulada(EstrategiaMetricas):
    """Calcula simulando clientes con SimPy."""

    def calcular(self, esc):
        rng = np.random.default_rng(esc.semilla)    
        env = simpy.Environment()
        servidor = simpy.Resource(env, capacity=1)  

        esperas = []                
        estancias = []              
        traza = [(0.0, 0)]          
        eventos = []                

        acum = {"ultimo": 0.0, "area_cola": 0.0,
                "area_sistema": 0.0, "ocupado": 0.0}

        def actualizar():
            """Suma lo ocurrido desde el último cambio de estado."""
            dt = env.now - acum["ultimo"]
            en_cola = len(servidor.queue)
            en_servicio = servidor.count
            acum["area_cola"] += en_cola * dt
            acum["area_sistema"] += (en_cola + en_servicio) * dt
            acum["ocupado"] += en_servicio * dt
            acum["ultimo"] = env.now

        def cliente(numero):
            llegada = env.now
            eventos.append((env.now, "llegada", numero))
            actualizar()
            with servidor.request() as pedido:
                traza.append((env.now, len(servidor.queue)))    
                yield pedido                                    
                traza.append((env.now, len(servidor.queue)))    
                eventos.append((env.now, "inicio", numero))
                esperas.append(env.now - llegada)
                yield env.timeout(rng.exponential(1 / esc.mu))  
                estancias.append(env.now - llegada)
                actualizar()
                eventos.append((env.now, "salida", numero))

        def generador_de_clientes():
            numero = 0
            while True:
                yield env.timeout(rng.exponential(1 / esc.lam)) 
                numero += 1
                env.process(cliente(numero))

        env.process(generador_de_clientes())
        env.run(until=esc.tiempo_simulacion)
        actualizar()

        T = esc.tiempo_simulacion
        rho = acum["ocupado"] / T
        L = acum["area_sistema"] / T
        Lq = acum["area_cola"] / T
        W = sum(estancias) / len(estancias)
        Wq = sum(esperas) / len(esperas)

        return Metricas(rho, L, Lq, W, Wq, esperas, traza, eventos)
