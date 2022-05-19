# pylint: disable=W1510

import subprocess
import os
import sys
from sentinel.libs.helpers import print_info


def run(
        cmd, env=None, capture_output=False, stdin=None, mask=None, cwd=None
):
    if mask is None:
        mask = []
    if env is None:
        env = os.environ.copy()
    else:
        env = {**os.environ.copy(), **env}

    command_as_string = " ".join(cmd)
    for value_to_mask in mask:
        command_as_string = command_as_string.replace(value_to_mask, "***")

    log_line = f"executing: ```{command_as_string}```"
    if cwd and cwd != ".":
        log_line += f' in directory {cwd}'
    print_info(log_line)

    sys.stdout.flush()
    return subprocess.run(cmd, env=env, capture_output=capture_output, input=stdin, cwd=cwd)
