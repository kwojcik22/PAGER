from machine import Pin
import time as time
# sending bit to the server
import socket
import machine
import ubinascii
import network

from machine import I2C, Pin
from i2c_lcd import I2cLcd

def send_ip_to_server(server_ip, server_port, device_ip):
    addr = socket.getaddrinfo(server_ip, server_port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(device_ip.encode())
    s.close()

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print('Connecting to WiFi...')
    while not wlan.isconnected():
        pass 
        print('.')
    print('Connected to WiFi:', wlan.ifconfig())
    return wlan

def device_msg():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd_addr = 0x27  # Common address, yours may differ
    lcd = I2cLcd(i2c, lcd_addr, 2, 16)
    lcd.move_to(0, 0)
    lcd.putstr("INCOMING:")
    lcd.move_to(3, 1)
    lcd.putstr("P I W O")

        #PWM piezo buzzer on pin 15
    buzzer = machine.PWM(machine.Pin(15), freq=10, duty=512)
    # for loop 4 times
    for _ in range(4):
        buzzer.duty(0)  # Set duty cycle to 0 (off)
        time.sleep(0.5)   # Play sound for 0.5 second
        buzzer.duty(512)  # Change duty cycle to 512 (on)
        time.sleep(0.5)   # Play sound for 0.5 second
    buzzer.deinit()  # Turn off the buzzer

def server_command():
    # Set up a socket to listen for incoming commands
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 22))  # Listen on port 22
    while True:
        print("Waiting for server command...")
        data, addr = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        command = data.decode()
        print("Received command:", command)
        if command == 'ALERT\n':
            device_msg()

def turn_off_LCD():
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd_addr = 0x27  # Common address, yours may differ
    lcd = I2cLcd(i2c, lcd_addr, 2, 16)
    lcd.clear()


# Indicate that the pager is running by turning on an LED connected to pin 2
led = Pin(2, Pin.OUT)
led.value(0)  # Turn the LED on
print("PAGER RUNNING")
time.sleep_ms(1000)  # Keep the LED on for 1 second
led.value(1)  # Turn the LED off

ssid = 'T-Mobile_Swiatlowod_0574'
password = '52290969530931889255'
server_ip = '192.168.1.116'
server_port = 22
wlan = connect_wifi(ssid, password)

send_ip_to_server(server_ip, server_port, wlan.ifconfig()[0])
server_command()
wlan.disconnect()
