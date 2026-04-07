"""Load model package data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ModelPackage = Dict[str, Any]


def load_packages(data_file: Path | str) -> List[ModelPackage]:
    """Load model packages from JSON."""
    return json.loads(Path(data_file).read_text(encoding="utf-8"))
