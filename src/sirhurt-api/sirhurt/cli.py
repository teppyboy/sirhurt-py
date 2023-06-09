import readline  # Enable input() additional features
import tkinter as tk
import tkinter.messagebox as msgbox
from threading import Thread
from requests import Session
from pathlib import Path
from sirhurt import Exploit, RobloxProcess, InjectedClient

exploit = Exploit()
rbx_proc: RobloxProcess = None
client: InjectedClient = None
session = Session()

commands = []


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
    global client
    if rbx_proc is None or not rbx_proc.is_process_alive():
        print("Current Roblox process is dead.")
        rbx_proc = None
        client = None
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
    global client
    if not check_alive():
        return
    print("Injecting...")
    client = exploit.inject(roblox=rbx_proc)
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
    client.execute(fp.read_text())
    print("Execution success.")


def execute_url(url):
    if not check_alive():
        return
    client.execute(session.get(url=url).text)
    print("Execution from Url success.")


def execute_gui():
    window = tk.Tk()
    script_box = tk.Text()
    script_box.pack()

    def _exec(*args, **kwargs):
        if rbx_proc is None or not rbx_proc.is_process_alive():
            msgbox.showerror(title="Error", message="Not injected.")
            return
        script = script_box.get("1.0", tk.END)
        client.execute(script)

    exec_btn = tk.Button(text="Execute", command=_exec)
    exec_btn.pack()
    window.mainloop()


def loadstring(string):
    if not check_alive():
        return
    client.execute(string)
    print("Execution success.")


def parse_args(args: list[str]):
    global rbx_proc
    global client
    try:
        command = args[0].lower()
        try:
            if args[1].lower() == "proc":
                if command in ["find"]:
                    find_process()
                elif command in ["set"]:
                    rbx_proc = set_process(args[2])
                elif command in ["check"]:
                    rbx_proc = client = (
                        None if not check_alive(noisy=True) else rbx_proc
                    )
                elif command in ["close"]:
                    close_proc()
                else:
                    print("Invalid command:", args[0], args[1])
                return
            elif args[1].lower() == "file":
                if command in ["execute", "exec"]:
                    execute_file(file=args[2])
                return
            elif args[1].lower() == "url":
                if command in ["execute", "exec"]:
                    execute_url(url=args[2])
                return
        except IndexError:
            pass
        if command in ["find-process", "find-proc", "fp"]:
            find_process()
        elif command in ["set-process", "set-proc", "sp"]:
            rbx_proc = set_process(args[1])
        elif command in ["check-process", "check-proc", "cp"]:
            rbx_proc = client = None if not check_alive(noisy=True) else rbx_proc
        elif command in ["close-process", "close-roblox", "close"]:
            close_proc()
        elif command in ["update", "upd8", "ud", "download", "dl"]:
            update_dll()
        elif command in ["inject", "ij"]:
            inject()
        elif command in ["execute-file", "execfile", "file"]:
            execute_file(file=args[1])
        elif command in ["execute-url", "execurl", "url"]:
            execute_url(url=args[1])
        elif command in ["execute-gui", "execgui", "gui"]:
            Thread(target=execute_gui, daemon=True).run()
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
