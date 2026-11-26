"""Afficher un extrait du journal enregistre sur l'ESP32."""

NOM_FICHIER = "log_mpu6050.txt"
NOMBRE_LIGNES = 15

try:
    print("Contenu de :", NOM_FICHIER)
    with open(NOM_FICHIER, "r") as fichier:
        for numero, ligne in enumerate(fichier):
            if numero >= NOMBRE_LIGNES:
                print("... extrait limite a", NOMBRE_LIGNES, "lignes")
                break
            print(ligne, end="")
except OSError as erreur:
    print("Impossible d'ouvrir le journal :", erreur)
    print("Lancer d'abord mpu6050_log.py pour creer le fichier.")
