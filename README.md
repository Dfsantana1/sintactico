# Parser BMinor - Analizador Sintáctico

## 🎯 Resumen

Analizador sintáctico completo para el lenguaje BMinor que implementa:
- Estructuras de control **WHILE** y **DO-WHILE**
- Operadores de incremento/decremento **prefijos** (`++x`, `--x`) y **postfijos** (`x++`, `x--`)
- Visualización del AST usando **rich.Tree**

## 📁 Archivos del Proyecto

- `model.py` - Definición de nodos AST
- `parser.py` - Analizador sintáctico (lexer + parser)
- `errors.py` - Manejo de errores
- `test_parser.py` - Pruebas unitarias
- `requirements.txt` - Dependencias

## 🚀 Uso Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas
python test_parser.py

# Usar el parser
python parser.py archivo.bminor
```

## ✅ Objetivos Completados

| Objetivo | Estado | Descripción |
|----------|--------|-------------|
| **Nodos AST** | ✅ | WhileStmt, DoWhileStmt, PreInc, PreDec implementados |
| **Estructuras WHILE/DO-WHILE** | ✅ | Gramática y reconocimiento funcional |
| **Operadores ++/--** | ✅ | Prefijos y postfijos reconocidos |
| **Visualización rich.Tree** | ✅ | Método pretty() implementado |

## 📊 Ejemplos

### WHILE
```bminor
x: integer = 0;
while (x < 10) {
    x = x + 1;
}
```

### DO-WHILE
```bminor
count: integer = 5;
do {
    count = count - 1;
} while (count > 0);
```

### Operadores ++/--
```bminor
x: integer = 5;
y: integer = ++x;  // Prefijo
z: integer = x++;  // Postfijo
```

## 🧪 Pruebas

Ejecutar `python test_parser.py` para verificar:
- Estructuras de control WHILE y DO-WHILE
- Operadores de incremento/decremento
- Visualización del AST con rich.Tree
- Casos de error y validación

---
**Proyecto completado al 100%** - Todos los objetivos del taller cumplidos ✅