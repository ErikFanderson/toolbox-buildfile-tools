from doit.action import CmdAction
{% for job in jobs %}
#----------------------------------------------------------
# Task "{{job['name']}}" 
#----------------------------------------------------------
def task_{{job['name']}}() -> dict:
    """[Generated] Runs toolbox job {{job['name']}}"""
    return {
        'file_dep': {{job['file_dep']}},
        'targets': {{job['targets']}},
        'actions': [{{job['action']}}],
        'verbosity': {{job['verbosity']}}
    }
#----------------------------------------------------------
{% endfor %}
#----------------------------------------------------------
# Utility Methods
#----------------------------------------------------------
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
