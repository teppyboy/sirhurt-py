from pathlib import Path

import psutil

from sirhurt.wine import Wine


def get_proc_env(pid: int):
    """
    Obsolete, use psutil.Process(...).environ() instead
    """
    environ_file = Path(f"/proc/{str(pid)}/environ")
    if not environ_file.is_file():
        raise FileNotFoundError(f"Process {pid} environ file not found.")
    proc_env = {}
    for line in environ_file.read_text().split("\0"):
        try:
            env = line.split("=", 1)
            proc_env[env[0]] = env[1]
        except Exception:
            continue
    return proc_env

def get_wine_procs_ids(wine: Wine) -> list[dict[str, str | int]]:
    dbg_out = wine.winedbg('--command "info proc"', env={
        "WINEDEBUG": "-all"
    }, shell=True)
    procs = []
    dbg_out.check_returncode()
    for line in dbg_out.stdout.decode().split("\n"):
        props = line.split(" ")
        try:
            if "=" in props[0]:
                pid = int(props[0][1:], 16)
                threads = int(props[1])
            else:
                pid = int(props[1], 16)
                threads = int(props[2])
            name = props[-1][1:-1]
        except (ValueError, IndexError):
            continue
        procs.append({
            "name": name,
            "pid": pid,
            "threads": threads
        })
    return procs

def get_wine_from_pid(pid: int) -> Wine | None:
    proc_env = psutil.Process(pid=pid).environ()
    prefix = proc_env["WINEPREFIX"] or "~/.wine"
    # .../<wine>/bin/wine and we need the <wine> path
    wine_path = Path(proc_env["WINELOADER"]).parent.parent
    wine = Wine(wine=wine_path, prefix=prefix)
    return wine

def unix_to_wine_pid(pid: int) -> dict | None:
    proc = psutil.Process(pid=pid)
    wine = get_wine_from_pid(pid=pid)    
    wine_procs = get_wine_procs_ids(wine=wine)
    for wine_proc in wine_procs:
        if proc.name() in wine_proc["name"]:
            # Also return the Wine instance because the wine PID is local to that prefix
            return {
                "pid": wine_proc["pid"],
                "wine": wine 
            }
    return
