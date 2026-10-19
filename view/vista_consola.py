from abc import ABC, abstractmethod


class VistaBase(ABC):
    """Toda vista debe tener estos métodos."""

    @abstractmethod
    def mostrar_inestable(self, esc):
        pass

    @abstractmethod
    def mostrar_escenario(self, esc, teorico, simulado):
        pass

    @abstractmethod
    def mostrar_tabla_comparativa(self, resultados):
        pass


class VistaConsola(VistaBase):

    def mostrar_inestable(self, esc):
        print("\nEscenario", esc.numero, ": El sistema no es estable (λ >= μ)")

    def mostrar_escenario(self, esc, t, s):
        print("\n" + "=" * 62)
        print(f"ESCENARIO {esc.numero} | λ={esc.lam} μ={esc.mu} | {esc.condicion}")
        print("=" * 62)
        print(f"{'Medida':<26}{'Teórico':>14}{'Simulado':>14}")
        print("-" * 62)
        print(f"{'ρ (utilización)':<26}{t.rho:>14.4f}{s.rho:>14.4f}")
        print(f"{'L  (en el sistema)':<26}{t.L:>14.4f}{s.L:>14.4f}")
        print(f"{'Lq (en la cola)':<26}{t.Lq:>14.4f}{s.Lq:>14.4f}")
        print(f"{'W  (tiempo en sistema)':<26}{t.W:>14.4f}{s.W:>14.4f}")
        print(f"{'Wq (espera en cola)':<26}{t.Wq:>14.4f}{s.Wq:>14.4f}")

    def mostrar_tabla_comparativa(self, resultados):
        print("\n" + "=" * 100)
        print("TABLA COMPARATIVA (T = teórico, S = simulado)")
        print("=" * 100)
        print(f"{'Esc':<5}{'λ':>5}{'μ':>5}{'ρ(T)':>8}{'L(T)':>8}{'L(S)':>8}"
              f"{'Lq(T)':>8}{'Lq(S)':>8}{'W(T)':>8}{'W(S)':>8}"
              f"{'Wq(T)':>8}{'Wq(S)':>8}")
        print("-" * 100)
        for esc, t, s in resultados:
            print(f"{esc.numero:<5}{esc.lam:>5}{esc.mu:>5}{t.rho:>8.3f}"
                  f"{t.L:>8.3f}{s.L:>8.3f}{t.Lq:>8.3f}{s.Lq:>8.3f}"
                  f"{t.W:>8.3f}{s.W:>8.3f}{t.Wq:>8.3f}{s.Wq:>8.3f}")
