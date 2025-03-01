import re
import subprocess
from pathlib import Path

# Path to pyproject.toml
PYPROJECT_PATH = Path("pyproject.toml")

def get_version():
    """Extracts the current version from pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    match = re.search(r'version = "(.*?)"', content)
    return match.group(1) if match else None

def update_version(new_version):
    """Replaces the old version with the new version in pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    updated_content = re.sub(r'version = "(.*?)"', f'version = "{new_version}"', content)
    PYPROJECT_PATH.write_text(updated_content)

# Get current version and update patch number
version = get_version()
if version:
    major, minor, patch = map(int, version.split("."))
    new_version = f"{major}.{minor}.{patch + 1}"
    update_version(new_version)
    print(f"Updated version to: {new_version}")

    # Build package
    subprocess.run(["python", "-m", "build"], check=True)

    # Upload to TestPyPI
    subprocess.run(["python", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"], check=True)
else:
    print("Version not found in pyproject.toml")
