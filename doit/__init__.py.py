#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Erik Anderson
# Email: erik.francis.anderson@gmail.com
# Date: 03/03/2020
"""Docstring for module __init__.py"""

# Imports - standard library
from typing import Callable, List

# Imports - 3rd party packages
from toolbox.tool import Tool
from toolbox.database import Database
from toolbox.logger import LogLevel
from toolbox.path_helper import PathHelper

# Imports - local source

class Doit(Tool):
    """Doit buildfile tool"""

    def __init__(self, db: Database, log: Callable[[str, LogLevel], None]):
        super().__init__(db,log)

    def steps(self) -> List[Callable[[], None]]:
        """Returns a list of functions to run for each step"""
        return [self.check_files,
                self.generate_tcl,
                self.run_sim]

    def check_files(self):
        """Checks that all files are real"""

    def generate_tcl(self):
        """Generates tcl that will be passed to xrun"""

    def run_sim(self):
        """Calls xrun"""
