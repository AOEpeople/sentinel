import json
import os
from pathlib import Path
from typing import ClassVar


class ConfigRepository:
    path: str

    def __init__(self, path: str = str(Path.home()) + "/.sentinel"):
        self.path = path
        Path(self.path).mkdir(parents=True, exist_ok=True)

    def set(self, data: "ClassVar") -> None:
        f = open(self.path + "/" + str(data.__class__.__name__).lower(), mode="w")
        f.write(json.dumps(data.__dict__, indent=4))
        f.close()

    @staticmethod
    def fetch(data: "ClassVar") -> "ClassVar":
        return ConfigRepository().get(data)

    def get(self, data: "ClassVar") -> "ClassVar":
        if self.exists(data) is False:
            raise Exception(f"no valid configuration, please add a valid configuration to {self.path}")
        f = open(self.path + "/" + str(data.__name__).lower())
        content = f.read()
        f.close()
        return json.loads(content, object_hook=lambda d: data(**d))

    def exists(self, data: "ClassVar") -> bool:
        return os.path.isfile(self.path + "/" + str(data.__name__).lower())
