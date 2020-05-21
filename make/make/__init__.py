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
    spacing: str
    dependencies: List[str]
    actions: List[str]

@dataclass
class MakeTarget:
    name: str
    outputs: List[str]
    description: str
    spacing: str
    dependencies: List[str]
    actions: List[str]


class Make(JinjaTool):
    """Make buildfile tool"""
    def __init__(self, db: Database, log: Callable[[str, LogLevel], None]):
        super(Make, self).__init__(db, log)
        self.make = self.get_db(self.get_namespace("Make"))
        # Get jobs! and targets
        jobs = self.get_db("jobs")
        self.max_num_chars = max([len(j) for j in jobs.keys()])
        self.max_num_chars = max([len(t["name"]) for t in self.make["targets"]] + 
            [self.max_num_chars]) 
        self.jobs = self.make_jobs()
        self.targets = self.make_targets()


    def steps(self) -> List[Callable[[], None]]:
        """Returns a list of functions to run for each step"""
        return [self.render_tasks, self.render_makefile]

    def make_jobs(self) -> List[MakeJob]:
        """Returns list of jobs"""
        jobs = self.get_db("jobs")
        job_list = []
        for k, v in jobs.items():
            try:
                descr = v["description"]
            except KeyError:
                descr = f'No description for job "{k}"'
            spacing = (self.max_num_chars - len(k)) * " "
            job_list.append(
                MakeJob(name=k,
                        description=descr,
                        dependencies=[],
                        spacing=spacing + 4 * " ",
                        actions=[self.get_command(k)]))

        return job_list
    
    def make_targets(self) -> List[MakeJob]:
        """Returns list of jobs"""
        target_list = []
        # Create job list from configuration generators
        for t in self.make["targets"]:
            descr = t["description"] if t["description"] else f'Target "{t["name"]}"'
            dependencies = t["dependencies"] if t["dependencies"] else [] 
            outputs = t["outputs"] if t["outputs"] else [] 
            spacing = (self.max_num_chars - len(t["name"])) * " "
            target_list.append(
                MakeTarget(name=t["name"],
                        description=descr,
                        outputs=outputs,
                        dependencies=dependencies,
                        spacing=spacing + 4 * " ",
                        actions=t["commands"]))

        return target_list 

    def render_tasks(self):
        """Generates tasks file that should be imported in the Makefile
        This is always regenerated
        """
        output = os.path.join(self.get_db('internal.work_dir'),
                              'Makefile.toolbox')
        self.render_to_file("Makefile.toolbox", output, jobs=self.jobs, targets=self.targets)

    def render_makefile(self):
        """Looks to see if Makefile exists otherwise populates with new one"""
        if not (Path(self.get_db('internal.work_dir')) / 'Makefile').is_file():
            output = os.path.join(self.get_db('internal.work_dir'), 'Makefile')
            self.render_to_file("Makefile",
                                output,
                                jobs=self.jobs,
                                args=self.get_db('internal.args'))
        else:
            self.log(f'File "Makefile" already exists in working directory.')
