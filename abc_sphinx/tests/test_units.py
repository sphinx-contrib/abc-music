"""
Unit tests for abcm2svg.
"""

import pytest

from abc_sphinx.abcm2svg import clean_abcpath


@pytest.mark.parametrize('filecreate, fileclean',
    [
        ('The Sloe.svg', 'The Sloe.svg'),
        ('The Sloe.abc', '_The Sloe.abc')
    ]
)
def test_clean_abcpath(tmp_path, filecreate, fileclean):
    filecreate = (tmp_path / filecreate)
    fileclean = tmp_path / fileclean
    filecreate.touch()
    fileclean.touch()
    clean_abcpath(filecreate)
    assert (fileclean).is_file() == False


