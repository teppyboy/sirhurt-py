from pathlib import Path
from sirhurt.roblox import RobloxProcess


class InjectedClient:
    """Roblox client wrapper for SirHurt"""

    def __init__(self, roblox: RobloxProcess, target_file: Path) -> None:
        self._roblox = roblox
        self._target_file = target_file

    def execute(self, script: str):
        if not self._roblox.is_process_alive():
            raise RuntimeError("Associated Roblox process is dead.")
        self._target_file.write_text(script)
