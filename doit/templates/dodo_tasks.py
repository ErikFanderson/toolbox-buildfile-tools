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
