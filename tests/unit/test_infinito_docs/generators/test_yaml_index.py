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

from infinito_docs.generators.yaml_index import generate_yaml_index  # noqa: E402


class TestYamlIndexGenerator(unittest.TestCase):
    def test_generate_yaml_index_respects_gitignore(self) -> None:
        with TemporaryDirectory() as td:
            src = Path(td) / "repo"
            src.mkdir(parents=True)

            (src / ".gitignore").write_text("ignored.yml\n", encoding="utf-8")
            (src / "ok.yaml").write_text("a: 1\n", encoding="utf-8")
            (src / "ignored.yml").write_text("b: 2\n", encoding="utf-8")

            out_dir = Path(td) / "out"
            out_file = out_dir / "yaml_index.rst"

            generate_yaml_index(str(src), str(out_file))

            text = out_file.read_text(encoding="utf-8")
            self.assertIn(".. literalinclude::", text)
            self.assertIn("ok.yaml", text)
            self.assertNotIn("ignored.yml", text)


if __name__ == "__main__":
    unittest.main()
