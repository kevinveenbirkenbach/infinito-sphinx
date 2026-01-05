import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def _add_src_to_path() -> None:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / "src").exists():
        root = root.parent
    sys.path.insert(0, str(root / "src"))


_add_src_to_path()

from infinito_docs.extensions.local_file_headings import add_local_file_headings  # noqa: E402


class _FakeApp:
    def __init__(self, srcdir: str) -> None:
        self.srcdir = srcdir


class TestLocalFileHeadings(unittest.TestCase):
    def test_add_local_file_headings_collects_headings(self) -> None:
        with TemporaryDirectory() as td:
            srcdir = Path(td)
            docs_dir = srcdir / "docs"
            docs_dir.mkdir(parents=True)

            # This file name simulates an "index" page
            (docs_dir / "index.rst").write_text("Index\n=====\n", encoding="utf-8")
            (docs_dir / "readme.md").write_text("# Readme\n", encoding="utf-8")
            (docs_dir / "a.md").write_text("# A\n## A1\n", encoding="utf-8")

            app = _FakeApp(str(srcdir))
            context: dict = {}

            # pagename 'docs/index' => directory 'docs'
            add_local_file_headings(app, "docs/index", "x", context, None)

            self.assertIn("local_md_headings", context)
            tree = context["local_md_headings"]
            self.assertTrue(isinstance(tree, list))
            # At least one heading should exist (from index.rst and a.md)
            flat_texts = []

            def _walk(items):
                for it in items:
                    flat_texts.append(it.get("text"))
                    _walk(it.get("children", []))

            _walk(tree)

            self.assertIn("Index", flat_texts)
            self.assertIn("A", flat_texts)
            self.assertIn("A1", flat_texts)

            # README should be excluded when index.rst exists
            self.assertNotIn("Readme", flat_texts)


if __name__ == "__main__":
    unittest.main()
