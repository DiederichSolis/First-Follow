class GrammarAnalyzer:
    def __init__(self, grammar, start_symbol):
        """
        Inicializa el analizador con la gramática y el símbolo inicial.
        """
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.non_terminals = set(grammar.keys())
        self.terminals = self._find_terminals()
        self.first_sets = {}
        self.follow_sets = {}
        
    def _find_terminals(self):
        """Encuentra todos los terminales en la gramática."""
        terminals = set()
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol not in self.non_terminals and symbol != 'ε':
                        terminals.add(symbol)
        return terminals
    
    def compute_first(self):
        """Calcula los conjuntos FIRST para todos los no terminales."""
        # Inicializar FIRST para cada no terminal como conjunto vacío
        self.first_sets = {nt: set() for nt in self.non_terminals}
        
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    # Caso 1: X -> ε
                    if production == ['ε']:
                        if 'ε' not in self.first_sets[nt]:
                            self.first_sets[nt].add('ε')
                            changed = True
                        continue
                    
                    # Para cada símbolo en la producción
                    all_epsilon = True
                    for symbol in production:
                        # Caso 2: X es terminal
                        if symbol in self.terminals:
                            if symbol not in self.first_sets[nt]:
                                self.first_sets[nt].add(symbol)
                                changed = True
                            all_epsilon = False
                            break
                        
                        # Caso 3: X es no terminal
                        elif symbol in self.non_terminals:
                            # Añadir FIRST(Y1) - {ε} a FIRST(X)
                            before_len = len(self.first_sets[nt])
                            self.first_sets[nt].update(self.first_sets[symbol] - {'ε'})
                            if len(self.first_sets[nt]) > before_len:
                                changed = True
                            
                            # Si ε no está en FIRST(Y1), terminar
                            if 'ε' not in self.first_sets[symbol]:
                                all_epsilon = False
                                break
                    
                    # Si todos los símbolos pueden derivar ε, añadir ε a FIRST(X)
                    if all_epsilon:
                        if 'ε' not in self.first_sets[nt]:
                            self.first_sets[nt].add('ε')
                            changed = True
        
        return self.first_sets

    
    def compute_follow(self):
        """Calcula los conjuntos FOLLOW para todos los no terminales."""
        if not self.first_sets:
            self.compute_first()
            
        # Inicializar FOLLOW para cada no terminal como conjunto vacío
        self.follow_sets = {nt: set() for nt in self.non_terminals}
        # Regla 1: $ está en FOLLOW(S)
        self.follow_sets[self.start_symbol].add('$')
        
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.grammar[nt]:
                    # Para cada no terminal en la producción
                    for i in range(len(production)):
                        B = production[i]
                        if B not in self.non_terminals:
                            continue
                        
                        # Regla 2: A → αBβ
                        if i < len(production) - 1:
                            beta = production[i+1:]
                            first_beta = self._compute_first_for_sequence(beta)
                            
                            # Añadir FIRST(β) - {ε} a FOLLOW(B)
                            before_len = len(self.follow_sets[B])
                            self.follow_sets[B].update(first_beta - {'ε'})
                            if len(self.follow_sets[B]) > before_len:
                                changed = True
                            
                            # Regla 3: Si ε está en FIRST(β), añadir FOLLOW(A) a FOLLOW(B)
                            if 'ε' in first_beta:
                                before_len = len(self.follow_sets[B])
                                self.follow_sets[B].update(self.follow_sets[nt])
                                if len(self.follow_sets[B]) > before_len:
                                    changed = True
                        else:
                            # Regla 3: A → αB (caso donde β es ε)
                            before_len = len(self.follow_sets[B])
                            self.follow_sets[B].update(self.follow_sets[nt])
                            if len(self.follow_sets[B]) > before_len:
                                changed = True
        
        return self.follow_sets
    
    def _compute_first_for_sequence(self, sequence):
        """Calcula FIRST para una secuencia de símbolos."""
        first = set()
        all_epsilon = True
        
        for symbol in sequence:
            if symbol in self.terminals:
                first.add(symbol)
                all_epsilon = False
                break
            elif symbol in self.non_terminals:
                first.update(self.first_sets[symbol] - {'ε'})
                if 'ε' not in self.first_sets[symbol]:
                    all_epsilon = False
                    break
        
        if all_epsilon:
            first.add('ε')
            
        return first
    
    def get_results_as_string(self):
        """Devuelve los resultados como una cadena formateada."""
        result = "Conjuntos FIRST:\n"
        for nt in sorted(self.first_sets.keys()):
            result += f"FIRST({nt}) = {sorted(self.first_sets[nt])}\n"
        
        result += "\nConjuntos FOLLOW:\n"
        for nt in sorted(self.follow_sets.keys()):
            result += f"FOLLOW({nt}) = {sorted(self.follow_sets[nt])}\n"
        
        return result
def read_grammar_from_file(filename):
    """
    Lee una gramática desde un archivo de texto.
    """
    grammar = {}
    start_symbol = None
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        if not lines:
            raise ValueError("El archivo está vacío")
        
        # Primera línea es el símbolo inicial
        start_symbol = lines[0].strip()
        
        for line in lines[1:]:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Saltar líneas vacías o comentarios
            
            if '->' not in line:
                raise ValueError(f"Línea mal formada: {line}")
            
            # Dividir izquierda y derecha
            left, right = line.split('->', 1)
            left = left.strip()
            
            # Dividir las producciones
            productions = [prod.strip() for prod in right.split('|')]
            
            # Procesar cada producción
            grammar[left] = []
            for prod in productions:
                if prod == 'ε':
                    grammar[left].append(['ε'])
                else:
                    # Dividir los símbolos (asumiendo que están separados por espacios)
                    symbols = prod.split()
                    grammar[left].append(symbols)
    
    return grammar, start_symbol


def write_results_to_file(filename, content):
    """Escribe el contenido en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def process_grammar(input_file, output_file):
    """
    Procesa una gramática desde un archivo de entrada y escribe los resultados en un archivo de salida.
    """
    try:
        # Leer gramática
        grammar, start_symbol = read_grammar_from_file(input_file)
        
        # Analizar gramática
        analyzer = GrammarAnalyzer(grammar, start_symbol)
        analyzer.compute_first()
        analyzer.compute_follow()
        
        # Obtener resultados
        results = analyzer.get_results_as_string()
        
        # Escribir resultados
        write_results_to_file(output_file, results)
        print(f"Análisis completado. Resultados escritos en {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
   
    input_filename = "gramatica.txt"  
    output_filename = "resultados.txt"  
    
    process_grammar(input_file=input_filename, output_file=output_filename)