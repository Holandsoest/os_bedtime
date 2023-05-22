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
        if message != "": command += f' /c {message}'
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
def computer_hostage(function, listen_mouse=True, listen_keyboard=True, timeout_seconds=-1, verbose=False) -> bool:
    """A blocking code that can keep the computer hostage for input devices.
    ## args
    - `function` If the mouse_listener, keyboard_listener or event_listener get a trigger it will run this function. You can use a lambda to also parse in arguments.  
    - `listen_mouse` When `True` (default): runs the `function` if you scroll, move or click your mouse.
    - `listen_keyboard` When `True` (default): runs the `function` if you press or release a key on your keyboard.
    - `timeout_seconds` (int) after this amount of seconds the listeners will stop without calling the `function` and it will `return False`  
    negative numbers will result in 100 years of delay.
    - `verbose` (default=False) When `True`: Causes this script to explain what triggered it with `print()`s
    ## returns
    - `True` if a listener got triggered.
    - `False` if the `timeout_seconds` timer expired.
    - This function is blocking
    
    This can be used for example to `computer_hostage(function=lambda:computer_shutdown(seconds_delay=1, message='Whoa! You scared me! What is wrong with you???'))` to shutdown the computer as something happens.
    This way you can display your computer, but as soon as someone tries to use the computer it shuts down.
    
    Implemented for WINDOWS.
    #### TODO:
    ---
    - Listen for devices https://stackoverflow.com/questions/469243/how-can-i-listen-for-usb-device-inserted-events-in-linux-in-python 
    """
    import pynput.mouse     # Checking the mouse with https://pythonhosted.org/pynput/mouse.html#controlling-the-mouse
    import pynput.keyboard  # Listen for Keyboard strokes https://pythonhosted.org/pynput/ https://stackoverflow.com/questions/24072790/how-to-detect-key-presses 

    import threading
    import ctypes
    def on_move(x, y):
        if verbose: print(f'Pointer moved to ({x}, {y})')
        return False
    def on_click(x, y, button, pressed):
        if verbose: print(f'{"Pressed" if pressed else "Released"} at ({x}, {y})')
        return False
    def on_scroll(x, y, dx, dy):
        if verbose: print(f'Scrolled ({x}, {y})')
        return False
    def on_press(key):
        if verbose: print(f'{key} pressed')
        return False
    def on_release(key):
        if verbose: print(f'{key} released')
        return False
    
    class StopableThread(threading.Thread): # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
        def __init__(self, function, verbose=False):
            threading.Thread.__init__(self)
            self.function = function
            self.verbose = verbose
            self.should_stop = False
        def get_id(self):
            # returns id of the respective thread
            if hasattr(self, '_thread_id'):
                return self._thread_id
            for id, thread in threading._active.items():
                if thread is self:
                    return id
        def stop_thread(self):
            self.should_stop = True
            try:
                self.listener.stop()
                self.listener.join()
            finally: pass
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')
                return
    class MouseListener(StopableThread):
        def run(self):
            try:
                self.listener = pynput.mouse.Listener( on_move=on_move, on_click=on_click, on_scroll=on_scroll )
                self.listener.start()
                self.listener.join()
                
                if self.should_stop: return

                if verbose: print('Mouse trigger')
                self.function()
            finally: pass
    class KeyboardListener(StopableThread):
        def run(self):
            try:
                self.listener = pynput.keyboard.Listener( on_press=on_press, on_release=on_release )
                self.listener.start()
                self.listener.join()

                if self.should_stop: return

                if verbose: print('Keyboard trigger')
                self.function()
            finally: pass
    
    # Start the listeners
    listeners = []
    if listen_mouse:    listeners.append(MouseListener(function,verbose))
    if listen_keyboard: listeners.append(KeyboardListener(function,verbose))
    for listerer in listeners:
        listerer.start()

    # Wait until something happens
    did_trigger = False
    if timeout_seconds < 1: timeout_seconds = 3153600000 # 100 years
    while (timeout_seconds > 0):
        time.sleep(1)
        timeout_seconds -= 1
        for listener in listeners:
            if not listener.is_alive():
                # it activated the payload
                did_trigger = True
                timeout_seconds = 0
                break
    
    # Either the timer expired or a listener triggered
    for listener in listeners:
        listener.stop_thread()
    for listener in listeners:
        listener.join()

    # Returns True if listener triggered
    return did_trigger
if __name__ == '__main__':
    print(computer_hostage(lambda:print('sample text'), timeout_seconds=3, verbose=True))
