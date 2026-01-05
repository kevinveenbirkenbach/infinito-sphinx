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

from infinito_docs.generators.index import generate_ansible_roles_index  # noqa: E402


class TestIndexGenerator(unittest.TestCase):
    def test_generate_index_lists_rst_files(self) -> None:
        with TemporaryDirectory() as td:
            roles_dir = Path(td) / "generated_roles"
            roles_dir.mkdir(parents=True)
            (roles_dir / "b.rst").write_text("b", encoding="utf-8")
            (roles_dir / "a.rst").write_text("a", encoding="utf-8")

            out_file = Path(td) / "roles" / "ansible_role_glosar.rst"

            generate_ansible_roles_index(str(roles_dir), str(out_file), "Ansible Role Glossary")

            text = out_file.read_text(encoding="utf-8")
            self.assertIn(".. toctree::", text)
            self.assertIn("Ansible Role Glossary", text)
            self.assertIn("generated_roles/a", text)
            self.assertIn("generated_roles/b", text)


if __name__ == "__main__":
    unittest.main()
