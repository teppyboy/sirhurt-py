import os
import platform
import subprocess

# from pathlib import Path
# from sirhurt.constants import APP_PATHS
from sirhurt.wine import Wine


class Windows(Wine):
    def __init__(self, wine: os.PathLike = None, prefix: os.PathLike = None) -> None:
        # Fake Wine
        if platform.system() != "Windows":
            raise RuntimeError("Only Windows is supported using fake Wine.")
        # self._wine = Path(APP_PATHS.user_cache_dir).joinpath("wine-windows")
        # self._bin = self._wine.joinpath("bin")
        # self._bin.mkdir(parents=True, exist_ok=True)
        # # Fake executables
        # self._bin.joinpath("wine").touch()
        # self._bin.joinpath("winedbg").touch()
        # super().__init__(wine=self._wine, prefix=prefix)

    @property
    def version(self):
        return platform.release()

    @staticmethod
    def from_system():
        return Windows()

    @staticmethod
    def from_grapejuice():
        raise RuntimeError("Grapejuice is not available on Windows.")

    def run(
        self,
        args: list[str] | str,
        prefix: str = None,
        env: dict = None,
        shell: bool = False,
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(args=args, env=env, shell=shell)

    def winedbg(
        self,
        args: list[str] | str,
        prefix: str = None,
        env: dict = None,
        shell: bool = False,
    ) -> subprocess.CompletedProcess[bytes]:
        raise RuntimeError("Not available on Windows.")
