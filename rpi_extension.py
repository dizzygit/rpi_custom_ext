import RPi.GPIO as GPIO #z biblioteki pip install rpi-lgpio, standardowy RPi.GPIO nie działa
import time
import logging
import os

#obsługa i2c:
from luma.core.interface.serial import i2c

#wyświetlacz OLED 1.30': 
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

#biblioteka do sprawdzenia IP
import socket

# Konfiguracja loggera
logging.basicConfig(
    filename='/home/dizzy/rpi_custom_ext/test.log',  # Ścieżka do pliku logów
    level=logging.INFO,               # Poziom logów
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format logów
    datefmt='%Y-%m-%d %H:%M:%S'       # Format daty i czasu
)

# Konfiguracja GPIO
GPIO.setmode(GPIO.BCM)  # Używamy numeracji BCM (Broadcom)

# Ustawienia dla wyświetlacza OLED
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# Funkcja do odczytu temperatury
def get_temperature():
    temp_output = os.popen("vcgencmd measure_temp").readline()
    return temp_output.replace("temp=", "").replace("'C\n", "")

# Funkcja do pobierania adresu IP
def get_ip_address():
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    ipaddr = s.getsockname()[0]
    host = socket.gethostname()
    #print ("IP:", ipaddr, " Host:", host)
    return ipaddr, host

# Zmienna z ścieżką do czcionki TTF
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Ścieżka do czcionki
font_size = 12  # Rozmiar czcionki

# Funkcja do wyświetlania tekstu na OLED
def display_text(temp, ip, hostname):
    with canvas(device) as draw:
        font = ImageFont.truetype(font_path, font_size)  # Użycie czcionki TTF
        draw.text((5,5), f"Temp: {temp}C", font=font, fill=255)
        draw.text((5,20), f"IP: {ip}", font=font, fill=255)  # Wyświetlanie adresu IP w drugiej linii
        draw.text((5,35), f"Hostname: {hostname}", font=font, fill=255)  # Wyświetlanie adresu IP w drugiej linii

# Konfiguracja pinu jako wejście pod przycisk
input_przycisk = 17
GPIO.setup(input_przycisk, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull up czyli przycisk zwieramy do masy

# Funkcja obsługi przerwania na GPIO
def button_callback(channel):
    logging.info("Wciśnięto przycisk")

# Ustawienie przerwania na wykrycie opadającego zbocza (wciśnięcie przycisku)
GPIO.add_event_detect(input_przycisk, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    # Skrypt działa w pętli nieskończonej, dopóki nie zostanie przerwany
    while True:
        temp = get_temperature()        # Odczyt temperatury
        ip_address, host_name = get_ip_address()   # Odczyt adresu IP        
        display_text(temp, ip_address, host_name) # Wyświetlanie temperatury i adresu IP na OLED
        time.sleep(1)
except KeyboardInterrupt:
    print("Koniec programu")
finally:
    GPIO.cleanup()
