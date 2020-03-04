from doit.action import CmdAction
from dodo_tasks import *

#----------------------------------------------------------
# Global doit setup
#----------------------------------------------------------
# Doit config
DOIT_CONFIG = {
    'default_tasks': []
}

# Global setup
BUILD_DIR = '/sratch/efa/pipes_superswitch'
SYMLINK = 'build'
CONF_YML = [
{% for config in configs -%}
{% if not loop.last -%}
    "{{config}}",
{% else -%}
    "{{config}}"
{% endif -%}
{% endfor -%}
]

def return_task(file_dep:list=[],targets:list=[],actions:list=[],verbosity:int=2) -> dict:
    """Helper function for return doit task"""
    return {
        'file_dep': file_dep,
        'targets': targets,
        'actions': actions,
        'verbosity': verbosity
    }

def action_fn(action):
    """Default action command w/ no line buffering"""
    return CmdAction(action,buffering=1)
#----------------------------------------------------------

#----------------------------------------------------------
# Create buildfile
#----------------------------------------------------------
def task_buildfile():
    '''Creates new buildfile'''
    return return_task(actions=[{{build_action}}])
#----------------------------------------------------------

#----------------------------------------------------------
# Clean Methods
#----------------------------------------------------------
def task_cleanup():
    """Cleans up files"""
    actions = [
	action_fn("rm -rf build *.log __pycache__ {{build_dir}}")
    ]
    return return_task(actions=actions)
#----------------------------------------------------------
