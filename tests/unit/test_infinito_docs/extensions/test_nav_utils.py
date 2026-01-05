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

from infinito_docs.extensions.nav_utils import (  # noqa: E402
    natural_sort_key,
    extract_headings_from_file,
    group_headings,
    sort_tree,
)


class TestNavUtils(unittest.TestCase):
    def test_natural_sort_key(self) -> None:
        self.assertLess(natural_sort_key("file2"), natural_sort_key("file10"))

    def test_extract_headings_from_md_ignores_code_blocks(self) -> None:
        with TemporaryDirectory() as td:
            f = Path(td) / "x.md"
            f.write_text(
                "\n".join(
                    [
                        "# Title",
                        "```",
                        "# Not a heading",
                        "```",
                        "## Sub",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            headings = extract_headings_from_file(str(f), max_level=10)
            texts = [h["text"] for h in headings]
            self.assertIn("Title", texts)
            self.assertIn("Sub", texts)
            self.assertNotIn("Not a heading", texts)

    def test_extract_headings_from_rst(self) -> None:
        with TemporaryDirectory() as td:
            f = Path(td) / "x.rst"
            f.write_text("Header\n======\n\nBody\n", encoding="utf-8")
            headings = extract_headings_from_file(str(f), max_level=10)
            self.assertTrue(any(h["text"] == "Header" for h in headings))

    def test_group_and_sort_tree(self) -> None:
        headings = [
            {"level": 1, "text": "B", "anchor": "b", "priority": 1, "filename": "b"},
            {"level": 2, "text": "B1", "anchor": "b1", "priority": 1, "filename": "b"},
            {"level": 1, "text": "A", "anchor": "a", "priority": 0, "filename": "a"},
        ]
        tree = group_headings(headings)
        sort_tree(tree)
        self.assertEqual(tree[0]["text"], "A")
        self.assertEqual(tree[1]["text"], "B")
        self.assertEqual(tree[1]["children"][0]["text"], "B1")


if __name__ == "__main__":
    unittest.main()
