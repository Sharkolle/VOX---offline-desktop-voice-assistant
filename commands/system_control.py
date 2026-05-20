# commands/system_control.py

# 🖥️ This module handles VOX's system control commands.
# Functions include:
# - Shutdown, Restart, Logout, Lock, Sleep
# - Screenshot capture
# - Empty recycle bin
# - Control volume (up/down/mute)
# - Play/Pause media
#
# Works across Windows, Linux, and macOS wherever possible.

import os
import platform
from core.voice_recognition import listen_and_recognize
from commands.speak import speak
import subprocess


def confirm_action(action: str) -> bool:
    """
    Confirms if the user really wants to perform a sensitive system action.

    Args:
        action (str): The action being confirmed (e.g., "shutdown")

    Returns:
        bool: True if confirmed, False otherwise.
    """
    print(f"Are you sure you want to {action}? Say 'yes' to confirm or 'no' to cancel.")
    speak(f"Say yes to {action} your system or no to cancel.")

    while True:
        confirmation = listen_and_recognize()
        if confirmation is None:
            print("No response detected. Please try again.")
            continue

        confirmation = confirmation.strip().lower()
        if "yes" in confirmation:
            return True
        elif "no" in confirmation:
            return False
        else:
            print("Invalid response. Please say 'yes' to confirm or 'no' to cancel.")


def shutdown_system():
    if not confirm_action("shutdown"):
        return {"text": "Shutdown canceled.", "speak": "Shutdown request canceled."}

    system = platform.system()
    if system == "Windows":
        os.system("shutdown /s /t 5")
    elif system in ["Linux", "Darwin"]:
        os.system("shutdown -h now")
    else:
        return {"text": "Shutdown not supported.", "speak": "Sorry, I can't shut down this system."}

    return {"text": "Shutting down in 5 seconds...", "speak": "Powering down in 5 seconds. Goodbye!"}


def restart_system():
    if not confirm_action("restart"):
        return {"text": "Restart canceled.", "speak": "Restart request canceled."}

    system = platform.system()
    if system == "Windows":
        os.system("shutdown /r /t 5")
    elif system in ["Linux", "Darwin"]:
        os.system("shutdown -r now")
    else:
        return {"text": "Restart not supported.", "speak": "Sorry, I can't restart this system."}

    return {"text": "Restarting in 5 seconds...", "speak": "System restart in 5 seconds. Hold tight!"}


def logout_system():
    if not confirm_action("log out"):
        return {"text": "Logout canceled.", "speak": "Logout request canceled."}

    system = platform.system()
    if system == "Windows":
        os.system("shutdown /l")
    elif system in ["Linux", "Darwin"]:
        os.system("pkill -KILL -u $USER")
    else:
        return {"text": "Logout not supported.", "speak": "Sorry, I can't log out from this system."}

    return {"text": "Logging out...", "speak": "Logging out now!"}


def lock_system():
    system = platform.system()
    if system == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif system == "Linux":
        os.system("gnome-screensaver-command -l")
    elif system == "Darwin":
        os.system("/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession -suspend")
    else:
        return {"text": "Lock not supported.", "speak": "Sorry, I can't lock this system."}

    return {"text": "Locking system...", "speak": "System locked!"}


def sleep_system():
    system = platform.system()
    if system == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif system == "Linux":
        os.system("systemctl suspend")
    elif system == "Darwin":
        os.system("pmset sleepnow")
    else:
        return {"text": "Sleep not supported.", "speak": "Sorry, I can't put this system to sleep."}

    return {"text": "Putting system to sleep...", "speak": "Goodnight."}


def take_screenshot():
    system = platform.system()
    if system == "Windows":
        os.system("powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')\"")
    elif system == "Linux":
        os.system("gnome-screenshot")
    elif system == "Darwin":
        os.system("screencapture -i ~/Desktop/screenshot.png")
    else:
        return {"text": "Screenshot not supported.", "speak": "Sorry, I can't take screenshots on this system."}

    return {"text": "Taking screenshot...", "speak": "Screenshot taken!"}


def empty_recycle_bin():
    if not confirm_action("empty the recycle bin"):
        return {"text": "Canceled.", "speak": "Recycle bin request canceled."}

    system = platform.system()
    try:
        if system == "Windows":
            os.system("powershell -command \"Clear-RecycleBin -Force\"")
        elif system == "Linux":
            os.system("trash-empty")
        elif system == "Darwin":
            os.system("rm -rf ~/.Trash/*")
        else:
            return {"text": "Empty bin not supported.", "speak": "Sorry, I can't empty the recycle bin on this system."}

        return {"text": "Recycle bin emptied.", "speak": "Recycle bin has been emptied."}
    except OSError as e:
        print(f"Error emptying recycle bin: {e}")


def volume_up():
    system = platform.system()
    if system == "Windows":
        os.system("powershell -command \"(New-Object -ComObject WScript.Shell).SendKeys([char]175)\"")
    elif system == "Linux":
        os.system("amixer -D pulse sset Master 5%+")
    elif system == "Darwin":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 5)'")
    return {"text": "Volume increased", "speak": "Volume turned up"}


def volume_down():
    system = platform.system()
    if system == "Windows":
        os.system("powershell -command \"(New-Object -ComObject WScript.Shell).SendKeys([char]174)\"")
    elif system == "Linux":
        os.system("amixer -D pulse sset Master 5%-")
    elif system == "Darwin":
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 5)'")
    return {"text": "Volume decreased", "speak": "Volume turned down"}


def mute_volume():
    system = platform.system()
    if system == "Windows":
        os.system("nircmd mutesysvolume 2")
    elif system == "Linux":
        os.system("amixer -D pulse set Master 1+ toggle")
    elif system == "Darwin":
        os.system("osascript -e 'set volume output muted true'")
    return {"text": "Volume muted", "speak": "Sound muted"}


def play_pause_media():
    system = platform.system()
    if system == "Windows":
        os.system("nircmd sendkey 0xB3 press")
    elif system == "Linux":
        os.system("playerctl play-pause")
    elif system == "Darwin":
        os.system("osascript -e 'tell application \"System Events\" to key code 16'")
    return {"text": "Media play/pause", "speak": "Media toggled"}


def toggle_wifi():
        system = platform.system()
        if system == "Windows":
            os.system("netsh interface set interface \"Wi-Fi\" admin=enable")
            # Enable would use admin=enable
        elif system == "Linux":
            os.system("nmcli radio wifi off")
        elif system == "Darwin":
            os.system("networksetup -setairportpower en0 off")
        return {
            "text": "Wi-Fi toggled",
            "speak": "Wireless network adjusted"
        }

def brightness_adjust(level="up"):
        system = platform.system()
        if system == "Windows":
            try:
                import screen_brightness_control as sbc
                current = sbc.get_brightness()[0]
                new = min(100, current + 10) if level == "up" else max(0, current - 10)
                sbc.set_brightness(new)
            except:
                return {
                    "text": "Install screen-brightness-control package for Windows",
                    "speak": "Brightness control requires additional software"
                }
        elif system == "Linux":
            os.system(f"brightnessctl set 10%{'+' if level == 'up' else '-'}")
        elif system == "Darwin":
            os.system(f"brightness {'1' if level == 'up' else '-1'}")

        return {
            "text": f"Brightness turned {level}",
            "speak": f"Screen brightness {level}"
        }


def toggle_bluetooth(state="toggle"):
    system = platform.system()

    if system == "Windows":
        if state == "toggle":
            os.system(
                "powershell -command \"$bt = Get-WmiObject -Class Win32_DeviceEnable -ErrorAction Stop; $bt.Enable = !$bt.Enable; $bt.Put()\"")
        else:
            enable = 1 if state == "on" else 0
            os.system(f"powershell -command \"(New-Object -ComObject Shell.Application).ServiceStop('bthserv', 0)\"")
            os.system(f"powershell -command \"(Get-WmiObject -Class Win32_DeviceEnable).Enable = {enable}; $_.Put()\"")
    elif system == "Linux":
        if state == "toggle":
            os.system("bluetoothctl power on" if "no" in os.popen(
                "bluetoothctl show | grep Powered").read() else "bluetoothctl power off")
        else:
            os.system(f"bluetoothctl power {'on' if state == 'on' else 'off'}")
    elif system == "Darwin":
        if state == "toggle":
            current = os.popen("blueutil -p").read().strip()
            new_state = "0" if current == "1" else "1"
            os.system(f"blueutil -p {new_state}")
        else:
            os.system(f"blueutil -p {'1' if state == 'on' else '0'}")
    else:
        return {
            "text": "Bluetooth control not supported",
            "speak": "Can't control Bluetooth on this system"
        }

    return {
        "text": f"Bluetooth turned {'on' if state == 'on' or state == 'toggle' else 'off'}",
        "speak": f"Bluetooth {'enabled' if state == 'on' or state == 'toggle' else 'disabled'}"
    }


def check_system_updates():
    system = platform.system()
    response = {"text": "", "speak": ""}

    if system == "Windows":
        result = os.popen("powershell -command \"Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot\"").read()
        response["text"] = "Windows updates checked: " + result[:200]
        response["speak"] = "Checked for Windows updates"
    elif system == "Linux":
        if os.path.exists("/etc/apt/sources.list"):
            result = os.popen("sudo apt update && sudo apt list --upgradable").read()
            response["text"] = "Available updates: " + result[:200]
            response["speak"] = "Checked for system updates"
        else:
            response["text"] = "Only APT-based systems supported"
            response["speak"] = "Update check not supported"
    elif system == "Darwin":
        result = os.popen("softwareupdate -l").read()
        response["text"] = "Available macOS updates: " + result[:200]
        response["speak"] = "Checked for macOS updates"
    else:
        response["text"] = "Update check not supported"
        response["speak"] = "Can't check updates on this system"

    return response


def run_system_diagnosis():
    system = platform.system()
    report = {"text": "System Diagnosis Report\n", "speak": "System diagnosis completed"}

    if system == "Windows":
        report["text"] += "OS Version: " + platform.version() + "\n"
        report["text"] += "Disk Space: " + os.popen("wmic logicaldisk get size,freespace,caption").read() + "\n"
        report["text"] += "Memory: " + os.popen("systeminfo | findstr Memory").read() + "\n"
    elif system == "Linux":
        report["text"] += "OS: " + os.popen("lsb_release -d").read() + "\n"
        report["text"] += "Disk: " + os.popen("df -h").read() + "\n"
        report["text"] += "Memory: " + os.popen("free -h").read() + "\n"
    elif system == "Darwin":
        report["text"] += "OS: " + os.popen("sw_vers -productVersion").read() + "\n"
        report["text"] += "Disk: " + os.popen("df -h").read() + "\n"
        report["text"] += "Memory: " + os.popen("top -l 1 -s 0 | grep PhysMem").read() + "\n"

    return report



