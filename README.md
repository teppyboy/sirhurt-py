# sirhurt-py

SirHurt API written in Python (+Rust for the injector)

## Features

sirhurt-py is a fairly new project, but it can cover most use cases:
+ **Linux support!**
+ Find Roblox processes
+ Inject the exploit
+ Execute scripts
+ Multiple instances* 

> <sub>* Multiple Roblox in single Wine prefix/Windows isn't implemented yet but 
> you can use other tools like "Multiple Roblox" from WeAreDevs to do that</sub>

## Installation

### From source

> **Warning**

> For the DLL injector to compile, you must have Rust *nightly*, if you don't and you're using `rustup` then to install the nightly toolchain:
>
> ```bash
> rustup default nightly
>```

Assuming you have [`poetry`](https://python-poetry.org/) installed:
> **Warning**

> Building injector requires `cargo` to be installed.

```bash
git clone https://github.com/teppyboy/sirhurt-py/
cd sirhurt-py
poetry install
poetry shell
# If you don't want to build the injector:
# ,/build.py --no-module --no-injector
./build.py --no-module
# Then you can run sirhurt-api from source dir (./src/sirhurt-api)
# by importing "sirhurt"
```

## Usage

Here's a simple Python code that find Roblox processes, inject SirHurt and execute `print("Hello world!")`

```py
from sirhurt import RobloxProcess, Exploit, InjectedClient

exploit: Exploit = Exploit()
exploit.download_dll()
roblox: RobloxProcess = RobloxProcess.get_roblox_process()
client: InjectedClient = exploit.inject(roblox=roblox)
client.execute('print("Hello world!")')
```

## FAQ

### 1. Why?

This API has native Linux support for SirHurt as well as automatically do all the hard work for you (finding Roblox process
in Linux and Wine and map them together, inject the exploit, multiple instances through symlinks)

## License

[MIT](./LICENSE)
