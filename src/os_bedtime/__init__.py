import os
# import sys
# import time
import psutil

def computer_sleep(hibernate=False, wake_up_events_disabled=False) -> None:
    """Function will put the computer in sleep mode.

    Implemented for WINDOWS.
    #### TODO:
    ---
    - Write `hibernate` implementation for OSX
    - Write `wake_up_events_disabled` for OSX and LINUX
    - Test `sleep` implementation for OSX and LINUX
    - Test `hibernate` implementation for LINUX
    - Write implementation for a blocking mode, where the program is blocked until it happened and the pc woke up again

    #### Args:
    ---
    - `hibernate` When `true` the computer tries to hibernate in stead of sleeping
    - `wake_up_events_disabled` When `true` the computer will not randomly* wake up. PS: It is not random, they are timer events often or another computer is trying to talk to you. But in the case of True you ignore all those events and the computer will only wake up because of the power-button being pressed. 
    #### Returns:
    ---
    `None`
    """
    
    if psutil.OSX:
        os.system("pmset sleepnow")
    elif psutil.LINUX:
        if hibernate:
            os.system("systemctl hibernate")
        else:
            os.system("systemctl suspend")
    elif psutil.WINDOWS:
        os.system(f"rundll32.exe powrprof.dll,SetSuspendState {int(hibernate)},1,{int(wake_up_events_disabled)}")
    else:
        raise RuntimeError("I have no implementation for that operating system :'(")
def computer_shutdown(reboot=False, force=False, seconds_delay=0, message="") -> None:
    """Function will put the computer in sleep mode.

    Implemented for WINDOWS.
    #### TODO:
    ---
    - Write implementation for OSX and LINUX

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
    if psutil.WINDOWS:
        command = "shutdown"
        command += " /r" if reboot else " /s"
        if force: command += " /f"
        if seconds_delay > 0: command += f" /t {int(seconds_delay)}"
        if message != "": command += f' /c {str(message)}'
        os.system(command)
    else:
        raise RuntimeError("I have no implementation for that operating system :'(")