"""
Automatically run basic make checks.
"""


import pytest

from pathlib import Path
from subprocess import run


@pytest.fixture(scope='module')
def make_html():
    """Run the documentation make"""
    makepath = Path(__file__).parent.parent.parent
    cap = run(['make', 'html', f'--directory={str(makepath)}'], capture_output=True)
    yield cap, makepath


def test_make_html_runs(make_html):
    assert make_html[0].returncode == 0


@pytest.mark.parametrize(
    'name',
    ['Boulavogue.svg', 'Jenny Pluck Pears.svg']
)
def test_make_html_outputs(make_html, name):
    svgs = [i.name for i in (make_html[1] / 'source').rglob('*.svg')]
    assert name in svgs