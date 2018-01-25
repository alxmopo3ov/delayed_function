"""
Arcadia container in case of python is one monolithic binary. We suppose that
user has defined library for every function he uses in the program (we require the library_root parameter
in container_params for arcadia users)

Arcadia container is needed to run on Nirvana: we automatically create package and corresponding folder with executable
binary
"""


from arcadia_binary_container.generate_arcadia_binary import generate_arcadia_binary_dir
