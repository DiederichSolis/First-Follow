# Análisis de Conjuntos FIRST y FOLLOW

Este repositorio contiene una implementación en Python del análisis sintáctico para obtener los conjuntos **FIRST** y **FOLLOW** de una gramática libre de contexto.

## 📁 Archivos

- `First-Follow.py`: Script principal en Python que procesa una gramática y genera los conjuntos FIRST y FOLLOW.
- `gramatica.txt`: Contiene la definición de la gramática usada para el análisis.
- `resultados.txt`: Salida del programa con los conjuntos FIRST y FOLLOW calculados.

## 📚 Gramática usada

```txt
S -> a B D h  
B -> c C  
C -> b C | ε  
D -> E F  
E -> g | ε  
F -> f | ε  
```
🧠 Funcionamiento del algoritmo
  - El script analiza producciones de la forma A -> α desde un archivo de texto.

  - Calcula los conjuntos FIRST usando reglas de derivación anticipada.

  - Calcula los conjuntos FOLLOW tomando en cuenta posiciones relativas de los símbolos no terminales en las producciones.
