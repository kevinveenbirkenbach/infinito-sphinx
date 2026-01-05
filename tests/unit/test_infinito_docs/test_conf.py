import importlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


def _add_src_to_path() -> None:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / "src").exists():
        root = root.parent
    sys.path.insert(0, str(root / "src"))


_add_src_to_path()


class TestSphinxConf(unittest.TestCase):
    def test_conf_import_and_key_settings(self) -> None:
        with patch.object(sys, "argv", ["sphinx-build"]):
            conf = importlib.import_module("infinito_docs.conf")

        self.assertIn("myst_parser", conf.extensions)
        self.assertIn("sphinx.ext.autodoc", conf.extensions)
        self.assertEqual(conf.html_theme, "sphinxawesome_theme")

        self.assertIn(".md", conf.source_suffix)
        self.assertIn(".rst", conf.source_suffix)
        self.assertIn(".yaml", conf.source_suffix)
        self.assertIn(".yml", conf.source_suffix)

        self.assertTrue(hasattr(conf, "templates_path"))
        self.assertTrue(hasattr(conf, "html_static_path"))


if __name__ == "__main__":
    unittest.main()
