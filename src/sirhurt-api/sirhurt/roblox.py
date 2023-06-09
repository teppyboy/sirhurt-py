import os
import psutil
from importlib.util import find_spec
from threading import Thread
from pathlib import Path
from sirhurt.helpers import unix_to_wine_pid, get_wine_from_pid
from sirhurt.wine import Wine


class RobloxProcess:
    """
    Manage Roblox process
    """

    def __init__(self, pid: int, wine_pid: int, prefix: str, wine: Wine) -> None:
        self._proc = psutil.Process(pid=pid)
        self._wine_pid = wine_pid
        self._wine = wine
        self._prefix = prefix
        self._pid = pid

    def inject(self, dll: os.PathLike, onclose=None):
        injector_bin = Path(find_spec(__name__).origin).parent.joinpath(
            "bin/injector.exe"
        )
        self._wine.run(
            [
                str(injector_bin),
                "--pid",
                str(self._wine_pid),
                "--dll",
                f"Z:/{str(dll)}",
            ],
            prefix=self._prefix,
        ).check_returncode()

        # Waits for process to exit and do cleanup
        def hook():
            self._proc.wait()
            if onclose:
                onclose()

        Thread(target=hook).start()

    def is_process_alive(self):
        return psutil.pid_exists(pid=self._pid)

    def close(self):
        self._proc.terminate()

    def kill(self):
        self._proc.kill()

    @staticmethod
    def get_roblox_processes() -> list["RobloxProcess"]:
        rbx_procs = []
        for proc in psutil.process_iter(["pid", "name"]):
            # Sometimes the process miss the last character and the extension
            if "RobloxPlayerBet" in proc.name():
                env = proc.environ()
                rbx_procs.append(
                    RobloxProcess(
                        pid=proc.pid,
                        wine_pid=unix_to_wine_pid(proc.pid)["pid"],
                        prefix=env.get("WINEPREFIX", "~/.wine"),
                        wine=get_wine_from_pid(proc.pid),
                    )
                )
        return rbx_procs

    @staticmethod
    # No return types to fix TypeError:
    # TypeError: unsupported operand type(s) for |: 'str' and 'NoneType'
    def get_roblox_process():
        """
        Returns:
            RobloxProcess if it found a Roblox process, otherwise None
        """
        for proc in psutil.process_iter(["pid", "name"]):
            # Sometimes the process miss the last character and the extension
            if "RobloxPlayerBet" in proc.name():
                env = proc.environ()
                return RobloxProcess(
                    pid=proc.pid,
                    wine_pid=unix_to_wine_pid(proc.pid)["pid"],
                    prefix=env.get("WINEPREFIX", "~/.wine"),
                    wine=get_wine_from_pid(proc.pid),
                )
