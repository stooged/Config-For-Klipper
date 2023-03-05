#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

RELAY_GPIO = 17
DHT_GPIO = 4
is_20x4lcd = True
temp_on = 24
temp_off = 20
displayname = str("Printer")

lcd_display = None
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(RELAY_GPIO, GPIO.OUT) 

try:
    if is_20x4lcd:
        lcd_display = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4, backlight_enabled=True, charmap='A00')
        if lcd_display is not None:           
            lcd_display.clear()
            displayname = displayname[0:20]
            lcd_display.cursor_pos = (1, int((20 - len(displayname)) / 2))
            lcd_display.write_string(displayname)
            lcd_display.cursor_pos = (2, 5)
            lcd_display.write_string("Loading...")
    else:
        lcd_display = CharLCD(i2c_expander='PCF8574', address=0x27, cols=16, rows=2, backlight_enabled=True, charmap='A00')
        if lcd_display is not None:           
            lcd_display.clear()
            displayname = displayname[0:16]
            lcd_display.cursor_pos = (0, int((16 - len(displayname)) / 2))
            lcd_display.write_string(displayname)
            lcd_display.cursor_pos = (1,0)
            lcd_display.write_string("   Loading...   ")
except Exception as e:
    lcd_display = None




while True:


    try:    

        if lcd_display is not None:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)

            if temperature != None and int(temperature) >= int(temp_on):
                GPIO.output(RELAY_GPIO, GPIO.HIGH)
            elif temperature != None and int(temperature) <= int(temp_off):   
                GPIO.output(RELAY_GPIO, GPIO.LOW)

            if temperature != None and humidity != None and is_20x4lcd:

                enctemp = str(int(temperature)) + "C"
                enchum = str(int(humidity)) + "%"
                lcd_display.cursor_pos = (0, 0)
                lcd_display.write_string(chr(32) * 20)
                lcd_display.cursor_pos = (1, 0)
                lcd_display.write_string("Enclosure Temp:")
                lcd_display.cursor_pos = (1, 15)
                lcd_display.write_string(chr(32) * (5 - len(enctemp)))
                lcd_display.cursor_pos = (1, 20 - len(enctemp))
                lcd_display.write_string(enctemp)
                lcd_display.cursor_pos = (2, 0)
                lcd_display.write_string("Enclosure Humi:")
                lcd_display.cursor_pos = (2, 15)
                lcd_display.write_string(chr(32) * (5 - len(enchum)))
                lcd_display.cursor_pos = (2, 20 - len(enchum))
                lcd_display.write_string(enchum)
                lcd_display.cursor_pos = (3, 0)
                lcd_display.write_string(chr(32) * 20)

            elif temperature != None and humidity != None:
                lcd_display.cursor_pos = (0, 0)
                lcd_display.write_string("Temp: %d C   " % temperature)
                lcd_display.cursor_pos = (1, 0)
                lcd_display.write_string("Humidity: %d %% " % humidity)
            
    except RuntimeError as e:
        continue
    except Exception as e:
        continue

    time.sleep(1)




