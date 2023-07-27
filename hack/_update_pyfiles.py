import ast
from pathlib import Path
from typing import Callable, NamedTuple


class ParsedFile(NamedTuple):
    source: str
    parsed: ast.Module


def update_pyfile(
    our_path: Path,
    their_path: Path,
    how_to_update: Callable[[ParsedFile, ParsedFile], str],
) -> None:
    our_source = our_path.read_text()
    their_source = their_path.read_text()

    our_module = ast.parse(our_source, str(our_path))
    their_module = ast.parse(their_source, str(their_path))

    updated_source = how_to_update(
        ParsedFile(our_source, our_module),
        ParsedFile(their_source, their_module),
    )

    if not updated_source.endswith("\n"):
        updated_source += "\n"

    our_path.write_text(updated_source)


def update_toplevel(our_file: ParsedFile, their_file: ParsedFile) -> str:
    our_defs = _get_top_level_defs(our_file.parsed)
    their_defs = _get_top_level_defs(their_file.parsed)

    updated_source = our_file.source

    def replace_def(updated_src: str, our_def: ast.stmt, their_def: ast.stmt) -> str:
        our_src_segment = ast.get_source_segment(our_file.source, our_def)
        their_src_segment = ast.get_source_segment(their_file.source, their_def)
        assert our_src_segment and their_src_segment
        return updated_src.replace(our_src_segment, their_src_segment, 1)

    for def_name, our_def in our_defs.items():
        their_def = their_defs[def_name]
        updated_source = replace_def(updated_source, our_def, their_def)

    return updated_source


def _get_top_level_defs(module: ast.Module) -> dict[str, ast.stmt]:
    defs: dict[str, ast.stmt] = {}
    n_docstrings = 0

    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defs[node.name] = node
        # top-level variables (constants)
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            defs[node.targets[0].id] = node
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            n_docstrings += 1
            defs[f"__docstring_{n_docstrings}__"] = node

    return defs


def update_all_but_imports(our_file: ParsedFile, their_file: ParsedFile) -> str:
    def find_last_import(module: ast.Module) -> ast.stmt:
        *_, last_import = (
            node
            for node in module.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        )
        return last_import

    our_last_import = find_last_import(our_file.parsed)
    their_last_import = find_last_import(their_file.parsed)

    def endline(node: ast.stmt) -> int:
        return node.end_lineno or node.lineno

    our_imports = our_file.source.splitlines()[: endline(our_last_import)]
    their_code = their_file.source.splitlines()[endline(their_last_import) :]

    return "\n".join(our_imports + their_code)


FileToUpdate = tuple[str, str, Callable[[ParsedFile, ParsedFile], str]]


update_matrix: list[FileToUpdate] = [
    (
        "gemlock_parser/analysis.py",
        "scancode-toolkit/src/textcode/analysis.py",
        update_toplevel,
    ),
    (
        "gemlock_parser/strings.py",
        "scancode-toolkit/src/textcode/strings.py",
        update_toplevel,
    ),
    (
        "gemlock_parser/tokenize.py",
        "scancode-toolkit/src/licensedcode/tokenize.py",
        update_toplevel,
    ),
    (
        "gemlock_parser/gemfile_lock.py",
        "scancode-toolkit/src/packagedcode/gemfile_lock.py",
        update_all_but_imports,
    ),
    (
        "tests/test_gemfile_lock.py",
        "scancode-toolkit/tests/packagedcode/test_gemfile_lock.py",
        update_all_but_imports,
    ),
    (
        "tests/scancode_config.py",
        "scancode-toolkit/src/scancode_config.py",
        update_toplevel,
    ),
]


def main() -> None:
    for our_path, their_path, how_to_update in update_matrix:
        update_pyfile(Path(our_path), Path(their_path), how_to_update)
        print(our_path)


if __name__ == "__main__":
    main()
