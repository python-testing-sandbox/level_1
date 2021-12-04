import ast

import pytest

import code


def test_extract_all_constants_from_ast():
    func = """
def func_with_strings():
    s1 = "A"
    s2 = "B"
    if s2 == f"C":
        return ",".join(s1)
    else:
        return s1
    """
    ast_tree = ast.parse(func)
    assert set(code.extract_all_constants_from_ast(ast_tree)) == {'A', 'B', 'C', ','}


def test_rec():
    fibonacci = """
def fibonacci(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
fibonacci(5)
    """
    ast_tree = ast.parse(fibonacci)
    for node in ast.walk(ast_tree):
        if type(node) == ast.FunctionDef:
            assert code.has_recursive_calls(node)
