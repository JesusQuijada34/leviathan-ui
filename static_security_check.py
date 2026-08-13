import ast
from pathlib import Path

root = Path("leviathan_ui")
core = list(root.glob("*.py"))
assert len(core) >= 5
for path in core:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assert path.stat().st_size > 500, path
source = "\n".join(path.read_text(encoding="utf-8") for path in core)
requirements = Path("lib/requirements.txt").read_text(encoding="utf-8")
details = Path("details.xml").read_text(encoding="utf-8")
readme = Path("README.md").read_text(encoding="utf-8")
assert "<platform>AlphaCube</platform>" in details
assert "PyQt6" in requirements and "Pillow" in requirements
assert "sys.platform == \"win32\"" in source or "sys.platform == 'win32'" in source
assert "except" in source
assert "AlphaCube" in readme
assert "Updater template for PackageMaker" not in source
print("LEVIATHAN_UI_STATIC_FUNCTIONAL_CHECK_OK")
