class Metricas:
    def __init__(self, rho, L, Lq, W, Wq,
                 tiempos_espera=None, traza_cola=None, eventos=None):
        self.rho = rho
        self.L = L
        self.Lq = Lq
        self.W = W
        self.Wq = Wq

        self.tiempos_espera = tiempos_espera or []
        self.traza_cola = traza_cola or []
        self.eventos = eventos or []
