"""Convert abc files in source to svg files making these available for
use in a sphinx doc.
"""

import re

from pathlib import Path
from shlex import split
from subprocess import run


class DependencyMissingError(Exception):
    ...


class abcm2psSubProcFailed(Exception):
    ...


def check_shellprog(prog='abcm2ps -V'):
    """Check that abcm2ps is installed"""
    try:
        run(split(prog), capture_output=True)
    except:   # noqa: E722
        raise DependencyMissingError(
            f'You need to have {prog} installed'
        )


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
    # Delete the title field from the files
    fname_notitle = rm_title(filename)
    fnames = [filename, fname_notitle]
    for fname in fnames:
        svgfile = fname.with_suffix('.svg')

        # Run abcm2s as a subprocess:
        output = run(
            [
                'abcm2ps',
                '-g',   # Produce SVG output.
                f'{str(fname)}',
                '-O',   # Output file.
                f'{svgfile}',
            ],
            capture_output=True
        )
        if output.returncode != 0:  # pragma: no cover
            # Haven't been able to test this because almost
            # no level of malformation seems to cause the wrapped
            # script to fail.
            msg = (
                'ABCM2PS Failed because:\n'
                f'stdout\n------\n{output.stdout}\n\n'
                f'stderr\n------\n{output.stderr}\n'
            )
            raise abcm2psSubProcFailed(msg)
        else:
            outfile = re.findall(
                r'written on (.*) \(', output.stdout.decode()
            )[0]
            Path(outfile).rename(svgfile)
    return True


def rm_title(filename):
    """Remove title fields from an abcfile and write
    the result to _{original_title}.abc
    """
    text = filename.read_text().splitlines()
    text = [line for line in text if not re.match('^T:', line)]
    fname_notitle = filename.with_name(f'_{filename.name}')
    fname_notitle.write_text('\n'.join(text))
    return fname_notitle


def abc_wrangler(app):
    check_shellprog()
    for abcpath in Path(app.srcdir).rglob('*.abc'):
        if not re.match('^_.*', abcpath.name):
            clean_abcpath(abcpath)
            convert_abcfile(abcpath)


def setup(app):   # pragma: no cover
    app.connect('builder-inited', abc_wrangler)
