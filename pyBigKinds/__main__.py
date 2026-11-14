"""CLI entry point: ``pybigkinds app`` (or ``python -m pyBigKinds app``)."""
import pathlib
import subprocess
import sys

USAGE = "usage: pybigkinds app [streamlit options]"


def main(argv=None):
    """Runs the Streamlit app for `pybigkinds app`; returns a process exit code."""
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] != "app":
        print(USAGE, file=sys.stderr)
        return 2
    try:
        import streamlit  # noqa: F401  pylint: disable=C0415,W0611
    except ImportError:
        print("the app requires the 'app' extra: pip install 'pyBigKinds[app]'", file=sys.stderr)
        return 1
    app = pathlib.Path(__file__).with_name("app.py")
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(app), *argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
