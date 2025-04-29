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
     