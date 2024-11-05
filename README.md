
# Proyecto: Máquina de Turing de Doble Cinta

### Nombre: Oscar Javier Ortíz Pocón
### Carnet: 1182222

## Descripción General
Este proyecto implementa una Máquina de Turing de doble cinta en Python. La máquina acepta cadenas de caracteres y las procesa de acuerdo con un conjunto de reglas definidas en una función de transición. Cada cinta maneja los símbolos en posiciones pares e impares de la cadena de entrada, permitiendo a la máquina procesar la cadena en ambas direcciones.

## Requisitos
- Python 3.x
- Librerías adicionales:
  - `graphviz` (para la visualización del grafo de derivación)
  - `tabulate` (para la presentación tabular de la 7-tupla)

## Estructura del Código

### Clase `TuringMachine`
La clase `TuringMachine` encapsula la lógica de la máquina de Turing. Incluye:
- **7-Tupla**: Define la máquina en términos de estados (`Q`), alfabeto de entrada (`Σ`), alfabeto de cinta (`Γ`), estado inicial, estados finales y función de transición.
- **`self.transitions`**: Diccionario de transiciones que define el comportamiento de la máquina.
- **`toggle_direction`**: Alterna la dirección de movimiento del cabezal entre izquierda (L) y derecha (R).
- **`print_7_tuple`**: Imprime la configuración inicial de la máquina en formato de tabla.
- **`load_tape`**: Carga la cadena en las dos cintas, dividiéndola en posiciones pares e impares.
- **`print_tape_state`**: Muestra el estado actual de ambas cintas y cabezales, y el estado de la máquina.
- **`run`**: Ejecuta la máquina, procesando la cadena paso a paso, alternando la dirección y verificando si alcanza un estado final.
- **`step`**: Realiza un paso en la cinta, cambiando de estado y desplazando el cabezal según la función de transición.

### Funciones Adicionales
- **`generarTabla`**: Genera la tabla de transición en dirección derecha, para simular el comportamiento de la máquina en esa dirección.
- **`generarTablaReversa`**: Genera la tabla de transición en dirección izquierda, simulando el comportamiento en sentido contrario.
- **`obtener_siguiente_estado`**: Determina el siguiente estado de la máquina en base al estado actual y al símbolo leído.
- **`generar_arbol_derivacion`**: Genera un árbol de derivación de la cadena de entrada y lo exporta como un archivo PNG usando Graphviz.

### Ejecución del Proyecto
El programa carga las cadenas de entrada desde el archivo `cadena.txt` y las procesa. Para cada cadena:
1. Se genera y muestra la tabla de transición.
2. Se ejecuta la máquina para verificar si la cadena es aceptada o rechazada.
3. Se genera un árbol de derivación en formato PNG para cada cadena.

### Explicación de Componentes Específicos

- **7-Tupla de la Máquina de Turing**
  - **`Γ` (Alfabeto de cinta)**: `{'a', 'b', '*', '#', ' '}`. Define los símbolos que pueden aparecer en la cinta.
  - **`Σ` (Alfabeto de entrada)**: `{'a', 'b', '*', '#'}`. Alfabeto de entrada que la máquina acepta.
  - **`b` (Símbolo en blanco)**: `" "`. Utilizado para representar espacios en la cinta.
  - **`Q` (Conjunto de estados)**: `{'q0', 'q1', 'q2', 'q3', 'q4'}`. Estados posibles de la máquina.
  - **`q0` (Estado inicial)**: `'q0'`. La máquina empieza en este estado.
  - **`F` (Estados finales)**: `{'q4'}`. La máquina termina en este estado si la cadena es aceptada.
  - **`f` (Función de transición)**: Diccionario de transiciones que define cómo la máquina cambia de estado y mueve el cabezal.

- **Grafo de Derivación**
  Utilizando Graphviz, el grafo representa la secuencia de estados alcanzados por la máquina al procesar cada símbolo de la cadena de entrada.

- **Tablas de Simbología y de Transición**
  La tabla de transición ilustra las reglas que la máquina sigue al leer símbolos de la cinta en cada estado. Estas se pueden representar en Excel para una mayor claridad visual.
