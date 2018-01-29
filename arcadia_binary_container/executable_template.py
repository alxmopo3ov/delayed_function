executable_template = """import {function_file}
from {auto_ml_root}.environment import Environment
from {auto_ml_root}.executable_container.nirvana_container import NirvanaContainer

if __name__ == "__main__":
    env = Environment()
    container_type = env.container_type
    function_name = env.function_name
    container = NirvanaContainer({function_file}.{function_name})
    container.run()
"""