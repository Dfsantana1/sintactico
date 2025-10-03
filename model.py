"""Modelo del AST (Abstract Syntax Tree) y utilidades de visualización.

Este archivo define las clases que representan nodos del AST usados por el
parser. Cada nodo es un dataclass que contiene la información necesaria para
las etapas posteriores del compilador (análisis semántico, generación de
código, etc.). También se incluye una función `add_pretty_methods` que añade
un método `pretty()` a las clases para facilitar la visualización con
`rich.Tree`.

Las docstrings y comentarios están en español para que sea más sencillo
estudiar y mantener el código en contextos académicos o educativos.
"""

from dataclasses import dataclass, field
from multimethod import multimeta, multimethod
from typing      import List, Union

# =====================================================================
# Clases Abstractas
# =====================================================================
class Visitor(metaclass=multimeta):
    """Clase base para visitantes (patrón Visitor).

    Se utiliza como metaclase multimethod para permitir dispatch múltiple en
    visitantes si se implementan. Aquí no hay implementación concreta, sólo
    sirve como interfaz para los visitantes que procesen nodos del AST.
    """
    pass

@dataclass
class Node:
    """Nodo base del AST.

    Todos los nodos del AST heredan de esta clase. Proporciona un método
    `accept` que permite aplicar el patrón Visitor (si se implementa un
    visitante con método `visit`).
    """

    def accept(self, v: Visitor, *args, **kwargs):
        """Aceptar un visitante y delegar la operación.

        v: instancia de un visitante que implemente `visit`.
        """
        return v.visit(self, *args, **kwargs)

@dataclass
class Statement(Node):
    """Nodo base para declaraciones/estructuras de control.

    Sirve como padre lógico de todas las construcciones que representan
    sentencias o declaraciones en el lenguaje (declaraciones de variables,
    bloques, if, while, return, etc.).
    """
    pass

@dataclass
class Expression(Node):
    """Nodo base para expresiones.

    Incluye literales, operaciones binarias/unarias, llamadas a funciones y
    ubicaciones (variables y accesos a arreglos).
    """
    pass

# =====================================================================
# Definiciones
# =====================================================================
@dataclass
class Program(Statement):
    """Representa el programa raíz (lista de declaraciones).

    body: lista de sentencias/declaraciones que forman el programa.
    """

    body: List[Statement] = field(default_factory=list)

@dataclass
class Declaration(Statement):
    """Clase abstracta para declaraciones (variables, funciones, arreglos...).

    No contiene campos por sí misma; sirve para agrupar semánticamente las
    clases que representan declaraciones.
    """
    pass

@dataclass
class VarDecl(Declaration):
    """Declaración de variable simple.

    name: identificador (string)
    type: tipo declarado (otro nodo, p.ej. un literal que indique el tipo)
    value: expresión opcional con el valor inicial
    """

    name : str
    type : Expression
    value: Expression = None

'''
Statement
  |
  +-- Declaration (abstract)
  | |
  | +-- VarDecl: Guardar la información de una declaración de variable
  | |
  | +-- ArrayDecl: Declaración de Arreglos (multi-dimencioanles)
  | |
  | +-- FuncDecl: Para guardar información sobre las funciones declaradas

    -- VarParm
    -- ArrayParm

  -- IfStmt
  -- ReturnStmt
  |
  +-- PrintStmt
  |
  +-- ForStmt
  |
  +-- WhileStmt
  |
  +-- DoWhileStmt
  |
  +-- Assignment
'''
# Expresiones

@dataclass
@dataclass
class BinOper(Expression):
    """Operación binaria (p. ej. a + b, a && b, a < b).

    oper: símbolo del operador (string) como '+', '&&', '=='
    left, right: subexpresiones
    """

    oper : str
    left : Expression
    right: Expression

@dataclass
@dataclass
class UnaryOper(Expression):
    """Operación unaria (p. ej. -x, !x).

    oper: símbolo del operador unario
    expr: subexpresión sobre la que se aplica
    """

    oper : str
    expr : Expression

@dataclass
@dataclass
class Literal(Expression):
    """Nodo base para literales (integer, float, char, string, boolean).

    value: el valor literal (tipado en Python)
    type: nombre textual del tipo (se asigna en subclases)
    """

    value : Union[int, float, str, bool]
    type  : str = None

@dataclass
@dataclass
class Integer(Literal):
    """Literal entero.

    Valida en __post_init__ que el valor sea un int y marca el tipo.
    """

    value : int

    def __post_init__(self):
        assert isinstance(self.value, int), "Value debe ser un 'integer'"
        self.type = 'integer'

@dataclass
@dataclass
class Float(Literal):
    """Literal float (coma flotante).

    Valida que el valor sea float y asigna el tipo.
    """

    value : float

    def __post_init__(self):
        assert isinstance(self.value, float), "Value debe ser un 'float'"
        self.type = 'float'

@dataclass
@dataclass
class Boolean(Literal):
    """Literal booleano.

    value: True|False
    """

    value : bool

    def __post_init__(self):
        assert isinstance(self.value, bool), "Value debe ser un 'boolean'"
        self.type = 'boolean'

@dataclass
@dataclass
class Char(Literal):
    """Literal char (un solo carácter).

    Se asegura que el string tenga longitud 1.
    """

    value : str

    def __post_init__(self):
        assert isinstance(self.value, str) and len(self.value) == 1, "Value debe ser un 'char'"
        self.type = 'char'

@dataclass
@dataclass
class String(Literal):
    """Literal string.

    Contiene un string Python normal (sin comillas externas).
    """

    value : str

    def __post_init__(self):
        assert isinstance(self.value, str), "Value debe ser un 'string'"
        self.type = 'string'

# =====================================================================
# Operadores de Incremento/Decremento
# =====================================================================
@dataclass
class PreInc(Expression):
    """Incremento prefijo (++x).

    expr: subexpresión que será incrementada antes de evaluarse.
    """

    expr : Expression

@dataclass
class PreDec(Expression):
    """Decremento prefijo (--x)."""

    expr : Expression

@dataclass
class PostInc(Expression):
    """Incremento postfijo (x++)."""

    expr : Expression

@dataclass
class PostDec(Expression):
    """Decremento postfijo (x--)."""

    expr : Expression

# =====================================================================
# Declaraciones adicionales
# =====================================================================
@dataclass
class ArrayDecl(Declaration):
    """Declaración de arreglo (posible multi-dimensional).

    dimensions: lista de expresiones que indican las dimensiones (tamaños)
    value: opción para inicializar con una lista de expresiones
    """

    name : str
    type : Expression
    dimensions : List[Expression] = field(default_factory=list)
    value : Expression = None

@dataclass
class FuncDecl(Declaration):
    """Declaración de función.

    name: identificador de la función
    return_type: tipo de retorno (puede ser 'void')
    params: lista de parámetros (VarParm o ArrayParm)
    body: lista de sentencias que forman el cuerpo de la función
    """

    name : str
    return_type : Expression
    params : List[Declaration] = field(default_factory=list)
    body : List[Statement] = field(default_factory=list)

@dataclass
class VarParm(Declaration):
    """Parámetro por valor de función."""

    name : str
    type : Expression

@dataclass
class ArrayParm(Declaration):
    """Parámetro de tipo arreglo para funciones."""

    name : str
    type : Expression
    dimensions : List[Expression] = field(default_factory=list)

# =====================================================================
# Estructuras de control
# =====================================================================
@dataclass
class IfStmt(Statement):
    """Sentencia condicional if-then[-else].

    condition: expresión booleana
    then_stmt: sentencia o bloque a ejecutar si la condición es verdadera
    else_stmt: sentencia o bloque opcional para la rama else
    """

    condition : Expression
    then_stmt : Statement
    else_stmt : Statement = None

@dataclass
class WhileStmt(Statement):
    """Bucle while."""

    condition : Expression
    body : Statement

@dataclass
class DoWhileStmt(Statement):
    """Bucle do-while (ejecuta el cuerpo al menos una vez)."""

    body : Statement
    condition : Expression

@dataclass
class ForStmt(Statement):
    """Bucle for con inicialización, condición y actualización."""

    init : Statement
    condition : Expression
    update : Statement
    body : Statement

@dataclass
class ReturnStmt(Statement):
    """Sentencia return con expresión opcional."""

    expr : Expression = None

@dataclass
class PrintStmt(Statement):
    """Sentencia para imprimir el valor de una expresión."""

    expr : Expression

@dataclass
class Assignment(Statement):
    """Asignación a una ubicación (variable o índice de arreglo)."""

    location : Expression
    value : Expression

# =====================================================================
# Llamadas de función y ubicaciones
# =====================================================================
@dataclass
class FuncCall(Expression):
    """Llamada a función con argumentos opcionales."""

    name : str
    args : List[Expression] = field(default_factory=list)

@dataclass
class Location(Expression):
    """Nodo base para ubicaciones (variables y accesos a arreglos)."""
    pass

@dataclass
class VarLoc(Location):
    """Ubicación que referencia una variable por nombre."""

    name : str

@dataclass
class ArrayLoc(Location):
    """Ubicación que referencia un arreglo con una lista de índices."""

    name : str
    indices : List[Expression] = field(default_factory=list)

# =====================================================================
# Pretty printing con rich.Tree
# =====================================================================
from rich.tree import Tree

def add_pretty_methods():
    """Añade un método `pretty()` a las clases de nodo para visualización.

    El método `pretty()` construye un `rich.Tree` que representa el nodo y sus
    hijos recursivamente. Esto es útil para depuración y para mostrar el AST
    en consola de forma legible.
    """

    def pretty(self):
        """Construye un árbol `rich.Tree` representando este nodo.

        Recorre los atributos del objeto y, según su tipo, agrega subnodos o
        valores simples al árbol.
        """

        tree = Tree(f"[bold blue]{self.__class__.__name__}[/bold blue]")

        if hasattr(self, '__dict__'):
            for key, value in self.__dict__.items():
                # Si el atributo es otro Node, agregarlo recursivamente
                if isinstance(value, Node):
                    tree.add(f"[green]{key}:[/green]").add(value.pretty())
                # Si es una lista de nodos, agregar cada elemento
                elif isinstance(value, list):
                    if value and isinstance(value[0], Node):
                        for i, item in enumerate(value):
                            tree.add(f"[green]{key}[{i}]:[/green]").add(item.pretty())
                    else:
                        # Lista de valores simples
                        tree.add(f"[green]{key}:[/green] {value}")
                else:
                    # Valor primitivo (int, str, bool...)
                    tree.add(f"[green]{key}:[/green] {value}")

        return tree

    # Asignar el método pretty a las clases relevantes del AST
    for cls in [Program, Declaration, VarDecl, ArrayDecl, FuncDecl, VarParm, ArrayParm,
                Statement, IfStmt, WhileStmt, DoWhileStmt, ForStmt, ReturnStmt, PrintStmt, Assignment,
                Expression, BinOper, UnaryOper, Literal, Integer, Float, Boolean, Char, String,
                PreInc, PreDec, PostInc, PostDec, FuncCall, Location, VarLoc, ArrayLoc]:
        cls.pretty = pretty


# Inicializar los métodos para visualización
add_pretty_methods()