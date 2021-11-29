import ast
import code


func = '''
def func_with_strings():
    s1 = "A"
    s2 = "B"
    if s2 == f"C":
        return ",".join(s1)
    else:
        return s1
'''


def test_extract_all_constants_from_ast():
    ast_tree = ast.parse(func)
    assert set(code.extract_all_constants_from_ast(ast_tree)) == {'A', 'B', 'C', ','}
