#!/usr/bin/env python3
"""
Pruebas para el parser de BMinor
Demuestra casos con while, do-while, ++x, --x
"""

from parser import parse_string
from rich import print
from rich.console import Console

console = Console()

def test_while_simple():
    """Prueba simple de WHILE"""
    console.print("\n[bold blue]=== Prueba: WHILE simple ===[/bold blue]")
    
    source = """
    x: integer = 0;
    while (x < 10) {
        x = x + 1;
    }
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para WHILE")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de WHILE")

def test_do_while_simple():
    """Prueba simple de DO-WHILE"""
    console.print("\n[bold blue]=== Prueba: DO-WHILE simple ===[/bold blue]")
    
    source = """
    x: integer = 0;
    do {
        x = x + 1;
    } while (x < 10);
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para DO-WHILE")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de DO-WHILE")

def test_prefix_increment_simple():
    """Prueba simple de incremento prefijo"""
    console.print("\n[bold blue]=== Prueba: ++ prefijo simple ===[/bold blue]")
    
    source = """
    x: integer = 5;
    y: integer = ++x;
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para ++ prefijo")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de ++ prefijo")

def test_postfix_increment_simple():
    """Prueba simple de incremento postfijo"""
    console.print("\n[bold blue]=== Prueba: ++ postfijo simple ===[/bold blue]")
    
    source = """
    x: integer = 5;
    y: integer = x++;
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para ++ postfijo")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de ++ postfijo")

def test_prefix_decrement_simple():
    """Prueba simple de decremento prefijo"""
    console.print("\n[bold blue]=== Prueba: -- prefijo simple ===[/bold blue]")
    
    source = """
    x: integer = 5;
    y: integer = --x;
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para -- prefijo")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de -- prefijo")

def test_postfix_decrement_simple():
    """Prueba simple de decremento postfijo"""
    console.print("\n[bold blue]=== Prueba: -- postfijo simple ===[/bold blue]")
    
    source = """
    x: integer = 5;
    y: integer = x--;
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para -- postfijo")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de -- postfijo")

def test_complex_while():
    """Prueba WHILE con operadores de incremento"""
    console.print("\n[bold blue]=== Prueba: WHILE con ++ ===[/bold blue]")
    
    source = """
    i: integer = 0;
    sum: integer = 0;
    while (i < 10) {
        sum = sum + i;
        i = ++i;
    }
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para WHILE con ++")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de WHILE con ++")

def test_complex_do_while():
    """Prueba DO-WHILE con operadores de decremento"""
    console.print("\n[bold blue]=== Prueba: DO-WHILE con -- ===[/bold blue]")
    
    source = """
    count: integer = 10;
    do {
        count = count - 1;
        count = --count;
    } while (count > 0);
    """
    
    ast = parse_string(source)
    if ast:
        console.print("✓ Parsing exitoso para DO-WHILE con --")
        console.print(ast.pretty())
    else:
        console.print("✗ Error en parsing de DO-WHILE con --")

def run_all_tests():
    """Ejecuta todas las pruebas simples"""
    console.print("[bold green]Iniciando pruebas simples del parser BMinor...[/bold green]")
    
    test_while_simple()
    test_do_while_simple()
    test_prefix_increment_simple()
    test_postfix_increment_simple()
    test_prefix_decrement_simple()
    test_postfix_decrement_simple()
    test_complex_while()
    test_complex_do_while()
    
    console.print("\n[bold green]Pruebas simples completadas![/bold green]")

if __name__ == "__main__":
    run_all_tests()
