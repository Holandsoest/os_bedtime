# os_bedtime

os_bedtime is a python module **made for windows (for now)** to turn off the computer with simple functions.  
Currently support for Linux is unplanned but kept in mind, but for me there is no way to test OSX :'(  
So that will come much later.  

## Early access

Currently this module is yet in the major version **0.x.x** and with that in mind the interface might change at any time.  
It is kept in mind to make changes as little as possible, but it is not out of question that things might brake during early access.  

If you feel like contributing. (OSX or Linux or improvements for Windows even) Let me know in an issue.  

## How to install

`pip install os-bedtime`  

## **Issue:** Sleep issues

Your computer might be waking from sleep mode because certain peripheral devices, such as a mouse, a keyboard, or headphones are plugged into a USB port or connected via Bluetooth. It might also be caused by an app or a wake timer.

### **Windows:** Turn off wake-timers

> Wake timers are timers that may wake your computer on a set time. Disabling this make this impossible until you re-enable it.  
> *If you use wake-timers to automatically wake your computer at 7 am or something, this will not work anymore.*
> 
> 1. Right-click Windows button. Select `Energy-management`  
> 2. Scroll down and click the link for `Extra energy-settings`  
> 3. Click the `Change power-plan` to the right of the currently selected power-plan  
> 4. Click the `Change advanced energy-settings` link  
> 5. Scroll and find `Sleep` -> `Allow activation timers`  
> 6. Set it to `No` or `Disabled`  

### **Windows:** Turn off peripheral-devices access to wake your pc

> Peripheral-devices (like for example your keyboard) have access to wake your computer out of sleep-mode.
> For something like a keyboard this makes sense. You press the space-bar and the computer wakes up, but there are other devices where this might make less sense. For example a network device may wake your computer?
> 
> 1. left-click the windows button. Type `CMD` and choose `Run as administrator`  
> 2. It will prompt you if you did this and allow this... Allow  
> 3. Type in the console `powercfg -devicequery wake_armed` and press enter  
> 4. It gives you a list of all your peripheral devices that may wake up your computer out of sleep mode  
> 5. Right-click Windows button. Select `Device-management`  
> 6. Find all the devices (or the onces you want to disable), in the list and double-click them
> 7. Find the tab called: `Energy-management` and uncheck the checkbox for `This device may wake the computer out of sleepmode`  
***Note***: Some devices like mice and keyboards show up multiple times *(that is normal)*, but not all have this tab *(that is also normal)*. Find the onces that do and disable those  
