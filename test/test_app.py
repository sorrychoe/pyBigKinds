import pathlib

import pandas as pd
import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from pyBigKinds import __main__ as cli  # noqa: E402

APP = str(pathlib.Path(cli.__file__).with_name("app.py"))


def test_empty_state_prompts_upload():
    at = AppTest.from_file(APP).run()
    assert not at.exception
    assert at.info


def test_all_tabs_run():
    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["data"] = pd.read_excel("test/test.xlsx")
    at.run()
    assert not at.exception
    for key in ("run_cluster", "run_lda", "run_assoc"):
        at.button(key=key).click().run()
        assert not at.exception, key
    assert at.metric[0].value.startswith("20")


def test_cli_rejects_unknown_command(capsys):
    assert cli.main([]) == 2
    assert "usage" in capsys.readouterr().err
