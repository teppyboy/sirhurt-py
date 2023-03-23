#!/usr/bin/env python3
from pathlib import Path
from shutil import copy2
import subprocess
import sys


def run(args, cwd = Path.cwd()):
    print(f"> {args}")
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        cwd=cwd
    )
    for line in proc.stdout:
        print(line.decode(), end="")
    return proc


def build_injector(release: bool = False, strip: bool = False):
    injector_path = Path("./src/injector/")
    if release:
        print("Building injector in release mode...")
        run("cargo build --release --target x86_64-pc-windows-gnu", cwd=str(injector_path))
        bin_path = injector_path.joinpath("target/x86_64-pc-windows-gnu/release/injector.exe")
    else:
        print("Building injector in debug mode...")
        run("cargo build --target x86_64-pc-windows-gnu", cwd=str(injector_path))
        bin_path = injector_path.joinpath("target/x86_64-pc-windows-gnu/debug/injector.exe")
    if strip:
        print("Stripping binary...")
        run(f"strip {str(bin_path)}")
    return bin_path


def build_module(bin_path: Path | None):
    if bin_path:
        module_path = Path("./src/sirhurt-api")
        print("Copying injector binary to module...")
        copy2(bin_path, module_path.joinpath("sirhurt/bin/injector.exe"))
    print("Building module...")
    run("poetry build", cwd=module_path)

def main():
    release = False
    strip = False
    module = True
    injector = True
    if "--release" in sys.argv:
        release = True
        print("Release build enabled.")
    if "--strip" in sys.argv:
        strip = True
        print("Stripping enabled.")
    if "--no-module" in sys.argv:
        module = False
        print("Python module will not be built.")
    if "--no-injector" in sys.argv:
        injector = False
        print("Rust injector will not be built.")
    bin_path = None
    if injector:
        bin_path = build_injector(release=release, strip=strip)
    if module:
        build_module(bin_path=bin_path)
    print("Done.")


if __name__ == "__main__":
    main()
