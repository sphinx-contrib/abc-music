"""
Unit tests for abcm2svg.
"""

import pytest

import abc_sphinx
from abc_sphinx.abcm2svg import (
    clean_abcpath,
    check_shellprog,
    DependencyMissingError,
    rm_title,
    convert_abcfile,
    abc_wrangler
)


@pytest.mark.parametrize(
    'script',
    ['improbably_script_name', 'exit 1']
)
def test_check_shellprog(caplog, script):
    with pytest.raises(DependencyMissingError):
        check_shellprog(script)


@pytest.mark.parametrize(
    'filecreate, fileclean',
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
    assert (fileclean).is_file() is False


def test_rm_title(tmp_path):
    infile = tmp_path / 'Proudlocks Hornpipe.abc'
    outfile = tmp_path / '_Proudlocks Hornpipe.abc'
    infile.write_text(
        'T:Proudlocks Hornpipe\n'
        'T:  Lewis Proudlock\'s\n'
        'T: Proudlocks\' Favourite\n'
        'A: Lewis Proudlock'
    )
    rm_title(infile)
    assert outfile.read_text() == (
        'A: Lewis Proudlock'
    )


def test_convert_abcfile(tmp_path):
    """Content is stub, I may not use, because abcm2svg is
    extrnal, and should not need testing."""
    abcfile = tmp_path / 'Water of Teign.abc'
    abcfile.write_text("""
X: 4
T: Boulavogue
R: waltz
M: 3/4
L: 1/8
K: Dmaj
D2|"C"G4 D2|"C"G4 Bd|"C"g4 "Em"f2|"F"eg3 e2|"C"d4 "A"e2|
B4 GB|"Dm"A4 "D"G2|"F"E4 "G"D2|
"C"G4 "C"D2|"C"G4 Bd|"C"g4 "Em"f2|"F"eg3 e2|"C"d4 e2|
B G3 B2|"A"A4 "C"G2|"C"G4 "C"d2||
"C"d4 B2|"B"d2 e2 f2|"Am"g4 f2|"F"eg3 e2|"C"d4 e2|B4 GB|
"Dm"A4 "F"G2|"F"E4 "G"D2|
"C"G4 D2|"C"G4 Bd|"C"g4 "Em"f2|"F"eg3 e2|"C"d4 e2|B G3 B|
"Dm"A4 "C"G2|"C"G4||
    """)
    convert_abcfile(abcfile)
    assert (tmp_path / 'Water of Teign.svg').is_file()


def test_abc_wrangler(tmp_path, monkeypatch, capsys):
    for func in ['clean_abcpath', 'convert_abcfile']:
        monkeypatch.setattr(
            abc_sphinx.abcm2svg,
            func,
            lambda p: print(f'{p}')
        )
    abcfile = tmp_path / 'hello.abc'
    abcfile.touch()
    from types import SimpleNamespace
    app = SimpleNamespace(
        srcdir=tmp_path
    )
    abc_wrangler(app)
    out = capsys.readouterr().out.splitlines()
    assert 'hello.abc' in out[0]
