#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Erik Anderson
# Email: erik.francis.anderson@gmail.com
# Date: 03/03/2020
"""Docstring for module __init__.py"""

# Imports - standard library
from typing import Callable, List
import os, sys
from pathlib import Path

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
        return [self.gen_tasks, self.gen_dodo]

    def get_action_str(self, job: str) -> str:
        """Uses command line command and replaces build job with job"""
        replace = True
        cmd = self.get_db("internal.command").split(' ')
        for i,c in enumerate(cmd):
            if replace and not c.startswith('-'):
                cmd[i] = job
            elif c.startswith('-'):
                replace = False
            else:
                replace = True
        cmd = ' '.join(cmd)
        return f'CmdAction("toolbox-cli {cmd}", buffering=1)'

    def gen_tasks(self):
        """Generates tasks file that should be imported in the dodo file"""
        jobs = list(self.get_db("jobs").keys())
        job_list = []
        for job in jobs:
            self.get_action_str(job)
            job_dict = {}
            job_dict['name'] = job
            job_dict['file_dep'] = []
            job_dict['targets'] = []
            job_dict['action'] = self.get_action_str(job)
            job_dict['verbosity'] = self.get_db('tools.Doit.verbosity')
            job_list.append(job_dict)
        template = os.path.join(self.path, 'templates/dodo_tasks.py')
        output = os.path.join(self.get_db('internal.work_dir'), 'dodo_tasks.py')
        self.jinja_render(template, output, jobs=job_list)
        self.log('File "dodo_tasks.py" succesfully generated.')

    def gen_dodo(self):
        """Looks to see if dodo.py exists otherwise populates with new one"""
        if not (Path(self.get_db('internal.work_dir')) / 'dodo.py').is_file():
            template = os.path.join(self.path, 'templates/dodo.py')
            output = os.path.join(self.get_db('internal.work_dir'), 'dodo.py')
            self.jinja_render(template, output, args=self.get_db('internal.args'))
            self.log('File "dodo.py" succesfully generated.')
        else:
            self.log(f'File "dodo.py" already exists in working directory.')
