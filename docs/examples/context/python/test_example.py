from pathlib import Path

import pytest

from oso import Oso
import os
from runpy import run_path
import context

run_path("context.py")


@pytest.fixture
def oso():
    oso = Oso()
    oso.register_class(context.Env)
    return Oso()


@pytest.fixture
def load(oso):
    def load(policy):
        oso.load_file(Path(__file__).parent.parent / policy)

    return load


def test_policy(oso, load):
    load("01-context.polar")

    os.environ["ENV"] = "production"
    assert not oso.is_allowed("steve", "test", "policy")
    os.environ["ENV"] = "development"
    assert oso.is_allowed("steve", "test", "policy")
