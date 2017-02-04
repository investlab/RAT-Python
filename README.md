# basicRAT

This is a Python RAT (Remote Access Trojan). basicRAT was created to maintain a clean design full-featured Python RAT. Currently a work in progress and still being hacked on.

**Disclaimer: This RAT is for research purposes only, and should only be used on authorized systems. Accessing a computer system or network without authorization or explicit permission is illegal.**

## Features
* Cross-platform
* AES CBC encrypted C2 with D-H exchange
* Reverse shell
* File upload/download
* Standard utilities (wget, unzip)

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
* Scanning utility
* Password dumping (mimikatz / gsecdump)
* Tunneling
* System survey
* Client periodic connection attempt
* Accept connection from multiple clients

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

basicRAT server listening on port 1337...

[127.0.0.1] basicRAT> help

download <files>    - Download file(s).
help                - Show this help menu.
persistence         - Apply persistence mechanism.
quit                - Gracefully kill client and server.
rekey               - Regenerate crypto key.
run <command>       - Execute a command on the target.
unzip <file>        - Unzip a file.
upload <files>      - Upload files(s).
wget <url>          - Download a file from the web.

[127.0.0.1] basicRAT> run uname -a
Linux sandbox3 4.8.13-1-ARCH #1 SMP PREEMPT Fri Dec 9 07:24:34 CET 2016 x86_64 GNU/Linux
```

## Authors
* Austin Jackson [@vesche](https://github.com/vesche)
* Skyler Curtis [@deadPix3l](https://github.com/deadPix3l)

## Other open-source Python RATs for Reference
* [ahhh/Reverse_DNS_Shell](https://github.com/ahhh/Reverse_DNS_Shell)
* [sweetsoftware/Ares](https://github.com/sweetsoftware/Ares)
