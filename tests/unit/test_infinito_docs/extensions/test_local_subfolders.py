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

from infinito_docs.extensions.local_subfolders import collect_folder_tree, mark_current  # noqa: E402


class TestLocalSubfolders(unittest.TestCase):
    def test_collect_folder_tree_builds_tree(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td) / "root"
            root.mkdir(parents=True)

            (root / "index.rst").write_text("Root\n====\n", encoding="utf-8")
            (root / "a.md").write_text("# A\n", encoding="utf-8")

            sub = root / "sub"
            sub.mkdir()
            (sub / "readme.md").write_text("# Sub\n", encoding="utf-8")
            (sub / "x.rst").write_text("X\n=\n", encoding="utf-8")

            tree = collect_folder_tree(str(root), "")
            self.assertIsNotNone(tree)
            self.assertEqual(tree["text"], "Root")
            self.assertTrue(any(c.get("text") == "A" for c in tree["children"]))
            self.assertTrue(any(c.get("text") == "Sub" for c in tree["children"]))

    def test_mark_current_propagates(self) -> None:
        node = {
            "text": "Root",
            "link": "index",
            "children": [
                {"text": "Child", "link": "child/index", "children": []},
            ],
        }
        mark_current(node, "child/index")
        self.assertTrue(node["current"])
        self.assertTrue(node["children"][0]["current"])


if __name__ == "__main__":
    unittest.main()
