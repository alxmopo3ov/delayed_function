import os
import getpass
import json
from arcadia_binary_container.package_template import fill_package_template


auto_ml_dirname = 'auto_ml_executable_dir'
nirvana_auto_ml_container_program_name = 'nirvana_auto_ml_container'


ya_make_template = """PROGRAM({program_name})

OWNER({owner})

PY_SRCS(
    __main__.py
)

PEERDIR(
    {auto_ml_root}
    {library_root}
)

END()
"""


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


def get_arcadia_root():
    path = os.path.dirname(os.path.abspath(__file__))
    while path and not os.path.exists(os.path.join(path, '.arcadia.root')):
        path = os.path.dirname(path)
    if path:
        return path
    else:
        raise Exception('cant find arcadia root')


def get_auto_ml_root():
    cur_file = globals()['__file__']
    relpath = os.path.relpath(cur_file, get_arcadia_root())
    return '/'.join(relpath.split('/')[:-1])


def get_function_library_root(func):
    raise NotImplementedError("Sorry, but by now you must add library_root for every function you define")


def generate_arcadia_binary_dir(func, ignore_existing=False):
    if 'library_root' not in func.container_params:
        library_root = get_function_library_root(func)
    else:
        library_root = func.container_params['library_root']
        if library_root.startswith('/'):
            library_root = library_root[1:]
    ya_make = ya_make_template.format(
        owner=getpass.getuser(),
        auto_ml_root=get_auto_ml_root(),
        library_root=library_root,
        program_name=nirvana_auto_ml_container_program_name
    )

    # we assume that function can be imported from the __init__.py
    main = executable_template.format(
        function_file=library_root.replace('/', '.'),
        function_name=func.__name__,
        auto_ml_root=get_auto_ml_root()
    )

    dirname = os.path.join(library_root, auto_ml_dirname)
    if ignore_existing and os.path.exists(dirname):
        return dirname

    os.makedirs(dirname)
    with open(os.path.join(dirname, 'ya.make'), 'wt') as f:
        f.write(ya_make)
    with open(os.path.join(dirname, '__main__.py'), 'wt') as f:
        f.write(main)

    package = fill_package_template(dirname, nirvana_auto_ml_container_program_name)
    with open(os.path.join(dirname, 'package.json'), 'wt') as f:
        f.write(json.dumps(package) + '\n')

    return dirname
