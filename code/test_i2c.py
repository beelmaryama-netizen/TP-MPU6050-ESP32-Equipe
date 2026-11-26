"""Test de stabilite I2C (10 scans) pour l'ESP32 et le MPU6050."""
from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

for numero in range(1, 11):
    adresses = i2c.scan()
    etat = "OK" if 0x68 in adresses else "A VERIFIER"
    print("Test {} : {} - {}".format(numero, adresses, etat))
    time.sleep(1)
