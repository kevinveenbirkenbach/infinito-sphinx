import sys
import unittest
from pathlib import Path


def _add_src_to_path() -> None:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / "src").exists():
        root = root.parent
    sys.path.insert(0, str(root / "src"))


_add_src_to_path()


class TestPackageInit(unittest.TestCase):
    def test_import_package(self) -> None:
        import infinito_docs  # noqa: F401


if __name__ == "__main__":
    unittest.main()
