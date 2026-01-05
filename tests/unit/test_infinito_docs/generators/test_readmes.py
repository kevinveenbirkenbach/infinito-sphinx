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

from infinito_docs.generators.readmes import create_readme_in_subdirs  # noqa: E402


class TestReadmesGenerator(unittest.TestCase):
    def test_create_readme_in_subdirs_creates_files(self) -> None:
        with TemporaryDirectory() as td:
            gen = Path(td) / "generated"
            (gen / "a").mkdir(parents=True)
            (gen / "b" / "c").mkdir(parents=True)

            create_readme_in_subdirs(str(gen))

            self.assertTrue((gen / "a" / "README.md").exists())
            self.assertTrue((gen / "b" / "README.md").exists())
            self.assertTrue((gen / "b" / "c" / "README.md").exists())

            content = (gen / "a" / "README.md").read_text(encoding="utf-8")
            self.assertIn("Auto Generated Technical Documentation", content)


if __name__ == "__main__":
    unittest.main()
