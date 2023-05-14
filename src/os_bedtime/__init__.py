import os
import time
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
def computer_hostage(function, listen_mouse=True, verbose=False) -> None:
    import threading
    import ctypes
    """
    # ! Work In Progress ! COMING SOON !
    A blocking code that will keep the computer hostage.
    As soon as:
    - you move the mouse
    - you type on the keyboard
    - add / remove devices from device manager
    This `computer_hostage`-function will call `function`.
    It does only happen once.
    
    This can be used for example to `computer_hostage(function=computer_shutdown)` to shutdown the computer as something happens.
    This way you can display your computer, but as soon as someone tries to use the computer it shuts down.
    
    Implemented for WINDOWS.
    #### TODO:
    ---
    - Checking the mouse with https://pythonhosted.org/pynput/mouse.html#controlling-the-mouse
    - Listen for devices https://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python 
    - Listen for Keyboard strokes https://pythonhosted.org/pynput/ https://stackoverflow.com/questions/24072790/how-to-detect-key-presses 
    - 
    """
    def on_move(x, y):
        if verbose: print(f'Pointer moved to ({x}, {y})')
        return False
    def on_click(x, y, button, pressed):
        if verbose: print(f'{"Pressed" if pressed else "Released"} at ({x}, {y})')
        return False
    def on_scroll(x, y, dx, dy):
        if verbose: print('Scrolled ({x}, {y})')
        return False
    
    class StopableThread(threading.Thread): # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
        def __init__(self, function, verbose=False):
            threading.Thread.__init__(self)
            self.function = function
            self.verbose = verbose
        def run(self):
            """Overwrite this function"""
            pass
        def get_id(self):
            # returns id of the respective thread
            if hasattr(self, '_thread_id'):
                return self._thread_id
            for id, thread in threading._active.items():
                if thread is self:
                    return id
        def stop_thread(self):
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')
    class MouseListener(StopableThread):
        def run(self):
            from pynput.mouse import Listener
            try:
                with Listener(
                    on_move=on_move,
                    on_click=on_click,
                    on_scroll=on_scroll) as listener:
                        listener.join()
                if verbose: print('Mouse trigger')
                self.function()
            finally: pass

    if listen_mouse:
        mouse_listener = MouseListener(function)
        mouse_listener.start()
        time.sleep(5)
        mouse_listener.stop_thread()
        mouse_listener.join()
if __name__ == '__main__':
    computer_hostage(computer_lock, verbose=True)
