import ast
import datetime
import io
import re
from typing import Iterable, Any, Optional, Generator

from PIL import Image
from requests import get
from requests.exceptions import MissingSchema


def chunks(some_list: list, chunk_size: int) -> Generator:
    for chunk_num in range(0, len(some_list), chunk_size):
        yield some_list[chunk_num:chunk_num + chunk_size]


def flat(some_list: list[list]) -> list:
    return [item for sublist in some_list for item in sublist]


def has_recursive_calls(funcdef) -> bool:
    return bool([
        n for n in ast.walk(funcdef)
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name)
            and n.func.id == funcdef.name
        )
    ])


def parse_iso_datetime(iso_datetime: str) -> Optional[datetime.datetime]:
    if iso_datetime.endswith('Z'):
        iso_datetime = iso_datetime[:-1]
    try:
        return datetime.datetime.fromisoformat(iso_datetime)
    except ValueError:
        return None


def get_image_height_in_pixels(url: str) -> Optional[int]:
    try:
        img_data = get(url).content
    except MissingSchema:
        return None
    im = Image.open(io.BytesIO(img_data))
    return im.size[1]


def if_logs_has_any_of_commands(log: list[str], commands: list[str]) -> bool:
    is_section_present = False
    for required_command in commands:
        for base_command in log:
            if (
                base_command.startswith(f'{required_command} ')
                or f' {required_command} ' in base_command
                or base_command == required_command
            ):
                is_section_present = True
                break
    return is_section_present


def extract_all_constants_from_ast(ast_tree: ast.AST) -> list[str]:
    return list({n.s for n in ast.walk(ast_tree) if isinstance(n, ast.Str)})


def is_camel_case_word(word: str) -> bool:
    uppercase_letters_amount = re.subn(r'[A-Z]', '', word)[1]
    lowercase_letters_amount = re.subn(r'[a-z]', '', word)[1]
    return bool(
        (lowercase_letters_amount and uppercase_letters_amount >= 2)
        or re.findall(r'[a-z][A-Z]', word),
    )


def split_camel_case_words(camel_cased_word: str) -> list[str]:
    words_start_indexes = [m.start(0) for m in re.finditer(r'[A-Z]', camel_cased_word)]
    if words_start_indexes[0] > 0:
        words_start_indexes.insert(0, 0)
    if words_start_indexes[-1] < len(camel_cased_word):
        words_start_indexes.append(len(camel_cased_word))
    words = []
    for word_start_index, word_end_index in zip(words_start_indexes, words_start_indexes[1:]):
        words.append(camel_cased_word[word_start_index:word_end_index].lower())
    return words


def is_path_in_exclude_list(path: str, exclude: list[str]) -> bool:
    return any(e in path for e in exclude)


def get_full_class_name(obj: Any) -> str:
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__


def max_with_default(items: Iterable, default: Optional = None):
    default = default or 0
    items = list(items)
    if not items and default is not None:
        return default
    return max(items)


def is_python_class_name(name: str) -> bool:
    return name[0] == name[0].upper() and name[1:] == name[1:].lower()

