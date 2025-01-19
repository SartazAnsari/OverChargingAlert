import os
import subprocess
import sys
from datetime import datetime

# Path to script directory
script_dir = 'D:\\Projects\\Python\\over-charge-alert'

def run_script_in_virtualenv():
    # Path to virtual environment's Python interpreter
    python_bin = os.path.join(script_dir, 'over-charge-alert-env', 'Scripts', 'python.exe')
    
    # Path to Python script
    script_file = os.path.join(script_dir, 'OverChargeAlert.py')
    
    # Run the script using virtual environment's Python interpreter
    subprocess.Popen([python_bin, script_file])

def is_already_running():
    for proc in psutil.process_iter(['pid', 'name']):
        # check whether the process name matches
        if proc.info['name'] == 'OverChargeAlert.py':
            return True
    return False

# Check if we're running inside virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    import psutil
    import time
    from infi.systray import SysTrayIcon
    from plyer import notification
    import signal

    # Tracking variables
    last_state = None
    last_percentage = None
    last_time = None
    last_alert_time = 0

    def format_time_difference(start_time):
        if start_time is None:
            return "Unknown"
        diff = time.time() - start_time
        hours = int(diff // 3600)
        minutes = int((diff % 3600) // 60)
        return f"{hours}h {minutes}m"

    def show_notification(title, message, timeout=10):
        notification.notify(
            title=title,
            message=message,
            app_icon='icon.ico',
            timeout=timeout
        )

    def check_battery_status(systray):
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged

        status = "Charging" if plugged else "Not charging"
        message = f"Battery Level: {percent}%\nStatus: {status}"
        show_notification('Battery Status', message, timeout=5)
        return 0

    def monitor_battery():
        global last_state, last_percentage, last_time, last_alert_time
        
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged
        alert = 90
        current_time = time.time()

        # Initialize on first run
        if last_state is None:
            last_state = plugged
            last_percentage = percent
            last_time = current_time
            return

        # Check for plug/unplug events
        if plugged != last_state:
            time_str = format_time_difference(last_time)
            percent_change = abs(percent - last_percentage)

            if plugged:
                # Calculate battery usage time
                message = (
                    f"Ran on battery for: {time_str}\n"
                    f"Battery used: {percent_change}%\n"
                    f"({last_percentage}% → {percent}%)"
                )
                show_notification('Power Connected', message)
            else:
                # Calculate charging time
                message = (
                    f"Charged for: {time_str}\n"
                    f"Battery charged: {percent_change}%\n"
                    f"({last_percentage}% → {percent}%)"
                )
                show_notification('Power Disconnected', message)
            
            # Update tracking variables
            last_state = plugged
            last_percentage = percent
            last_time = current_time
            last_alert_time = current_time

        # Original overcharge monitoring - only check if 60 seconds passed since last alert
        if plugged and (current_time - last_alert_time) >= 60:
            if percent == 100:
                show_notification(
                    'Over Charge Alert',
                    'Battery is fully \U0001F50B charged.\nPlease unplug \U0001F50C your charger.'
                )
                last_alert_time = current_time
            elif percent > alert:
                show_notification(
                    'Over Charge Alert',
                    f'Battery charged over {alert}% \u26A1.\nPlease unplug \U0001F50C your charger.'
                )
                last_alert_time = current_time
            elif percent == alert:
                show_notification(
                    'Over Charge Alert',
                    f'Battery charged to {alert}% \u26A1.\nPlease unplug \U0001F50C your charger.'
                )
                last_alert_time = current_time

    def exit_action(systray):
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
        return 0

    menu_options = (
        ('Check Battery', None, check_battery_status),
    )
    systray = SysTrayIcon('icon.ico', 'Battery Monitor', menu_options, on_quit=exit_action)
    systray.start()

    # Start monitoring
    while True:
        monitor_battery()
        time.sleep(3)

else:
    run_script_in_virtualenv()