# Simulación de líneas de espera M/M/1

Programa en Python que **compara el modelo teórico de una cola M/M/1 con una simulación de eventos discretos**. Para cada escenario (λ, μ) calcula las métricas ρ, L, Lq, W y Wq de dos formas (fórmulas y simulación con SimPy), anima la cola en la terminal y guarda tres gráficas comparativas.

## 1. Tecnologías

| Tecnología | Versión usada en el desarrollo | Para qué se usa |
|---|---|---|
| Python | 3.14.4 (según `.venv/pyvenv.cfg`) | Lenguaje del proyecto |
| [SimPy] | 4.1.2 | Simulación de eventos discretos (llegadas, cola y servidor) |
| [NumPy]| 2.5.4 | Generador aleatorio con semilla y distribución exponencial |
| [Matplotlib] | 3.11.2 | Gráficas guardadas como imágenes PNG (backend `Agg`, sin ventanas) |

Del lenguaje estándar se usan: `abc` (clases abstractas), `threading` y `queue` (hilos y comunicación entre ellos), `collections.deque` (cola de clientes en la animación), `os`, `sys` y `time`.

La animación en consola usa **códigos ANSI** (colores y movimiento del cursor), por lo que no requiere ninguna librería adicional.


## 2. Fundamento teórico

Una cola **M/M/1** tiene llegadas de Poisson (tiempos entre llegadas exponenciales), tiempos de servicio exponenciales y **un solo servidor**.

| Símbolo | Significado |
|---|---|
| λ | Tasa de llegadas (clientes por unidad de tiempo) |
| μ | Tasa de servicio (clientes atendidos por unidad de tiempo) |
| ρ = λ/μ | Utilización del servidor |
| L | Número promedio de clientes en el sistema |
| Lq | Número promedio de clientes en la cola |
| W | Tiempo promedio en el sistema |
| Wq | Tiempo promedio de espera en la cola |

Fórmulas teóricas (implementadas en `EstrategiaTeorica`), válidas solo si **λ < μ**:

```
ρ  = λ / μ
L  = λ / (μ − λ)
Lq = λ² / (μ · (μ − λ))
W  = 1 / (μ − λ)
Wq = λ / (μ · (μ − λ))
```

Si λ ≥ μ el sistema es inestable (la cola crece sin límite). El programa lo detecta con `Escenarios.es_estable()` y muestra un aviso en lugar de calcular.

**Simulación** (`EstrategiaSimulada`): se simulan 10 000 unidades de tiempo por escenario (`tiempo_simulacion`) con semilla fija (`semilla=42`), de modo que los resultados son reproducibles. L, Lq y ρ se calculan como promedios en el tiempo (área bajo la curva dividida entre el tiempo total); W y Wq, como promedio sobre los clientes atendidos.

### Escenarios incluidos

| Escenario | λ | μ | ρ | Condición |
|---|---|---|---|---|
| 1 | 2.0 | 3.0 | 0.67 | Sistema estable |
| 2 | 2.5 | 3.0 | 0.83 | Mayor utilización |
| 3 | 2.9 | 3.0 | 0.97 | Cerca de saturación |

---

## 3. Instalación

### Requisitos previos

- Python 3 instalado (el proyecto se desarrolló con 3.14.4).
- `pip`.
- Una terminal con soporte de **UTF-8 y colores ANSI** (por los símbolos `λ μ ρ █ ▁ ┌` y los colores de la animación).

### Pasos

1. Ubícate en la carpeta del proyecto (la que contiene `main.py`):

   ```bash
   cd simul_lineas_espera
   ```

2. Crea un entorno virtual (recomendado):

   ```bash
   python3 -m venv .venv
   ```

3. Actívalo:

   | Sistema | Comando |
   |---|---|
   | Linux / macOS | `source .venv/bin/activate` |
4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

   Esto instala `simpy`, `matplotlib` y `numpy` (contenido de `requirements.txt`).

## 4. Cómo ejecutar

Desde la carpeta del proyecto (donde está `main.py`) y con el entorno virtual activado:

```bash
python main.py
```

> **Importante:** ejecútalo desde la carpeta raíz del proyecto. Los módulos se importan como `from model...`, `from view...` y `from controller...`, así que Python necesita que esa carpeta sea el directorio actual.

---

## 5. Cómo usar el programa

1. Al iniciar verás el mensaje: `Simulación M/M/1 (consola animada + gráficas guardadas en la carpeta 'graficas')`.
2. Para cada escenario aparece: `Presiona Enter para ver la animación del escenario N (Ctrl+C la salta)...`
   - **Enter**: reproduce la animación.
   - **Ctrl+C** durante la animación: la detiene y pasa a la tabla del escenario.
3. Tras la animación se imprime la **tabla del escenario** con las medidas teóricas y simuladas (ρ, L, Lq, W, Wq).
4. Cuando terminan los tres escenarios se imprime la **tabla comparativa** y se guardan las gráficas en la carpeta `graficas/`.

### Qué muestra la animación

Se anima solo la **ventana inicial de 40 unidades de tiempo simulado** (a razón de 1.0 s reales por unidad, unos 10 segundos por escenario):

- Barra de progreso del tiempo.
- La cola FIFO (los 8 clientes más cercanos al servidor; si hay más se muestra `+N`) y el estado del servidor (`libre` u ocupado con el número de cliente).
- Contadores: en cola, en el sistema, llegadas, atendidos, cola máxima y espera promedio hasta ese momento.
- Un mini gráfico de barras con el tamaño de la cola en el tiempo.
- El último evento ocurrido (llegada, paso al servidor, salida).

### Parámetros que puedes cambiar

| Qué | Dónde | Valor actual |
|---|---|---|
| Tiempo simulado que se anima | `VistaAnimada(ventana=...)` en `main.py` | `40` |
| Velocidad de la animación (segundos reales por unidad simulada) | `VistaAnimada(seg_por_unidad=...)` en `main.py` | `1.0` |
| Carpeta de las gráficas | `VistaAnimada(carpeta=...)` | `"graficas"` |
| Escenarios (λ, μ, descripción) | `FabricaEscenarios.crear_todos()` en `model/factory.py` | 3 escenarios |
| Duración de la simulación | `Escenarios(tiempo_simulacion=...)` en `model/escenarios.py` | `10000.0` |
| Semilla aleatoria | `Escenarios(semilla=...)` en `model/escenarios.py` | `42` |

---

## 6. Estructura del proyecto

```
simul_lineas_espera/
├── main.py                  # Punto de entrada: arma la vista y el controlador y ejecuta
├── requirements.txt         # Dependencias: simpy, matplotlib, numpy
├── model/                   # MODELO: datos y cálculo, sin entrada/salida
│   ├── escenarios.py        # Clase Escenarios (λ, μ, tiempo, semilla, ρ, estabilidad)
│   ├── matricas.py          # Clase Metricas (ρ, L, Lq, W, Wq + trazas y eventos)
│   ├── strategy.py          # EstrategiaMetricas, EstrategiaTeorica, EstrategiaSimulada
│   └── factory.py           # FabricaEscenarios y FabricaEstrategias
├── view/                    # VISTA: todo lo que se muestra al usuario
│   ├── vista_consola.py     # VistaBase (contrato) y VistaConsola (tablas de texto)
│   └── vista_animada.py     # VistaAnimada: animación en consola + gráficas PNG
├── controller/              # CONTROLADOR: coordina modelo y vista
│   └── controlador.py       # ControladorSimulacion (productor/consumidor con hilos)
└── graficas/                # Salida: imágenes generadas al ejecutar
```

### Por qué está organizado así

- **Separación por responsabilidades (MVC).** El modelo calcula, la vista muestra y el controlador conecta ambos. El modelo no imprime ni dibuja nada, y la vista no calcula métricas. Así se puede cambiar cómo se presenta el resultado (consola, animación, otra interfaz) sin tocar las fórmulas ni la simulación, y al revés.
- **`model/`** contiene lo que describe el problema: qué es un escenario (`Escenarios`), qué se mide (`Metricas`) y cómo se calcula (las estrategias). Las fábricas viven aquí porque deciden qué objetos del modelo se crean.
- **`view/`** separa el contrato (`VistaBase`) de las implementaciones. `VistaConsola` imprime tablas; `VistaAnimada` hereda de ella, añade la animación y las gráficas, y reutiliza las tablas con `super()`.
- **`controller/`** es la única pieza que conoce a la vez el modelo (fábricas) y la vista (que recibe por parámetro). Contiene la lógica de coordinación y de concurrencia.
- **`main.py`** solo ensambla las piezas. Si se quiere otra vista, basta cambiar una línea aquí.
- **`graficas/`** es carpeta de salida (la crea la vista si no existe), separada del código.

### Responsabilidad de cada clase

| Clase | Archivo | Responsabilidad |
|---|---|---|
| `Escenarios` | `model/escenarios.py` | Guarda λ, μ, tiempo de simulación y semilla; calcula ρ e indica si el sistema es estable |
| `Metricas` | `model/matricas.py` | Contenedor de resultados: ρ, L, Lq, W, Wq, tiempos de espera, traza de la cola y lista de eventos |
| `EstrategiaMetricas` | `model/strategy.py` | Clase abstracta: define `calcular(esc)` |
| `EstrategiaTeorica` | `model/strategy.py` | Aplica las fórmulas M/M/1 |
| `EstrategiaSimulada` | `model/strategy.py` | Simula con SimPy (generador de clientes, servidor de capacidad 1) y calcula las métricas |
| `FabricaEscenarios` | `model/factory.py` | Crea la lista de escenarios |
| `FabricaEstrategias` | `model/factory.py` | Crea la estrategia según el tipo (`"teorico"` o `"simulado"`) |
| `VistaBase` | `view/vista_consola.py` | Clase abstracta con los 3 métodos que toda vista debe tener |
| `VistaConsola` | `view/vista_consola.py` | Imprime las tablas de texto |
| `VistaAnimada` | `view/vista_animada.py` | Anima la cola y guarda las gráficas |
| `ControladorSimulacion` | `controller/controlador.py` | Calcula los escenarios en un hilo y los entrega a la vista en el hilo principal |

---

## 7. Patrones de diseño

### 7.1 MVC (Modelo–Vista–Controlador)

Patrón arquitectónico que organiza las carpetas `model/`, `view/` y `controller/` (ver sección anterior).

- **Por qué:** mantener separados el cálculo, la presentación y la coordinación.

### 7.2 Strategy

- **Dónde:** `EstrategiaMetricas` (interfaz) con `EstrategiaTeorica` y `EstrategiaSimulada` (`model/strategy.py`).
- **Qué resuelve:** hay dos formas intercambiables de obtener el mismo resultado (un objeto `Metricas`). Ambas se usan con la misma llamada, `calcular(esc)`.
- **Por qué:** el controlador no necesita saber cómo se calcula cada una; para añadir otro método (por ejemplo, otra distribución o más servidores) se crea una nueva estrategia sin modificar las existentes.

### 7.3 Factory (fábrica con métodos estáticos)

- **Dónde:** `FabricaEscenarios.crear_todos()` y `FabricaEstrategias.crear(tipo)` (`model/factory.py`).
- **Qué resuelve:** centraliza la creación de objetos. Si el tipo de estrategia no existe, lanza `ValueError`.
- **Por qué:** el controlador pide "una estrategia teórica" o "los escenarios" sin conocer las clases concretas ni sus parámetros. Cambiar o añadir escenarios se hace en un solo lugar.

### 7.4 Inyección de dependencias (por constructor)

- **Dónde:** `ControladorSimulacion(vista)` recibe la vista desde `main.py`.
- **Por qué:** el controlador funciona con cualquier objeto que cumpla el contrato de `VistaBase`, sin crear él mismo la vista. Eso facilita cambiar de vista o probar el controlador por separado.

### 7.5 Clase base abstracta y polimorfismo (jerarquía de vistas)

- **Dónde:** `VistaBase` → `VistaConsola` → `VistaAnimada` (`view/`).
- **Qué hace:** `VistaBase` obliga a implementar `mostrar_inestable`, `mostrar_escenario` y `mostrar_tabla_comparativa`. `VistaAnimada` sobrescribe `mostrar_escenario` (añade la animación y luego llama a `super()` para mostrar la tabla de siempre) y `mostrar_tabla_comparativa` (llama a `super()` y luego guarda las gráficas).
- **Por qué:** se extiende el comportamiento sin duplicar código. El controlador trata ambas vistas de la misma manera.

### 7.6 Productor–consumidor (concurrencia)

- **Dónde:** `ControladorSimulacion` (`controller/controlador.py`).
- **Cómo funciona:**
  - El **hilo productor** (`producir`) calcula cada escenario (teórico y simulado) y lo deja en una `queue.Queue(maxsize=1)`.
  - El **hilo principal** (consumidor, `ejecutar`) toma los escenarios de la cola y los muestra.
  - La constante `FIN = object()` es un **centinela** que indica que el productor terminó.
  - Si el productor falla, deja la excepción en la cola y el consumidor la vuelve a lanzar.
- **Por qué:**
  - Mientras se anima un escenario, el siguiente ya se está calculando.
  - `maxsize=1` evita que el productor se adelante demasiado y acumule resultados en memoria.
  - El consumidor se queda en el **hilo principal** para que **Ctrl+C** pueda interrumpir la animación (las señales llegan al hilo principal).
  - El hilo productor es `daemon`, así que no deja el programa colgado si este termina antes.

### 7.7 Objeto contenedor de datos

- **Dónde:** `Metricas` (`model/matricas.py`).
- **Por qué:** agrupa en un solo objeto todo lo que producen las estrategias (métricas, tiempos de espera, traza de la cola y eventos), de forma que la vista los recibe juntos y no depende de cómo se obtuvieron.

---

## 8. Flujo de ejecución

```
main.py
  │  crea VistaAnimada y ControladorSimulacion(vista)
  ▼
ControladorSimulacion.ejecutar()
  │
  ├── Hilo productor ──────────────────────────────────────────┐
  │     para cada escenario (FabricaEscenarios):               │
  │       ¿λ < μ? no → pone (esc, None, None)                  │
  │       sí → EstrategiaTeorica.calcular  → Metricas (t)      │
  │            EstrategiaSimulada.calcular → Metricas (s)      │
  │       pone (esc, t, s) en Queue(maxsize=1)                 │
  │     al final pone FIN                                      │
  │                                                            ▼
  └── Hilo principal (consumidor) ◄───────────── Queue ────────┘
        toma cada elemento:
          t es None → vista.mostrar_inestable(esc)
          si no     → vista.mostrar_escenario(esc, t, s)
                         ├─ espera Enter
                         ├─ armar_cuadros(eventos)   → "fotos" de la cola
                         ├─ reproducir(cuadros)      → animación en consola
                         └─ tabla del escenario (VistaConsola)
        al recibir FIN:
          vista.mostrar_tabla_comparativa(resultados)
              ├─ tabla comparativa (VistaConsola)
              └─ guarda las 3 gráficas en graficas/
```

### Cómo funciona la animación (`VistaAnimada`)

1. `armar_cuadros` recorre los eventos del modelo (`llegada`, `inicio`, `salida`) y genera un "cuadro" por cada instante (los eventos simultáneos van en el mismo cuadro).
2. `armar_serie` toma el tamaño de la cola a intervalos iguales para el mini gráfico.
3. `reproducir` dibuja los cuadros uno tras otro y espera entre ellos el tiempo simulado multiplicado por `seg_por_unidad` (con un máximo de 1.5 s por pausa).
4. `dibujar` construye las líneas de texto de cada cuadro. Para redibujar sobre el mismo lugar, `reproducir` sube el cursor tantas líneas como tiene el cuadro (`\033[NA`); al terminar, vuelve a mostrar el cursor.

---

## 9. Cómo extender el proyecto

**Agregar un escenario:** añade una línea en `FabricaEscenarios.crear_todos()`:

```python
Escenarios(4, 1.0, 3.0, "Poca carga"),
```

Si λ ≥ μ, el programa mostrará el aviso de sistema inestable en lugar de calcular.

**Agregar un método de cálculo (Strategy):**

1. Crea una clase que herede de `EstrategiaMetricas` e implemente `calcular(self, esc)` devolviendo un `Metricas`.
2. Regístrala en `FabricaEstrategias.crear`.

**Agregar otra vista:** crea una clase que herede de `VistaBase` (o de `VistaConsola`) e implemente los tres métodos, y pásala al controlador en `main.py`:

```python
controlador = ControladorSimulacion(MiNuevaVista())
```

> Las gráficas de `VistaAnimada.mostrar_tabla_comparativa` usan hoy los tres escenarios en filas; si agregas muchos escenarios, puede que haya que ajustar el tamaño de la figura (`figsize`).

---

## 10. Resultados de ejemplo

Salida de la tabla comparativa con los valores por defecto (semilla 42, 10 000 unidades de tiempo):

```
Esc      λ    μ    ρ(T)    L(T)    L(S)   Lq(T)   Lq(S)    W(T)    W(S)   Wq(T)   Wq(S)
1      2.0  3.0   0.667   2.000   2.079   1.333   1.410   1.000   1.040   0.667   0.705
2      2.5  3.0   0.833   5.000   5.334   4.167   4.499   2.000   2.132   1.667   1.799
3      2.9  3.0   0.967  29.000  24.756  28.033  23.794  10.000   8.561   9.667   8.228
```

(T = teórico, S = simulado.)

**Observación:** en los escenarios 1 y 2 los valores simulados quedan cerca de los teóricos. En el escenario 3 (ρ ≈ 0.97) la diferencia es mayor. Es un comportamiento esperable en colas muy cargadas, donde el promedio converge más lentamente; sin embargo, con una sola semilla y un solo tiempo de simulación no se comprobó cuánto mejora con más tiempo o con otras semillas.

---

