#!/usr/bin/env python
"""
New style setup script. All configuration options are within setup.cfg, pyproject.toml and MANIFEST.in.
"""

import setuptools

setup_kwargs = {
    "name": "EasyReflectometryLib",
}

setuptools.setup(**setup_kwargs)