import os
import subprocess
import json
from shutil import which
from pathlib import Path


class Wine:
    def __init__(self, wine: os.PathLike, prefix: os.PathLike = None) -> None:
        wine = Path(wine)
        binary = wine.joinpath("bin/wine")
        winedbg = wine.joinpath("bin/winedbg")
        if not wine.is_dir():
            raise FileNotFoundError("Wine path doesn't exist.")
        if not binary.is_file():
            raise FileNotFoundError("Wine binary doesn't exist.")
        if not winedbg.is_file():
            raise FileNotFoundError("Winedbg doesn't exist.")
        if not prefix:
            prefix = "~/.wine"
        self.wine = wine
        self.prefix = prefix
        self._binary = binary
        self._winedbg = winedbg

    @property
    def version(self):
        return subprocess.run([str(self.binary), "--version"]).stdout.decode()

    @staticmethod
    def from_system():
        wine = which("wine")
        if wine is None:
            raise FileNotFoundError("Wine doesn't exists in PATH")
        return Wine(wine=Path(wine).parent, prefix="~/.wine")

    @staticmethod
    def from_grapejuice():
        cfg_file = Path("~/.config/brinkervii/grapejuice/user_settings.json")
        if not cfg_file.is_file():
            raise FileNotFoundError("Grapejuice config file doesn't exist.")
        cfg: dict = json.loads(cfg_file.read_text())
        wine: str = None
        prefix: Path = Path("~/.local/share/grapejuice/prefixes/player/")
        for pfx in cfg["wineprefixes"]:
            if "player" in pfx["hints"]:
                wine = pfx["wine_home"] + "/bin/wine"
        if wine is None:
            try:
                wine = cfg["default_wine_home"] + "/bin/wine"
            except KeyError:
                # Grapejuice using system Wine, so use that.
                return Wine.from_system()
        if not prefix.is_dir():
            prefix.mkdir(parents=True)
        return Wine(binary=wine, prefix=prefix)

    def _prepare_env(self, prefix: str = None, env: dict = None):
        if not prefix:
            prefix = self.prefix
        _env: dict = os.environ.copy()
        _env.update({"WINEPREFIX": prefix})
        if env:
            _env.update(env)
        return _env

    def run(
        self, args: list[str] | str, prefix: str = None, env: dict = None, shell: bool = False
    ) -> subprocess.CompletedProcess[bytes]:
        if shell:
            args = str(self._binary) + " " + args
        else:
            args = [str(self._binary)] + args
        return subprocess.run(
            args=args, env=self._prepare_env(prefix=prefix, env=env), capture_output=True, shell=shell
        )

    def winedbg(
        self, args: list[str] | str, prefix: str = None, env: dict = None, shell: bool = False
    ) -> subprocess.CompletedProcess[bytes]:
        _env = self._prepare_env(prefix=prefix, env=env)
        if shell:
            args = str(self._winedbg) + " " + args
        else:
            args = [str(self._winedbg)] + args
        return subprocess.run(
            args=args, env=_env, capture_output=True, shell=shell
        )
