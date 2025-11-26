import os
import io
import runpy
import ast
import unittest
from unittest import mock


def load_is_valid_change_from_file(path):
    """Extract `is_valid_change` function from source file using AST and return the callable.

    This avoids importing the whole script (which runs interactive code at module import).
    """
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src, filename=path)
    func_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "is_valid_change":
            func_node = node
            break
    if func_node is None:
        raise RuntimeError("is_valid_change not found in file")
    module = ast.Module(body=[func_node], type_ignores=[])
    ast.fix_missing_locations(module)
    code = compile(module, path, "exec")
    ns = {}
    exec(code, ns)
    return ns["is_valid_change"]


class TestWordChanger(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "word_changer_game.py")

    def test_is_valid_change_cases(self):
        is_valid_change = load_is_valid_change_from_file(self.path)

        # same length, one letter different
        self.assertTrue(is_valid_change("cat", "cot"))
        # same length, zero letters different
        self.assertFalse(is_valid_change("cat", "cat"))
        # same length, two letters different
        self.assertFalse(is_valid_change("cat", "dog"))
        # different lengths
        self.assertFalse(is_valid_change("cat", "cats"))
        self.assertFalse(is_valid_change("", "a"))

    def test_full_game_flow_completes(self):
        # Provide inputs to complete a small game: length=3, start=cat, goal=dog,
        # moves: cot -> dot -> dog
        inputs = [
            "3",    # word_length
            "cat",  # start_word
            "dog",  # goal_word
            "cot",  # change 1
            "dot",  # change 2
            "dog",  # final change
        ]

        def fake_input(prompt=""):
            try:
                return inputs.pop(0)
            except IndexError:
                raise EOFError("No more input provided")

        # Capture stdout while running the script
        buf = io.StringIO()
        with mock.patch("builtins.input", side_effect=fake_input):
            with mock.patch("sys.stdout", new=buf):
                # runpy.run_path executes the script in a fresh namespace
                runpy.run_path(self.path, run_name="__main__")

        output = buf.getvalue()
        # Check that the final congratulatory message appears with start and goal words
        self.assertIn("Congratulations! You turned 'cat' into 'dog'!", output)


if __name__ == "__main__":
    unittest.main()
