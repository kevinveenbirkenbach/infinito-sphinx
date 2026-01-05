import io
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

from infinito_docs.__main__ import parse_makefile_targets, run_make_command  # noqa: E402


class TestMainModule(unittest.TestCase):
    def test_parse_makefile_targets_extracts_descriptions(self) -> None:
        with TemporaryDirectory() as td:
            p = Path(td) / "Makefile"
            p.write_text(
                "\n".join(
                    [
                        "# Build HTML docs",
                        "html:",
                        "\t@echo building",
                        "",
                        "# Clean artifacts",
                        "clean:",
                        "\t@echo cleaning",
                        "",
                        "nohelp:",
                        "\t@echo x",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            targets = parse_makefile_targets(p)
            self.assertIn("html", targets)
            self.assertEqual(targets["html"], "Build HTML docs")
            self.assertIn("clean", targets)
            self.assertEqual(targets["clean"], "Clean artifacts")
            self.assertIn("nohelp", targets)
            self.assertEqual(targets["nohelp"], "")

    @patch("infinito_docs.__main__.subprocess.Popen")
    def test_run_make_command_invokes_make(self, popen: MagicMock) -> None:
        fake_proc = MagicMock()
        fake_proc.stdout = io.StringIO("out1\nout2\n")
        fake_proc.stderr = io.StringIO("err1\n")
        fake_proc.wait.return_value = 7
        popen.return_value = fake_proc

        with TemporaryDirectory() as td:
            repo_root = Path(td)

            rc = run_make_command("html", repo_root)

            popen.assert_called_once()
            args, kwargs = popen.call_args
            self.assertEqual(args[0], ["make", "html"])
            self.assertEqual(kwargs["cwd"], str(repo_root))
            self.assertTrue(kwargs["text"])
            self.assertEqual(rc, 7)


if __name__ == "__main__":
    unittest.main()
