import os
import getpass


def fill_package_template(executable_dir, prog_name):
    return {
        "meta": {
            "name": 'auto-ml-arcadia-container',
            "maintainer": getpass.getuser(),
            "description": 'AutoML Arcadia container for {} library'.format(executable_dir),
            "version": "{revision}"
        },
        "build": {
            "targets": [executable_dir]
        },
        "data":
            [
                {
                    "source": {
                        "type": "BUILD_OUTPUT",
                        "path": os.path.join(executable_dir, prog_name)
                    },
                    "destination": {
                        "path": "/"
                    }
                }
            ]
    }
