from runner.local_runner import run_local
from runner.nirvana_runner import run_nirvana
from graph.dependency_graph import set_dependency_graph


runner_types = ['nirvana', 'local']


def run(runner_type, dependency_graph_id="default"):
    set_dependency_graph(dependency_graph_id)
    if runner_type == 'nirvana':
        run_nirvana()
    elif runner_type == 'local':
        run_local()
    else:
        raise ValueError("Unknown runner_type {}. it should be one of {}".format(runner_type, runner_types))
