import asyncio
import json

from sentinel.libs import executor as executor_lib
from mitmproxy import ctx


# pylint: disable-msg=missing-class-docstring
class Executor:
    done = False

    # pylint: disable-msg=no-self-use
    def load(self, loader):
        loader.add_option(
            name="executor_cmd",
            typespec=str,
            default="[]",
            help="json list of cmd parts to execute",
        )

    # pylint: disable-msg=no-self-use
    def running(self):
        if not self.done:
            cmd = json.loads(ctx.options.executor_cmd)
            asyncio.get_event_loop().run_in_executor(None, self.exec, cmd)
            self.done = True

    # pylint: disable-msg=no-self-use
    def exec(self, cmd):
        if ctx.options.listen_port != "":
            port = ctx.options.listen_port
        else:
            port = "8080"
        local_host = "localhost"
        executor_lib.run(cmd,
                         {"http_proxy": f"http://{local_host}:{port}", "https_proxy": f"http://{local_host}:{port}"})
        ctx.master.shutdown()


addons = [
    Executor()
]
