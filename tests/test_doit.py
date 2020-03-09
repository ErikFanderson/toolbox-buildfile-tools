#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Erik Anderson
# Email: erik.francis.anderson@gmail.com
# Date: 02/27/2020
"""Docstring for module test_example"""

# Imports - standard library
import subprocess
from pathlib import Path
import os, sys

# Imports - 3rd party packages

# Imports - local source

TEST_DIR = Path(__file__).resolve().parent
TOOLBOX = Path('.').resolve() / 'toolbox'
MOCK_DIR = TEST_DIR / 'mock'


def setup_module(test_mock_doit_build):
    """Clone toolbox and add to path"""
    subprocess.run(
        ["git", "clone", "git@github.com:ErikFanderson/toolbox.git"])
    # Set python path to include toolbox/
    sys.path.insert(1, str(TOOLBOX))
    # Set toolbox_Home toolbox/
    os.environ['TOOLBOX_HOME'] = str(TOOLBOX)


def teardown_module(test_mock_doit_build):
    """Removes build and toolbox directories"""
    subprocess.run(["rm", "-rf", "toolbox", "build", "dodo.py", "dodo_tasks.py"])
    sys.path.remove(str(TOOLBOX))


def test_mock_doit_build():
    """Tests the mock sim runs successfully"""
    from toolbox.toolbox import ToolBox, ToolBoxParams
    from toolbox.logger import LogLevel, LoggerParams
    args = ToolBoxParams(f'{MOCK_DIR}/doit/tools.yml',
                         build_dir='build',
                         symlink=None,
                         config=[f'{MOCK_DIR}/doit/config.yml'],
                         interactive=False,
                         log_params=LoggerParams(LogLevel.DEBUG),
                         job='test_doit')
    tb = ToolBox(args)
    tb.execute()
