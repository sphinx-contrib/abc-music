"""Convert abc files in source to svg files making these available for
use in a sphinx doc.
"""

import re
import shutil

from pathlib import Path
from shlex import split
from subprocess import run


class DepencyMissingError(Exception):
    ...


class abcm2psSubProcFailed(Exception):
    ...


def check_deps():
    """Check that abcm2ps is installed"""
    abcm2ps = run(split('abcm2ps -V'), capture_output=True)
    if abcm2ps.returncode != 0:
        raise DepencyMissingError('You need to have abcm2ps installed')


def clean_abcpath(abcpath):
    """clean up existing abc files
    """
    existing_files = [
        abcpath.with_suffix('.svg'),
        abcpath.parent / f'_{abcpath.name}'
    ]
    for file_ in existing_files:
        if file_.is_file():
            file_.unlink()


def convert_abcfile(filename):
    """Find Convert ABC to svg for later use.
    """
    svgfile = filename.with_suffix('.svg')
    if svgfile.is_file():
        shutil.rmtree(svgfile)

    # Delete the title field from the files
    text = filename.read_text().splitlines()
    text = [line for line in text if not re.match('^T:', line)]
    fname2 = filename.with_name(f'_{filename.name}')
    fname2.write_text('\n'.join(text))

    # Run abcm2s as a subprocess:
    output = run(
        [
            'abcm2ps',
            '-g',   # Produce SVG output.
            f'{str(fname2)}',
            '-O',   # Output file.
            f'{svgfile}'
        ],
        capture_output=True
    )
    outfile = re.findall(r'written on (.*) \(', output.stdout.decode())[0]
    Path(outfile).rename(svgfile)
    if output.returncode != 0:
        msg = (
            'ABCM2PS Failed because:\n'
            f'stdout\n------\n{output.stdout}\n\n'
            f'stderr\n------\n{output.stderr}\n'
        )
        raise abcm2psSubProcFailed(msg)


def abc_wrangler(app):
    check_deps()
    for abcpath in Path(app.srcdir).rglob('*.abc'):
        if not re.match('^_.*', abcpath.name):
            clean_abcpath(abcpath)
            convert_abcfile(abcpath)


def setup(app):
    app.connect('builder-inited', abc_wrangler)
