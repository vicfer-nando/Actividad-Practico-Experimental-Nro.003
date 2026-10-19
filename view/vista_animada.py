import os
import sys
import time

import matplotlib
matplotlib.use("Agg")           
import matplotlib.pyplot as plt
import numpy as np

from view.vista_consola import VistaConsola

NEGRITA = "\033[1m"
CYAN = "\033[96m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
GRIS = "\033[90m"
RESET = "\033[0m"

HUECOS = 8              
ANCHO = 5               

class VistaAnimada(VistaConsola):
    """Consola con la cola en movimiento; al final guarda las gráficas en una carpeta."""

    def __init__(self, ventana=40, seg_por_unidad=1.0, carpeta="graficas"):
        self.ventana = ventana                  
        self.seg_por_unidad = seg_por_unidad    
        self.carpeta = carpeta
        os.makedirs(carpeta, exist_ok=True)     

    def mostrar_escenario(self, esc, t, s):
        try:
            input(f"\nPresiona Enter para ver la animación del escenario "
                  f"{esc.numero} (Ctrl+C la salta)... ")
        except EOFError:
            pass
        cuadros = self.armar_cuadros(s.eventos)
        self.reproducir(esc, cuadros)
        super().mostrar_escenario(esc, t, s)    

    # ------------------------------------------------------------------
    # 1) Convertir los eventos del modelo en "cuadros" (fotos de la cola)
    # ------------------------------------------------------------------
    def armar_cuadros(self, eventos):
        cola = []                   
        servidor = None            
        llegadas = 0
        atendidos = 0
        cola_max = 0
        esperas = []                
        llegada_de = {}            
        mensajes = []               

        cuadros = [{"tiempo": 0.0, "mensaje": "Inicia la simulación", "cola": [],
                    "servidor": None, "llegadas": 0, "atendidos": 0,
                    "cola_max": 0, "espera_prom": 0.0}]

        for i in range(len(eventos)):
            tiempo, tipo, cid = eventos[i]
            if tiempo > self.ventana:
                break

            if tipo == "llegada":
                cola.append(cid)
                llegada_de[cid] = tiempo
                llegadas += 1
                mensajes.append(f"Llega el cliente #{cid}")
            elif tipo == "inicio":
                cola.remove(cid)
                servidor = cid
                espera = tiempo - llegada_de[cid]
                esperas.append(espera)
                mensajes.append(f"#{cid} pasa al servidor (esperó {espera:.2f})")
            else:  
                servidor = None
                atendidos += 1
                mensajes.append(f"#{cid} termina y sale")

            hay_mas_en_este_instante = (i + 1 < len(eventos)
                                        and eventos[i + 1][0] == tiempo)
            if hay_mas_en_este_instante:
                continue

            cola_max = max(cola_max, len(cola))
            espera_prom = sum(esperas) / len(esperas) if esperas else 0.0
            cuadros.append({"tiempo": tiempo, "mensaje": "  →  ".join(mensajes),
                            "cola": list(cola), "servidor": servidor,
                            "llegadas": llegadas, "atendidos": atendidos,
                            "cola_max": cola_max, "espera_prom": espera_prom})
            mensajes = []

        cuadros.append(dict(cuadros[-1], tiempo=self.ventana, mensaje="Fin de la animación"))
        return cuadros

    # ------------------------------------------------------------------
    # 2) Mostrar los cuadros uno tras otro
    # ------------------------------------------------------------------
    def reproducir(self, esc, cuadros):
        sys.stdout.write("\033[?25l")                
        try:
            for i, cuadro in enumerate(cuadros):
                lineas = self.dibujar(esc, cuadro)
                if i > 0:
                    sys.stdout.write(f"\033[{len(lineas)}A")   
                sys.stdout.write("".join(l + "\033[K\n" for l in lineas))
                sys.stdout.flush()
                if i + 1 < len(cuadros):
                    pausa = (cuadros[i + 1]["tiempo"] - cuadro["tiempo"]) * self.seg_por_unidad
                    time.sleep(min(pausa, 1.5))
        except KeyboardInterrupt:
            print("\nAnimación detenida.")
        finally:
            sys.stdout.write("\033[?25h")             
            sys.stdout.flush()

    def dibujar(self, esc, c):
        avance = int(c["tiempo"] / self.ventana * 30)
        barra = "█" * avance + "░" * (30 - avance)

        frente = c["cola"][:HUECOS]
        extra = len(c["cola"]) - len(frente)       
        if extra > 0:
            prefijo = f"+{extra}".rjust(ANCHO)
        else:
            prefijo = " " * ANCHO
        casillas = " " * (ANCHO * (HUECOS - len(frente)))
        for numero in reversed(frente):
            casillas += f"{CYAN}[{numero:>3}]{RESET}"
        tubo = "─" * (ANCHO * (HUECOS + 1))

        if c["servidor"] is None:
            servidor = f"{GRIS}[ libre ]{RESET}"
        else:
            servidor = f"{VERDE}[ #{c['servidor']:<3}]{RESET}"

        en_sistema = len(c["cola"])
        if c["servidor"] is not None:
            en_sistema += 1

        return [
            f"{NEGRITA}ESCENARIO {esc.numero}  |  λ={esc.lam}  μ={esc.mu}  "
            f"ρ={esc.rho():.2f}  |  {esc.condicion}{RESET}",
            f"  Tiempo: {c['tiempo']:6.2f} / {self.ventana:.0f}  {AMARILLO}{barra}{RESET}",
            "",
            "  LLEGADAS ──▶   COLA (FIFO)                          SERVIDOR",
            f"  ┌{tubo}┐",
            f"  │{prefijo}{casillas}│ ▶ {servidor}",
            f"  └{tubo}┘",
            "",
            f"  En cola: {len(c['cola']):<3} En sistema: {en_sistema:<3} "
            f"Llegadas: {c['llegadas']:<4} Atendidos: {c['atendidos']:<4} "
            f"Cola máx: {c['cola_max']}",
            f"  Espera promedio hasta ahora: {c['espera_prom']:.2f}",
            f"  Evento: {c['mensaje'][:66]}",
        ]

    # ------------------------------------------------------------------
    # 3) Gráficas: solo se guardan en la carpeta, no se muestran
    # ------------------------------------------------------------------
    def mostrar_tabla_comparativa(self, resultados):
        super().mostrar_tabla_comparativa(resultados)
        if not resultados:
            return
        self.grafica_cola(resultados)
        self.grafica_esperas(resultados)
        self.grafica_comparacion(resultados)
        print("\nGráficas guardadas en la carpeta:", self.carpeta)

    def guardar(self, fig, nombre):
        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta, nombre), dpi=120)
        plt.close(fig)                          

    def grafica_cola(self, resultados, ventana=100):
        """Tamaño de la cola en el tiempo (primeras 'ventana' unidades)."""
        fig, ejes = plt.subplots(len(resultados), 1, figsize=(10, 8),
                                 sharex=True, squeeze=False)
        ejes = ejes.flatten()
        for eje, (esc, t, s) in zip(ejes, resultados):
            tiempos = [p[0] for p in s.traza_cola if p[0] <= ventana]
            colas = [p[1] for p in s.traza_cola if p[0] <= ventana]
            eje.step(tiempos, colas, where="post", color="tab:blue")
            eje.axhline(t.Lq, color="red", linestyle="--",
                        label=f"Lq teórico = {t.Lq:.2f}")
            eje.axhline(s.Lq, color="green", linestyle=":",
                        label=f"Lq simulado = {s.Lq:.2f}")
            eje.set_title(f"Escenario {esc.numero}: λ={esc.lam}, μ={esc.mu} "
                          f"(ρ={esc.rho():.2f})")
            eje.set_ylabel("Clientes en cola")
            eje.legend(loc="upper left")
        ejes[-1].set_xlabel("Tiempo")
        fig.suptitle(f"Tamaño de la cola en el tiempo (primeras {ventana} unidades)")
        self.guardar(fig, "1_tamano_cola.png")

    def grafica_esperas(self, resultados, cantidad=300):
        """Tiempo de espera de los primeros 'cantidad' clientes."""
        fig, ejes = plt.subplots(len(resultados), 1, figsize=(10, 8),
                                 sharex=True, squeeze=False)
        ejes = ejes.flatten()
        for eje, (esc, t, s) in zip(ejes, resultados):
            esperas = s.tiempos_espera[:cantidad]
            eje.plot(range(1, len(esperas) + 1), esperas,
                     color="tab:orange", linewidth=0.9)
            eje.axhline(t.Wq, color="red", linestyle="--",
                        label=f"Wq teórico = {t.Wq:.2f}")
            eje.axhline(s.Wq, color="green", linestyle=":",
                        label=f"Wq simulado = {s.Wq:.2f}")
            eje.set_title(f"Escenario {esc.numero}: λ={esc.lam}, μ={esc.mu}")
            eje.set_ylabel("Espera en cola")
            eje.legend(loc="upper right")
        ejes[-1].set_xlabel("Número de cliente")
        fig.suptitle(f"Tiempo de espera de los primeros {cantidad} clientes")
        self.guardar(fig, "2_tiempos_espera.png")

    def grafica_comparacion(self, resultados):
        """Barras teórico vs simulado para L, Lq, W y Wq."""
        medidas = ["L", "Lq", "W", "Wq"]
        etiquetas = [f"Esc {esc.numero}" for esc, t, s in resultados]
        posiciones = np.arange(len(resultados))
        ancho = 0.35

        fig, ejes = plt.subplots(2, 2, figsize=(10, 8))
        for eje, medida in zip(ejes.flatten(), medidas):
            teoricos = [getattr(t, medida) for esc, t, s in resultados]
            simulados = [getattr(s, medida) for esc, t, s in resultados]
            eje.bar(posiciones - ancho / 2, teoricos, ancho,
                    label="Teórico", color="tab:red")
            eje.bar(posiciones + ancho / 2, simulados, ancho,
                    label="Simulado", color="tab:green")
            eje.set_xticks(posiciones)
            eje.set_xticklabels(etiquetas)
            eje.set_title(medida)
            eje.legend()
        fig.suptitle("Comparación teórico vs simulado")
        self.guardar(fig, "3_comparacion.png")
