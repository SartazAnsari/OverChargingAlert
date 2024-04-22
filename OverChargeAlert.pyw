import os
import subprocess
import sys

# Path to the script directory
script_dir = "D:\\Projects\\Python\\over-charge-alert"

def run_script_in_virtualenv():
    # Path to the Python interpreter in the virtual environment
    python_bin = os.path.join(script_dir, "over-charge-alert-env", "Scripts", "pythonw.exe")
    
    # Path to your Python script
    script_file = os.path.join(script_dir, "OverChargeAlert.pyw")
    
    # Run the script using the Python interpreter in the virtual environment
    subprocess.Popen([python_bin, script_file])

def is_already_running():
    for proc in psutil.process_iter(['pid', 'name']):
        # check whether the process name matches
        if proc.info['name'] == 'OverChargeAlert.py':
            return True
    return False

# Check if we're running inside a virtual environment
if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
    import psutil
    import time
    from infi.systray import SysTrayIcon
    from win10toast import ToastNotifier
    import signal

    # Check if another instance is already running
    if is_already_running():
        sys.exit()  # Exit if another instance is running

    def check_battery(systray):
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged  # True if the laptop is plugged in
        alert = 90

        toaster = ToastNotifier()

        if plugged:
            if percent == 100:
                toaster.show_toast("Over Charge Alert", "Battery is fully \U0001F50B charged.\nPlease unplug \U0001F50C your charger.", duration=10)
            elif percent > alert:
                toaster.show_toast("Over Charge Alert", "Battery charged over " + str(alert) + "% \u26A1.\nPlease unplug \U0001F50C your charger.", duration=10)
            elif percent == alert:
                toaster.show_toast("Over Charge Alert", "Battery charged to " + str(alert) + "% \u26A1.\nPlease unplug \U0001F50C your charger.", duration=10)
            

    def exit_action(systray):
        os.kill(os.getpid(), signal.CTRL_C_EVENT)

    menu_options = (("Check charge", None, check_battery),)
    systray = SysTrayIcon("icon.ico", "Battery Monitor", menu_options, on_quit=exit_action)
    systray.start()

    while True:
        check_battery(systray)
        time.sleep(60)  # check every minute

else:
    run_script_in_virtualenv()
