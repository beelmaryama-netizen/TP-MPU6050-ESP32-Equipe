"""TP MPU6050 - lecture et journalisation sur ESP32 (MicroPython).

Equipe : Khalid Asseffar, Maryem Belouaar, Samy, Youness, Mohammed Nouaoury, Daouda Souare.
Branchement : VCC -> 3V3, GND -> GND, SDA -> GPIO21, SCL -> GPIO22.
Lancer depuis Thonny avec F5, puis Ctrl+C pour terminer.
"""

from machine import I2C, Pin
import time

MPU6050_ADDR = 0x68
FICHIER_LOG = "log_mpu6050.txt"

# L'exercice original utilise 400 kHz. Nous avons teste 100 kHz
# pour rendre la communication plus stable sur notre montage.
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)


def capteur_present():
    """Reessayer le scan si la connexion I2C est temporairement instable."""
    for _ in range(5):
        adresses = i2c.scan()
        print("Scan I2C :", adresses)
        if MPU6050_ADDR in adresses:
            return True
        time.sleep_ms(200)
    return False


def lire_brut(registre):
    """Lire un entier signe sur 16 bits a partir de deux octets."""
    donnees = i2c.readfrom_mem(MPU6050_ADDR, registre, 2)
    valeur = (donnees[0] << 8) | donnees[1]
    if valeur >= 32768:
        valeur -= 65536
    return valeur


def demarrer():
    if not capteur_present():
        print("ERREUR : MPU6050 introuvable. Verifier le cablage.")
        return

    # Registre 0x6B : gestion de l'alimentation (reveil du capteur).
    i2c.writeto_mem(MPU6050_ADDR, 0x6B, b"\x00")
    time.sleep_ms(100)

    print("Demarrage de la lecture et du log...")
    with open(FICHIER_LOG, "a") as fichier:
        fichier.write("--- Debut du Journal MPU6050 ---\n")

    try:
        while True:
            try:
                # Axe Z : accelerometre (0x3F) et gyroscope (0x47).
                accel_z = lire_brut(0x3F) / 16384.0
                gyro_z = lire_brut(0x47) / 131.2

                ligne = "Accel [Z]: {:.2f} g | Rotation [Z]: {:.2f} deg/s\n".format(
                    accel_z, gyro_z
                )
                print(ligne, end="")

                # Mode 'a' : conserve les anciennes mesures.
                with open(FICHIER_LOG, "a") as fichier:
                    fichier.write(ligne)

            except OSError as erreur:
                print("Erreur de communication ou de fichier :", erreur)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nAcquisition arretee. Fichier :", FICHIER_LOG)


demarrer()
