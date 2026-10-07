"""Regression checks for the historical baseline's governance file boundary."""
import ast
from pathlib import Path
import tempfile
import unittest

source = Path(__file__).with_name("verify.py").read_text()
module = ast.parse(source)
function = next(node for node in module.body
                if isinstance(node, ast.FunctionDef) and node.name == "website_paths")
namespace = {}
exec(compile(ast.Module(body=[function], type_ignores=[]), "website_paths", "exec"), namespace)
website_paths = namespace["website_paths"]

class EnumerationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.add("index.html")
        self.add("assets/style.css")

    def add(self, path):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("synthetic fixture")

    def test_governance_does_not_change_website_inventory(self):
        expected = website_paths(self.root)
        for path in ["README.md", "AGENTS.md", "SECURITY.md", ".gitignore",
                     ".ai/project.yaml", ".github/PULL_REQUEST_TEMPLATE.md",
                     "docs/note.md", "baselines/evidence.txt", ".git/config"]:
            self.add(path)
        self.assertEqual(website_paths(self.root), expected)

    def test_unexpected_website_files_remain_detectable(self):
        expected = website_paths(self.root)
        self.add("unexpected.html")
        self.assertNotEqual(website_paths(self.root), expected)
        self.assertIn("unexpected.html", website_paths(self.root))

    def test_nested_readme_is_not_a_root_governance_entrypoint(self):
        self.add("assets/README.md")
        self.assertIn("assets/README.md", website_paths(self.root))

if __name__ == "__main__":
    unittest.main()
