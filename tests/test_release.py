"""Quick and dirty tests to avoid recreating releases three times."""

import pathlib

import pytest

import spookyhash

root_path = pathlib.Path(__file__).parent.parent
changelog_path = root_path / "CHANGELOG.md"


def test_version_consistent() -> None:
    """Ensure versions in spookyhash.py and spookyhash.pyx are consistent."""
    assert spookyhash.__version__ == spookyhash._spookyhash.__version__


@pytest.mark.skipif(not changelog_path.exists(), reason="Changelog not found")
def test_version_changelog() -> None:
    versions = [
        line.split()[1]
        for line in changelog_path.read_text().splitlines()
        if line.startswith("##")
    ]
    assert versions[0] == f"v{spookyhash.__version__}"
