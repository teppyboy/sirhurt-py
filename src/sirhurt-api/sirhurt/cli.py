import argparse
from pathlib import Path
from sirhurt import Exploit, RobloxProcess

exploit = Exploit()
rbx_proc: RobloxProcess = None


def find_process():
    procs = RobloxProcess.get_roblox_processes()
    if len(procs) == 0:
        print("Couldn't find any Roblox processes, is Roblox running?")
        return
    print("Available Roblox processes:")
    for i, v in enumerate(procs):
        print(f"[{i}]: {v._pid}")


def set_process(index):
    global rbx_proc
    try:
        index = int(index)
    except ValueError:
        print("Index must be a number.")
        return
    procs = RobloxProcess.get_roblox_processes()
    if len(procs) == 0:
        print("Couldn't find any Roblox processes, is Roblox running?")
        return
    try:
        rbx_proc = procs[index]
    except IndexError:
        print("Index out of range, use 'find-process' to get process list.")
        return
    print(f"Set current Roblox process to: {rbx_proc._pid}")
    return rbx_proc


def check_alive(noisy=False):
    global rbx_proc
    if rbx_proc is None or not rbx_proc.is_process_alive():
        print("Current Roblox process is dead.")
        rbx_proc = None
        return False
    if noisy:
        print("Current Roblox process is alive.")
    return True


def close_proc():
    global rbx_proc
    if not check_alive():
        return
    rbx_proc.close()
    rbx_proc = None
    print("Closed current Roblox process.")


def inject():
    if not check_alive():
        return
    print("Injecting...")
    exploit.inject(roblox=rbx_proc)
    print("Sucessfully injected.")


def update_dll():
    print("Checking for update...")
    if not exploit.is_update_available():
        print("DLL is already the latest version.")
        return
    print("Updating DLL...")
    exploit.download_dll()
    print("Update completed.")


def execute_file(file):
    if not check_alive():
        return
    fp = Path(file)
    if not fp.is_file():
        print(f"{file} doesn't exist/is not a file.")
        return
    rbx_proc.execute(fp.read_text())
    print("Execution success.")


def loadstring(string):
    if not check_alive():
        return
    rbx_proc.execute(string)
    print("Execution success.")

def parse_args(args: list[str]):
    global rbx_proc
    try:
        command = args[0].lower()
        try:
            if args[1].lower() == "proc":
                if command in ["find"]:
                    find_process()
                elif command in ["set"]:
                    rbx_proc = set_process(args[2])
                elif command in ["check"]:
                    rbx_proc = (
                        None if not check_alive(noisy=True) else rbx_proc
                    )
                elif command in ["close"]:
                    close_proc()
                else:
                    print("Invalid command:", args[0], args[1])
                return
        except Exception:
            pass
        if command in ["find-process", "find-proc", "fp"]:
            find_process()
        elif command in ["set-process", "set-proc", "sp"]:
            rbx_proc = set_process(args[1])
        elif command in ["check-process", "check-proc", "cp"]:
            rbx_proc = (
                None if not check_alive(noisy=True) else rbx_proc
            )
        elif command in ["close-process", "close-roblox", "close"]:
            close_proc()
        elif command in ["update", "upd8", "ud"]:
            update_dll()
        elif command in ["inject", "ij"]:
            inject()
        elif command in ["execute file", "execfile", "file"]:
            execute_file(file=args[1])
        elif command in ["execute", "exec"]:
            loadstring(string=" ".join(args[1:]))
        elif command in ["exit"]:
            print("Exiting from interactive console...")
            exit(0)
        else:
            print("Invalid command:", args[0])
    except IndexError:
        print("Error: The command has unfilled args.")
    except Exception as e:
        print("Error:", e)

def console():
    print("Welcome to SirHurt API interactive console!")
    print("To get started, type 'help' to show commands list.")
    while True:
        try:
            inp = input("> ")
        except KeyboardInterrupt:
            # Trigger newline
            print()
            print("Exiting from interactive console...")
            break
        args = inp.split(" ")
        parse_args(args=args)


def main():
    console()
