# ESP8266 MicroPython Project Setup Guide

This guide explains how to set up your ESP8266 board and your PC for MicroPython development, including installing all dependencies and uploading files.

## HARDWARE
- ESP8266 development board for ch340 driver
- USBmicro cable
- Windows PC (PowerShell recommended)
- Python 3.x installed on your PC

## ESP instalation 
## 1. Install Python and Required Tools on PC
1. Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Open PowerShell and install the required Python packages:
   ```
   pip install esptool mpremote
   ```

## 2. Install USB Drivers (if needed)
- For most ESP8266 boards, Windows will auto-install drivers.
- If not, install the [CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) or [CH340](https://sparks.gogo.co.nz/ch340.html) driver, depending on your board.

## 3. Flash MicroPython Firmware to ESP8266
1. Download the latest MicroPython firmware for ESP8266 from [micropython.org/download/esp8266](https://micropython.org/download/esp8266/).
2. Put your ESP8266 into bootloader mode:
   - Hold the FLASH button, press and release the RST button, then release FLASH.
3. Erase the chip:
   ```
   python -m esptool --port COMx erase_flash
   ```
   (Replace `COMx` with your actual COM port)
4. Flash the firmware:
   ```
   python -m esptool --port COMx --baud 460800 write_flash --flash_size=detect 0x00000 esp8266-xxxxxx.bin
   ```
   (Replace `esp8266-xxxxxx.bin` with your firmware filename)

## 4. Upload Python Files and Libraries to ESP8266
1. Download MicroPython-compatible libraries, make sure they don't import smbus and they are micropython libs:
   - [lcd_api.py](https://github.com/dhylands/python_lcd/blob/master/lcd/lcd_api.py)
   - [i2c_lcd.py](https://github.com/dhylands/python_lcd/blob/master/lcd/i2c_lcd.py)
2. Change the wifi credentials in ```main.py``` to yours, then save file
   ```
   ssid = 'XX' #replace with your WiFi SSID
   password = 'XX' #replace with your WiFi password
   ```
3. Upload files using mpremote:
   ```
   python -m mpremote connect COMx cp main.py :main.py
   python -m mpremote connect COMx cp lcd_api.py :lcd_api.py
   python -m mpremote connect COMx cp i2c_lcd.py :i2c_lcd.py
   ```

## 5. Connect to MicroPython REPL
- To interact with your ESP8266:
  ```
  python -m mpremote connect COMx
  ```
- Use Ctrl+D to soft reset, Ctrl+] to exit REPL.
- Use Putty with 115200 baud 

## 6. Serwer connection
Added functionality of sending ip at start and waiting for one message from server ```server.py```

## 7. Troubleshooting
- If you see `ImportError: no module named 'smbus'`, you are using a non-MicroPython library. Use the correct files linked above.
- Make sure only one program is using the COM port at a time.
- If upload fails, reset the board and try again.

## 8. Usage 
To use device click rst button. On every reset device will send a message to given ip, then wait for message sent to it. The message sent by device will contain its ip. The message receive will be verified whether it's 'ALERT', if true the buzzer beep will go on for few secs then the device will come back to waiting for message.
