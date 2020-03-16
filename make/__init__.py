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
from jinja2 import StrictUndefined, Environment, FileSystemLoader
from dataclasses import dataclass

# Imports - 3rd party packages
from toolbox.tool import Tool
from toolbox.database import Database
from toolbox.logger import LogLevel

# Imports - local source
from jinja_tool import JinjaTool

@dataclass
class MakeJob:
    name: str
    description: str
    dependencies: List[str]
    actions: List[str]

class Make(JinjaTool):
    """Make buildfile tool"""
    def __init__(self, db: Database, log: Callable[[str, LogLevel], None]):
        template_dir = os.path.join(db.get_db('internal.tools.Make.path'),
                                    'templates')
        JinjaTool.add_template_dirs(db, [template_dir])
        super(Make, self).__init__(db, log)
        self.jobs = self.make_jobs()

    def steps(self) -> List[Callable[[], None]]:
        """Returns a list of functions to run for each step"""
        return [self.render_tasks, self.render_makefile]

    def get_action_str(self, job: str) -> str:
        """Uses command line command and replaces build job with job"""
        replace = True
        cmd = self.get_db("internal.command").split(' ')
        for i, c in enumerate(cmd):
            if replace and not c.startswith('-'):
                cmd[i] = job
            elif c.startswith('-'):
                replace = False
            else:
                replace = True
        cmd = ' '.join(cmd)
        return f'"toolbox-cli {cmd}"'

    def make_jobs(self) -> List[MakeJob]:
        """Returns list of jobs"""
        jobs = list(self.get_db("jobs").keys())
        job_list = []
        for j in jobs:
            job_list.append(
                MakeJob(
                    name=j,
                    description=f'Need better description for task "{j}"',
                    dependencies=[],
                    actions=[self.get_action_str(j)]
                )
            )
        return job_list

    def render_tasks(self):
        """Generates tasks file that should be imported in the Makefile
        This is always regenerated
        """
        output = os.path.join(self.get_db('internal.work_dir'),
                              'Makefile.toolbox')
        self.render_to_file("Makefile.toolbox", output, jobs=self.jobs)
        self.log('File "Makefile.toolbox" succesfully generated.')

    def render_makefile(self):
        """Looks to see if Makefile exists otherwise populates with new one"""
        if not (Path(self.get_db('internal.work_dir')) / 'Makefile').is_file():
            output = os.path.join(self.get_db('internal.work_dir'), 'Makefile')
            self.render_to_file("Makefile",
                                output,
                                jobs=self.jobs, 
                                args=self.get_db('internal.args'))
            self.log('File "Makefile" succesfully generated.')
        else:
            self.log(f'File "Makefile" already exists in working directory.')
