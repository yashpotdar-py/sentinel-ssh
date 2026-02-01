"""
ui.py

Simple CLI coloring utilities. Because reading monochrome logs is for robots.
"""

def red(text: str) -> str:
    """Make text red. Used for bad things."""
    return f"\033[91m{text}\033[0m"

def green(text: str) -> str:
    """Make text green. Used for good things."""
    return f"\033[92m{text}\033[0m"

def yellow(text: str) -> str:
    """Make text yellow. Used for warnings or 'meh' things."""
    return f"\033[93m{text}\033[0m"

def dim(text: str) -> str:
    """Dim the text. Used for stuff you can probably ignore."""
    return f"\033[2m{text}\033[0m"
