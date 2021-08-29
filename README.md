# ABC-Sphinx-Extension

A sphinx extension to convert abc files into svg
images for use in a Sphinx document.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


It uses [abcm2ps](<http://moinejf.free.fr/>),  to carry out the conversion.

# To install

### From source

```bash
git co git@github.com:wxtim/abc-sphinx-extensions.git
pip install .
```

### From PyPi

```bash
pip install abc-sphinx-extensions
```

# To use

Add files with the extension ``.abc`` in source folder. After building these files will be available
as ``x.svg`` (with title rendered) and ``_x.svg`` (without title) for file ``x.abc``.
