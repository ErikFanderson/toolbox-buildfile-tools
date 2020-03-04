from doit.action import CmdAction

{% for job in jobs -%}
def task_{{job['name']}}() -> dict:
    """Runs toolbox job {{job['name']}}"""
    return {
        'file_dep': {{job['file_dep']}},
        'targets': {{job['targets']}},
        'actions': [{{job['action']}}],
        'verbosity': {{job['verbosity']}}
    }
{% endfor -%}
