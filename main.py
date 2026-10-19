from controller.controlador import ControladorSimulacion
from view.vista_animada import VistaAnimada

if __name__ == "__main__":
    print("Simulación M/M/1 (consola animada + gráficas guardadas en la carpeta 'graficas')")
    vista = VistaAnimada(ventana=40, seg_por_unidad=0.25)
    controlador = ControladorSimulacion(vista)
    controlador.ejecutar()
