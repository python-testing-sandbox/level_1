import ast
import os


def read_test_file(filename):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_files",
        filename,
    )
    with open(test_file_path, "r") as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    return tree
