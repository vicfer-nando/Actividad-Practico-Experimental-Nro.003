class Escenarios:
    def __init__(self, numero, lam, mu, condicion,
                 tiempo_simulacion=10000.0, semilla=42):
        self.numero = numero
        self.lam = lam
        self.mu = mu
        self.condicion = condicion
        self.tiempo_simulacion = tiempo_simulacion
        self.semilla = semilla

    def rho(self):
        return self.lam / self.mu

    def es_estable(self):
        return self.lam < self.mu