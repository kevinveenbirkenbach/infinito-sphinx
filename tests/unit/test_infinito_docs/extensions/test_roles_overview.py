import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace


def _add_src_to_path() -> None:
    root = Path(__file__).resolve()
    while root != root.parent and not (root / "src").exists():
        root = root.parent
    sys.path.insert(0, str(root / "src"))


_add_src_to_path()

from infinito_docs.extensions.roles_overview import RolesOverviewDirective, setup  # noqa: E402


class _FakeApp:
    def __init__(self) -> None:
        self.added = {}

    def add_directive(self, name: str, directive) -> None:
        self.added[name] = directive


class _FakeReporter:
    def error(self, message, *args, **kwargs):
        return ("ERROR", message)


class _FakeStateMachine:
    def __init__(self) -> None:
        self.reporter = _FakeReporter()


class _FakeState:
    def __init__(self, env) -> None:
        self.document = SimpleNamespace(settings=SimpleNamespace(env=env))

    @property
    def document_reporter(self):
        return _FakeReporter()


class TestRolesOverview(unittest.TestCase):
    def test_setup_registers_directive(self) -> None:
        app = _FakeApp()
        setup(app)
        self.assertIn("roles-overview", app.added)
        self.assertIs(app.added["roles-overview"], RolesOverviewDirective)

    def test_run_builds_overview(self) -> None:
        with TemporaryDirectory() as td:
            srcdir = Path(td) / "srcdir"
            roles_dir = srcdir / "roles"
            role_dir = roles_dir / "web-app-demo"
            (role_dir / "meta").mkdir(parents=True, exist_ok=True)

            (role_dir / "meta" / "main.yml").write_text(
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
            (role_dir / "README.md").write_text("# Demo Title\n\nText\n", encoding="utf-8")

            env = SimpleNamespace(srcdir=str(srcdir))
            state = _FakeState(env)
            sm = _FakeStateMachine()

            d = RolesOverviewDirective(
                name="roles-overview",
                arguments=[],
                options={},
                content=[],
                lineno=1,
                content_offset=0,
                block_text=".. roles-overview::",
                state=state,
                state_machine=sm,
            )

            res = d.run()
            self.assertTrue(isinstance(res, list))
            self.assertEqual(len(res), 1)


if __name__ == "__main__":
    unittest.main()
