import os
import ctypes
import winreg
import sys
# running the python file as administrator
def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# read operation in windows registry 
def read(root_key, subkey, value_name):
    try:
        with winreg.OpenKey(root_key, subkey) as key:
            value, _ = winreg.QueryValueEx(key, value_name)
            return value
    except Exception as e:
        print(f"Error while reading registry value: {e}")
        return None

# write operation in windows registry
def write(root_key, subkey, value_name, value, value_type):
    try:
        with winreg.OpenKey(root_key, subkey, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value)
        print("Registry value written successfully.")
    except Exception as e:
        print(f"Error writing registry value: {e}")

# blocking the usb by changing/modifying the registry
def block_usb():
    try:
        key_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
        print("USB ports disabled.")
    except Exception as e:
        print(f"Error disabling USB ports: {e}")

# disabling bluetooth by changing/modifying its service in the registry
def disable_bluetooth():
    try:
        os.system("sc config bthserv start= disabled")
        print("Bluetooth is disabled.")
    except Exception as e:
        print(f"Error while disabling Bluetooth: {e}")

# disabling the command prompt by changing/modifying the registry
def disable_command_prompt():
    try:
        # set the registry key to restrict cmd prompt
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\System"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 2)
        print("Command Prompt is disabled.")
    except Exception as e:
        print(f"Error while disabling Command Prompt: {e}")

# blocking access to websites by modifying hosts file
def block_website(website):
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts_path, "a") as hosts_file:
            hosts_file.write(f"127.0.0.1 {website}\n")
        print(f"Access to {website} blocked.")
    except Exception as e:
        print(f"Error blocking website: {e}")

if __name__ == "__main__":
    run_as_admin()
    block_usb()
    disable_bluetooth()
    disable_command_prompt()
    block_website("facebook.com")

    # notifying the user to restart the pc for changes to take effect
    ctypes.windll.user32.MessageBoxW(0, "Security measures applied. Please restart your computer.", "Restart Required", 1)
    # read and write functions for registry values
    root_key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\MyApp"
    value_name = "MyValue"
    value_type = winreg.REG_SZ
    value = "Hello, Registry!"
    # writing the registry value
    write(root_key, subkey, value_name, value, value_type)
    # reading the registry value
    read_value = read(root_key, subkey, value_name)
    if read_value is not None:
        print(f"Read value: {read_value}")
