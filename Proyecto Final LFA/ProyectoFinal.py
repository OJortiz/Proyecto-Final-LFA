import re
from graphviz import Digraph
from tabulate import tabulate

class TuringMachine:
    def __init__(self):
        # Definición de la máquina de Turing en forma de 7-tupla
        self.Gamma = {'a', 'b', '*', '#', ' '}  # Γ - Alfabeto de la cinta
        self.Sigma = {'a', 'b', '*', '#'}       # Σ - Alfabeto de entrada
        self.blank_symbol = ' '                 # b - Símbolo en blanco
        self.Q = {'q0', 'q1', 'q2', 'q3', 'q4'}  # Q - Conjunto de estados
        self.initial_state = 'q0'               # q0 - Estado inicial
        self.final_states = {'q4'}              # F - Conjunto de estados finales
        self.current_direction = 'R'
        self.transitions = {
            ('q0', 'a'): ('q1', 'a', 'R'),
            ('q1', 'b'): ('q2', 'b', 'R'),
            ('q2', 'a'): ('q3', 'a', 'R'),
            ('q3', '*'): ('q4', '*', 'R'),
            ('q3', 'b'): ('q1', 'b', 'R'),
            ('q3', 'a'): ('q3', 'a', 'R'),
            ('q4', 'a'): ('q3', 'a', 'R'),
            ('q4', 'b'): ('q1', 'b', 'R'),
            ('q4', '#'): ('q4', '#', 'R')
        }
        
        # Inicializa el estado y las cintas
        self.current_state = self.initial_state
        self.final_state = 'q4'
        self.tape_odd = []
        self.tape_even = []
        self.head_odd = 0
        self.head_even = 0

        self.print_7_tuple()
        
    def toggle_direction(self):
        # Alterna la dirección de lectura entre izquierda y derecha
        self.current_direction = 'L' if self.current_direction == 'R' else 'R'

    def print_7_tuple(self):
        data = [
            ["Γ (Alfabeto de la cinta)", self.Gamma],
            ["Σ (Alfabeto de entrada)", self.Sigma],
            ["b (Símbolo en blanco)", self.blank_symbol],
            ["Q (Conjunto de estados)", self.Q],
            ["q0 (Estado inicial)", self.initial_state],
            ["F (Estados finales)", self.final_states],
            ["f (Función de transición)", self.transitions]
        ]
        print(tabulate(data, headers=["Elemento", "Valor"], tablefmt="grid"))

    def load_tape(self, input_string):
        # Divide la cadena en símbolos de posiciones pares e impares
        self.tape_odd = [input_string[i] for i in range(0, len(input_string), 2)]
        self.tape_even = [input_string[i] for i in range(1, len(input_string), 2)]
        self.head_odd = 0
        self.head_even = 0

    def print_tape_state(self):
        odd_tape_state = ''.join(self.tape_odd)
        even_tape_state = ''.join(self.tape_even)
        print(f"Estado actual de la máquina:")
        print(f"  Cinta impar:  {odd_tape_state}")
        print(f"  Cabezal impar en posición {self.head_odd}: '{self.tape_odd[self.head_odd]}'" if self.head_odd < len(self.tape_odd) else "Cabezal impar fuera de la cinta")
        print(f"  Cinta par:    {even_tape_state}")
        print(f"  Cabezal par en posición {self.head_even}: '{self.tape_even[self.head_even]}'" if self.head_even < len(self.tape_even) else "Cabezal par fuera de la cinta")
        print(f"  Estado actual: {self.current_state}")

    def run(self):
        while self.current_state not in self.final_states:
            self.print_tape_state()
            # Procesar cinta impar
            if self.head_odd is not None:
                self.head_odd = self.step(self.tape_odd, self.head_odd, self.current_direction)
            
            # Procesar cinta par
            if self.head_even is not None:
                self.head_even = self.step(self.tape_even, self.head_even, self.current_direction)
            
            # Verificar si ambos cabezales están en un estado sin transición
            if self.head_odd is None and self.head_even is None:
                print("Cadena no aceptada: Error en transición.")
                return False
            
            # Alterna la dirección de lectura después de cada paso
            self.toggle_direction()
            self.print_tape_state()

        if self.current_state in self.final_states:
            print("Cadena aceptada: La máquina terminó en el estado final.")
            return True
        else:
            print("Cadena no aceptada: Estado final no alcanzado.")
            return False

    def step(self, tape, head, direction):
        symbol = tape[head] if head < len(tape) else self.blank_symbol
        if (self.current_state, symbol) in self.transitions:
            new_state, new_symbol, move_direction = self.transitions[(self.current_state, symbol)]
            tape[head] = new_symbol
            self.current_state = new_state
            # Mueve el cabezal en la dirección especificada
            if move_direction == 'R':
                head = head + 1 if direction == 'R' else head - 1
            elif move_direction == 'L' and head > 0:
                head = head - 1 if direction == 'L' else head + 1
            return head
        else:
            return None  # No hay transición válida
        
# Función para generar la tabla de transiciones en dirección derecha
def generarTabla(mensaje, numero):
    estado = '0'
    tabla_derecha = [['|||', '|a|', '|b|', '|a|', '|*|', '|#|'], 
                     ['|0|', '-', '-', '-', '-', '-'],
                     ['|1|', '-', '-', '-', '-', '-'],
                     ['|2|', '-', '-', '-', '-', '-'],
                     ['|3|', '-', '-', '-', '-', '-'],
                     ['|4|', '-', '-', '-', '-', '-']]
    
    for i in mensaje:
        simbolo = f"|{i}|"
        if estado == "0":
            tabla_derecha[1][tabla_derecha[0].index(simbolo)] = "|1|"
            estado = '1' if simbolo == "|a|" else "0"
        elif estado == "1":
            tabla_derecha[2][tabla_derecha[0].index(simbolo)] = "|2|"
            estado = '2' if simbolo == "|b|" else "1"
        elif estado == "2":
            tabla_derecha[3][tabla_derecha[0].index(simbolo)] = "|3|"
            estado = '3'
        elif estado == "3":
            if simbolo == "|b|":
                tabla_derecha[4][tabla_derecha[0].index(simbolo)] = "|1|"
                estado = "1"
            elif simbolo == "|a|":
                tabla_derecha[4][tabla_derecha[0].index(simbolo)] = "|3|"
                estado = "3"
            elif simbolo == "|*|":
                tabla_derecha[4][tabla_derecha[0].index(simbolo)] = "|4|"
                estado = "4"
        elif estado == "4":
            if simbolo == "|#|":
                tabla_derecha[5][tabla_derecha[0].index(simbolo)] = "|4|"
            elif simbolo == "|a|":
                tabla_derecha[5][tabla_derecha[0].index(simbolo)] = "|1|"
                estado = "1"
            elif simbolo == "|b|":
                tabla_derecha[5][tabla_derecha[0].index(simbolo)] = "|2|"
                estado = "2"

    print(f"Cadena {numero} (Dirección Derecha): {mensaje}")
    print("---Es válido---")
    print("Tabla de transiciones (Dirección Derecha):\n")
    for row in tabla_derecha:
        print(' '.join(row))
    
    return tabla_derecha

# Función para generar la tabla de transiciones en dirección izquierda
def generarTablaReversa(mensaje, numero):
    estado = '0'
    tabla_izquierda = [['|||', '|a|', '|b|', '|a|', '|*|', '|#|'], 
                       ['|0|', '-', '-', '-', '-', '-'],
                       ['|1|', '-', '-', '-', '-', '-'],
                       ['|2|', '-', '-', '-', '-', '-'],
                       ['|3|', '-', '-', '-', '-', '-'],
                       ['|4|', '-', '-', '-', '-', '-']]
    
    for i in reversed(mensaje):
        simbolo = f"|{i}|"
        if estado == "0":
            tabla_izquierda[1][tabla_izquierda[0].index(simbolo)] = "|1|"
            estado = '1' if simbolo == "|a|" else "0"
        elif estado == "1":
            tabla_izquierda[2][tabla_izquierda[0].index(simbolo)] = "|2|"
            estado = '2' if simbolo == "|b|" else "1"
        elif estado == "2":
            tabla_izquierda[3][tabla_izquierda[0].index(simbolo)] = "|3|"
            estado = '3'
        elif estado == "3":
            if simbolo == "|b|":
                tabla_izquierda[4][tabla_izquierda[0].index(simbolo)] = "|1|"
                estado = "1"
            elif simbolo == "|a|":
                tabla_izquierda[4][tabla_izquierda[0].index(simbolo)] = "|3|"
                estado = "3"
            elif simbolo == "|*|":
                tabla_izquierda[4][tabla_izquierda[0].index(simbolo)] = "|4|"
                estado = "4"
        elif estado == "4":
            if simbolo == "|#|":
                tabla_izquierda[5][tabla_izquierda[0].index(simbolo)] = "|4|"
            elif simbolo == "|a|":
                tabla_izquierda[5][tabla_izquierda[0].index(simbolo)] = "|1|"
                estado = "1"
            elif simbolo == "|b|":
                tabla_izquierda[5][tabla_izquierda[0].index(simbolo)] = "|2|"
                estado = "2"

    print(f"Cadena {numero} (Dirección Izquierda): {mensaje}")
    print("---Es válido---")
    print("Tabla de transiciones (Dirección Izquierda):\n")
    for row in tabla_izquierda:
        print(' '.join(row))
    
    return tabla_izquierda

# Función para obtener el siguiente estado según la tabla de transición
def obtener_siguiente_estado(estado_actual, caracter):
    tabla_transicion = {
        '0': {'a': '1'},
        '1': {'b': '2'},
        '2': {'a': '3'},
        '3': {'a': '3', 'b': '1', '*': '4'},
        '4': {'a': '3', 'b': '1', '#': '4'}
    }
    
    if estado_actual in tabla_transicion and caracter in tabla_transicion[estado_actual]:
        return tabla_transicion[estado_actual][caracter]  # Retorna el siguiente estado
    else:
        return '4'  # Estado de error

# Función para generar el árbol de derivación en formato PNG
def generar_arbol_derivacion(cadena, numero):
    dot = Digraph(comment=f'Árbol de Derivación - Cadena {numero}', format='png')
    dot.attr(rankdir='TB')
    
    estado_actual = '0'
    for i, caracter in enumerate(cadena):
        estado_siguiente = obtener_siguiente_estado(estado_actual, caracter)
        dot.node(f"{estado_actual}", estado_actual)
        dot.edge(f"{estado_actual}", estado_siguiente, label=caracter)
        estado_actual = estado_siguiente
    
    dot.node(f"{estado_actual}", estado_actual, shape='doublecircle')  # Estado final
    dot.render(f'arbol_derivacion_{numero}')

# Función principal
def main():
    try:
        with open('cadena.txt', 'r') as archivo:
            cadenas = archivo.readlines()
        
        for idx, cadena in enumerate(cadenas):
            cadena = cadena.strip()  # Quitar espacios y saltos de línea
            if cadena:  # Si la cadena no está vacía
                print(f'Procesando cadena: {cadena}')
                
                # Crear instancia de la máquina de Turing
                turing_machine = TuringMachine()
                turing_machine.load_tape(cadena)
                turing_machine.run()
                
                # Generar tabla de transiciones y árbol de derivación
                generarTabla(cadena, idx + 1)
                generarTablaReversa(cadena, idx + 1)
                generar_arbol_derivacion(cadena, idx + 1)
                
    except FileNotFoundError:
        print("Error: El archivo 'cadena.txt' no se encontró.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
