# OverChargeAlert

## Description
OverChargeAlert is a Python script for monitoring battery charge levels and displaying notifications when the battery is fully charged or over a specified threshold. Its purpose is to prevent overcharging of laptop batteries, helping users protect their battery health and prolong its lifespan. The script runs in the background and provides real-time updates on battery status.

## Features
- Monitors battery charge levels in real-time
- Displays toast notifications for battery alerts, including:
  - Notifications when the battery is fully charged.
  - Alerts when the battery charge exceeds a specified threshold (default: 90%).
  - Notifications for plug/unplug events, including battery usage and charging time.
- Runs in the background and checks battery status periodically
- Provides a system tray icon for easy access to battery status and manual checks.

## Prerequisites
*1.* **Python 3.x:** Download and install from [python.org](https://www.python.org/).

## Setup
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/SartazAnsari/over-charge-alert.git
   cd over-charge-alert
   ```

2. Create and activate a virtual environment (recommended to ensure a clean and isolated environment):
   - **For Windows:**
     ```bash
     python -m venv over-charge-alert-env
     .\over-charge-alert-env\Scripts\activate
     ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Usage
- Run `OverChargeAlert.py` to start monitoring battery status. This will display the console window while running.
- Alternatively, run `OverChargeAlert.pyw` to start monitoring battery status without displaying the console window.
- Ensure that the script is running in a virtual environment to avoid conflicts with system packages.

## Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
