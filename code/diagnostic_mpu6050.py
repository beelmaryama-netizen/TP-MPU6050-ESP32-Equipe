"""Diagnostic du MPU6050 : scan, identite, lecture brute et fichier test."""
from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

print("TEST 1 : demarrage")
print("TEST 2 : scan I2C :", i2c.scan())

try:
    # 0x75 : registre WHO_AM_I du MPU6050.
    identite = i2c.readfrom_mem(0x68, 0x75, 1)[0]
    print("TEST 3 : identite :", hex(identite))

    i2c.writeto_mem(0x68, 0x6B, b"\x00")
    time.sleep_ms(100)

    # 0x3F : debut des deux octets d'acceleration Z.
    brut = i2c.readfrom_mem(0x68, 0x3F, 2)
    print("TEST 4 : acceleration brute :", brut)

    with open("test_log.txt", "w") as fichier:
        fichier.write("Test ecriture OK\n")
    print("TEST 5 : fichier test_log.txt cree")
    print("TOUS LES TESTS SONT TERMINES")

except OSError as erreur:
    print("ERREUR I2C OU FICHIER :", erreur)
    print("Verifier les quatre connexions, puis relancer le diagnostic.")
