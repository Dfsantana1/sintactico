from dataclasses import dataclass, field
from multimethod import multimeta, multimethod
from typing      import List, Union

# =====================================================================
# Clases Abstractas
# =====================================================================
class Visitor(metaclass=multimeta):
    pass

@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

# =====================================================================
# Definiciones
# =====================================================================
@dataclass
class Program(Statement):
    body: List[Statement] = field(default_factory=list)

@dataclass
class Declaration(Statement):
    pass

@dataclass
class VarDecl(Declaration):
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
class BinOper(Expression):
    oper : str
    left : Expression
    right: Expression

@dataclass
class UnaryOper(Expression):
    oper : str
    expr : Expression

@dataclass
class Literal(Expression):
    value : Union[int, float, str, bool]
    type  : str = None

@dataclass
class Integer(Literal):
    value : int

    def __post_init__(self):
        assert isinstance(self.value, int), "Value debe ser un 'integer'"
        self.type = 'integer'

@dataclass
class Float(Literal):
    value : float

    def __post_init__(self):
        assert isinstance(self.value, float), "Value debe ser un 'float'"
        self.type = 'float'

@dataclass
class Boolean(Literal):
    value : bool

    def __post_init__(self):
        assert isinstance(self.value, bool), "Value debe ser un 'boolean'"
        self.type = 'boolean'

@dataclass
class Char(Literal):
    value : str

    def __post_init__(self):
        assert isinstance(self.value, str) and len(self.value) == 1, "Value debe ser un 'char'"
        self.type = 'char'

@dataclass
class String(Literal):
    value : str

    def __post_init__(self):
        assert isinstance(self.value, str), "Value debe ser un 'string'"
        self.type = 'string'

# =====================================================================
# Operadores de Incremento/Decremento
# =====================================================================
@dataclass
class PreInc(Expression):
    expr : Expression

@dataclass
class PreDec(Expression):
    expr : Expression

@dataclass
class PostInc(Expression):
    expr : Expression

@dataclass
class PostDec(Expression):
    expr : Expression

# =====================================================================
# Declaraciones adicionales
# =====================================================================
@dataclass
class ArrayDecl(Declaration):
    name : str
    type : Expression
    dimensions : List[Expression] = field(default_factory=list)
    value : Expression = None

@dataclass
class FuncDecl(Declaration):
    name : str
    return_type : Expression
    params : List[Declaration] = field(default_factory=list)
    body : List[Statement] = field(default_factory=list)

@dataclass
class VarParm(Declaration):
    name : str
    type : Expression

@dataclass
class ArrayParm(Declaration):
    name : str
    type : Expression
    dimensions : List[Expression] = field(default_factory=list)

# =====================================================================
# Estructuras de control
# =====================================================================
@dataclass
class IfStmt(Statement):
    condition : Expression
    then_stmt : Statement
    else_stmt : Statement = None

@dataclass
class WhileStmt(Statement):
    condition : Expression
    body : Statement

@dataclass
class DoWhileStmt(Statement):
    body : Statement
    condition : Expression

@dataclass
class ForStmt(Statement):
    init : Statement
    condition : Expression
    update : Statement
    body : Statement

@dataclass
class ReturnStmt(Statement):
    expr : Expression = None

@dataclass
class PrintStmt(Statement):
    expr : Expression

@dataclass
class Assignment(Statement):
    location : Expression
    value : Expression

# =====================================================================
# Llamadas de función y ubicaciones
# =====================================================================
@dataclass
class FuncCall(Expression):
    name : str
    args : List[Expression] = field(default_factory=list)

@dataclass
class Location(Expression):
    pass

@dataclass
class VarLoc(Location):
    name : str

@dataclass
class ArrayLoc(Location):
    name : str
    indices : List[Expression] = field(default_factory=list)

# =====================================================================
# Pretty printing con rich.Tree
# =====================================================================
from rich.tree import Tree

def add_pretty_methods():
    """Add pretty() method to all Node classes for rich.Tree visualization"""
    
    def pretty(self):
        tree = Tree(f"[bold blue]{self.__class__.__name__}[/bold blue]")
        
        if hasattr(self, '__dict__'):
            for key, value in self.__dict__.items():
                if isinstance(value, Node):
                    tree.add(f"[green]{key}:[/green]").add(value.pretty())
                elif isinstance(value, list):
                    if value and isinstance(value[0], Node):
                        for i, item in enumerate(value):
                            tree.add(f"[green]{key}[{i}]:[/green]").add(item.pretty())
                    else:
                        tree.add(f"[green]{key}:[/green] {value}")
                else:
                    tree.add(f"[green]{key}:[/green] {value}")
        
        return tree
    
    # Add pretty method to all Node classes
    for cls in [Program, Declaration, VarDecl, ArrayDecl, FuncDecl, VarParm, ArrayParm,
                Statement, IfStmt, WhileStmt, DoWhileStmt, ForStmt, ReturnStmt, PrintStmt, Assignment,
                Expression, BinOper, UnaryOper, Literal, Integer, Float, Boolean, Char, String,
                PreInc, PreDec, PostInc, PostDec, FuncCall, Location, VarLoc, ArrayLoc]:
        cls.pretty = pretty

# Initialize pretty printing methods
add_pretty_methods()