import os
# import sys
# import time
import psutil

def computer_sleep(hibernate=False) -> None:
    """Function will put the computer in sleep mode.

    Implemented for `WINDOWS 10`.
    
    ## TODO:
    ---
    - Write `hibernate` implementation for OSX
    - Test `sleep` implementation for OSX and LINUX
    - Test `hibernate` implementation for LINUX
    - Write implementation for a blocking mode, where the program is blocked until it happened and the pc woke up again

    ## Args:
    ---
    - `hibernate` When `true` the computer tries to hibernate in stead of sleeping
    ## Returns:
    ---
    `None`  

    This code is non-blocking
    """
    
    if psutil.OSX:
        os.system("pmset sleepnow")
    elif psutil.LINUX:
        if hibernate:
            os.system("systemctl hibernate")
        else:
            os.system("systemctl suspend")
    elif psutil.WINDOWS:
        # Check the current power-plan for issues
        if hibernate:
            os.system(f'powercfg /hibernate ON')

        os.system(f"rundll32.exe powrprof.dll,SetSuspendState {int(hibernate)},1,0")
    else:
        raise RuntimeError("I have no implementation for that operating system :'(")
def computer_shutdown(reboot=False, force=False, seconds_delay=0, message="") -> None:
    """Function will put the computer in sleep mode.

    Implemented for WINDOWS.
    #### TODO:
    ---
    - Write implementation for OSX
    - Write implementation for LINUX of `seconds_delay`
    - Test LINUX

    #### Args:
    ---
    - `reboot` When `true` the system will restart after shutdown.
    - `force` When `true` kills all applications and does not give them time to save their data. DANGEROUS
    - `seconds_delay` The amount of seconds that the system will have to wait before actually shutting down. You want to use this if you use `message`.
    - `message` The message you want the user to read when this command is called.
    #### Returns:
    ---
    `None`
    """
    if psutil.LINUX:
        # NOTE: LINUX has no `seconds_delay`
        command = "systemctl reboot" if reboot else "systemctl poweroff"
        if force: command += " --force"
        if message != "": command+=f' --message={message}'
    elif psutil.WINDOWS:
        command = "shutdown"
        command += " /r" if reboot else " /s"
        if force: command += " /f"
        if seconds_delay > 0: command += f" /t {int(seconds_delay)}"
        if message != "": command += f' /c {str(message)}'
        os.system(command)
    else:
        raise RuntimeError("I have no implementation for that operating system :'(")
# def computer_hostage(function) -> None:
#     """
#     # ! Work In Progress ! COMING SOON !
#     A blocking code that will keep the computer hostage.
#     As soon as:
#     - you move the mouse
#     - you type on the keyboard
#     - add / remove devices from device manager
#     This `computer_hostage`-function will call `function`.
#     It does only happen once.
    
#     This can be used for example to `computer_hostage(function=computer_shutdown)` to shutdown the computer as something happens.
#     This way you can display your computer, but as soon as someone tries to use the computer it shuts down.
    
#     Implemented for WINDOWS.
#     #### TODO:
#     ---
#     - Checking the mouse with https://pythonhosted.org/pynput/mouse.html#controlling-the-mouse
#     - Listen for devices https://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python 
#     - Listen for Keyboard strokes https://pythonhosted.org/pynput/ https://stackoverflow.com/questions/24072790/how-to-detect-key-presses 
#     - 
#     """
#     print("Feature coming soon.")
#     pass
def computer_lock() -> None:
    """Locks your computer.
    
    Implemented for WINDOWS.
    #### TODO:
    ---
    - Implement for Linux ???
    - Test OSX
    """
    if psutil.OSX:
        os.system("pmset displaysleepnow")
    elif psutil.WINDOWS:
        os.system(f"Rundll32.exe user32.dll,LockWorkStation")
    else:
        raise RuntimeError("I have no implementation for that operating system :'(")
    pass
if __name__ == '__main__':
    computer_sleep(hibernate=True)
