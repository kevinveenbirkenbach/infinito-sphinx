import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch


def _add_src_to_path() -> None:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / "src").exists():
        root = root.parent
    sys.path.insert(0, str(root / "src"))


_add_src_to_path()

from infinito_docs.generators.ansible_roles import (  # noqa: E402
    convert_md_to_rst,
    generate_ansible_roles_doc,
)


class TestAnsibleRolesGenerator(unittest.TestCase):
    @patch("infinito_docs.generators.ansible_roles.subprocess.run")
    def test_convert_md_to_rst_success(self, run: MagicMock) -> None:
        run.return_value = MagicMock(stdout=b"RST\n", returncode=0)
        out = convert_md_to_rst("# Title\n")
        self.assertEqual(out, "RST\n")

    @patch("infinito_docs.generators.ansible_roles.subprocess.run")
    def test_convert_md_to_rst_fallback_on_error(self, run: MagicMock) -> None:
        from subprocess import CalledProcessError

        run.side_effect = CalledProcessError(1, ["pandoc"])
        md = "# Title\n"
        out = convert_md_to_rst(md)
        self.assertEqual(out, md)

    @patch("infinito_docs.generators.ansible_roles.subprocess.run")
    def test_generate_ansible_roles_doc_writes_rst(self, run: MagicMock) -> None:
        run.return_value = MagicMock(stdout=b"Converted README\n", returncode=0)

        with TemporaryDirectory() as td:
            roles_dir = Path(td) / "roles"
            out_dir = Path(td) / "out"
            role = roles_dir / "web-app-demo"
            (role / "meta").mkdir(parents=True)

            (role / "meta" / "main.yml").write_text(
                "\n".join(
                    [
                        "galaxy_info:",
                        "  description: Demo role",
                        "  galaxy_tags:",
                        "    - demo",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (role / "README.md").write_text("# Demo\n\nHello\n", encoding="utf-8")

            generate_ansible_roles_doc(str(roles_dir), str(out_dir))

            out_file = out_dir / "web-app-demo.rst"
            self.assertTrue(out_file.exists())

            txt = out_file.read_text(encoding="utf-8")
            self.assertIn("Web-app-demo Role", txt)
            self.assertIn("**Description:**", txt)
            self.assertIn("Variables", txt)
            self.assertIn("Converted README", txt)


if __name__ == "__main__":
    unittest.main()
