"""Small dependency-free quality gate for the demo repository."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / "app").glob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
errors = []
for file_path in files:
    try:
        ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    except SyntaxError as exc:
        errors.append(f"{file_path.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
if errors:
    print("Review failed:")
    print("\n".join(errors))
    sys.exit(1)
print(f"Review passed: parsed {len(files)} Python files successfully.")
