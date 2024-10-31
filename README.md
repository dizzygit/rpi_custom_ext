# rpi_custom_ext
dodatki do RPi4 pod NAS na OMV - wyświetlacz, przycisk na obudowę
# Raspberry Pi Temperature and IP Monitor

This project monitors the temperature of a Raspberry Pi and displays it on a 1.30'' IIC OLED display, along with the device's IP address and hostname. It also logs button presses.

## Features
- Monitors the Raspberry Pi temperature
- Displays the temperature, IP address, and hostname on an OLED display
- Logs button presses to a file
- Uses the Luma library for OLED display control

## Requirements

1. Before running the script, ensure you have the following requirements installed:
- Python 3.x
- [Luma.OLED](https://pypi.org/project/luma.oled/) for OLED display support
- [RPi.LGPIO](https://pypi.org/project/rpi-lgpio/) for GPIO pin control

2. Check if the I2C Interface is Enabled: The I2C interface might be disabled by default on your Raspberry Pi. To enable it, run:

   ```bash
   sudo raspi-config
   ```

   Go to Interface Options.
   Select I2C and set it to Enabled.

3. Install Required Packages: If you haven't already, install the necessary packages to work with I2C:

   ```bash
   sudo apt update
   sudo apt install -y i2c-tools python3-smbus
   i2cdetect -y 1
   ```
   If you see the device address (like 0x3C) on the list, the device is correctly connected.


### Setting Up a Virtual Environment

1. **Install `python3-venv` and `python3-dev` if not already installed:**
   ```bash
   sudo apt install python3-venv
   sudo apt install python3-dev
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install required packages:**
   After activating the virtual environment, run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dizzygit/rpi_custom_ext.git
   cd rpi_custom_ext
   ```

2. **Run the script:**
   ```bash
   python rpi_extension.py
   ```

## Systemd Service

A `systemd` service file is provided in the repository. To enable it, follow these steps:

1. **Copy the service file to the systemd directory:**
   ```bash
   sudo cp rpi_extension.service /etc/systemd/system/
   ```

2. **Reload systemd to recognize the new service:**
   ```bash
   sudo systemctl daemon-reload
   ```

3. **Enable and start the service:**
   ```bash
   sudo systemctl enable rpi_extension
   sudo systemctl start rpi_extension
   ```

4. **Check the status of the service:**
   ```bash
   sudo systemctl status rpi_extension
   ```

## Logging

Logs of button presses are stored in `test.log` within the project directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
