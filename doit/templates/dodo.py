from doit.action import CmdAction
from pathlib import Path

if Path("dodo_tasks.py").is_file():
    from dodo_tasks import *

#----------------------------------------------------------
# Global doit setup
#----------------------------------------------------------
# Doit config
DOIT_CONFIG = {'default_tasks': []}

# Global setup
TOOLS_FILE = '{{args.tools_file}}'
BUILD_DIR = '{{args.build_dir}}'
SYMLINK = {% if args.symlink %}
'{{args.symlink}}'
{% else %}
None
{% endif %}
CONF_YML = [
{% for config in args.config -%}
{% if not loop.last -%}
    "{{config}}",
{% else -%}
    "{{config}}"
{% endif -%}
{% endfor -%}
]
#----------------------------------------------------------

#----------------------------------------------------------
# Create buildfile
#----------------------------------------------------------
def task_buildfile():
    '''Creates new buildfile'''
    config = ' -c ' + ' -c '.join(CONF_YML)
    build_dir = '' if not BUILD_DIR else f' -b {BUILD_DIR}'
    symlink = '' if not SYMLINK else f' -ln {SYMLINK}'
    tools_file = '' if not TOOLS_FILE else f' -t {TOOLS_FILE}'
    cmd = f"toolbox-cli{config}{build_dir}{symlink}{tools_file} {{args.job}}"
    return {
        'actions': [CmdAction(cmd, buffering=1)],
        'verbosity': 2
    }
#----------------------------------------------------------

#----------------------------------------------------------
# Clean Methods
#----------------------------------------------------------
def task_cleanup():
    """Cleans up files"""
    actions = [CmdAction(f"rm -rf build *.log __pycache__ {BUILD_DIR}", buffering=1)]
    return {
        'actions': actions,
        'verbosity': 2
    }
#----------------------------------------------------------
