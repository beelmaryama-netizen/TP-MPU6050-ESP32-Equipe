# TP - Lecture et journalisation du MPU6050 avec ESP32

**Cours :** Systèmes embarqués  
**Équipe :** Khalid Asseffar, Maryem Belouaar, Samy, Youness, Mohammed Nouaoury, Daouda Souare  
**Langage :** MicroPython (ESP32)  
**Objectif :** lire l'accélération et la rotation sur l'axe Z, afficher les valeurs dans Thonny et les enregistrer dans `log_mpu6050.txt` sur l'ESP32.

## Documentation technique

[Consulter le rapport PDF](documentation/Documentation_Technique_TP_MPU6050.pdf)

## Contenu du dossier

```text
TP_MPU6050_ESP32_Equipe/
├── code/
│   ├── test_i2c.py           # Vérifie l'adresse 0x68 sur 10 scans
│   ├── diagnostic_mpu6050.py # Vérifie le capteur et la mémoire flash
│   ├── mpu6050_log.py        # Programme principal de mesures + journalisation
│   └── lire_log.py           # Affiche un extrait du journal sur l'ESP32
├── documentation/
│   └── Documentation_Technique_TP_MPU6050.pdf
└── README.md
```

## Branchement (ESP32 éteint / câble USB débranché)

| MPU6050 | ESP32 | Rôle |
|---|---|---|
| VCC | 3V3 | Alimentation |
| GND | GND | Masse |
| SDA | GPIO 21 | Données I2C |
| SCL | GPIO 22 | Horloge I2C |

Ne pas utiliser le 5V pour cette configuration. Le capteur doit être correctement fixé (broches soudées et contacts stables).

## Utilisation avec Thonny

1. Brancher l'ESP32 par USB et sélectionner l'interpréteur **MicroPython (ESP32)** ainsi que le bon port série.
2. Ouvrir `code/test_i2c.py` puis appuyer sur **F5** : l'adresse **[104]** doit apparaître à chaque scan (104 = 0x68).
3. Si nécessaire, lancer `code/diagnostic_mpu6050.py` pour tester la lecture et l'écriture de fichier.
4. Ouvrir `code/mpu6050_log.py`, enregistrer le script sur **MicroPython device** puis lancer avec **F5**.
5. Faire bouger doucement le capteur pendant 20 à 30 secondes; les valeurs de Z s'affichent dans la console.
6. Arrêter par **Ctrl+C**. Aller dans **View > Files > MicroPython device** et télécharger `log_mpu6050.txt` sur le PC.
7. Facultatif : exécuter `code/lire_log.py` pour afficher les quinze premières lignes sur l'ESP32.

**Astuce :** conserver le nom `mpu6050_log.py` plutôt que `main.py` pour éviter un lancement automatique au démarrage pendant les tests.

## Exemple de ligne (illustration, pas une mesure réelle de l'équipe)

```text
Accel [Z]: 0.98 g | Rotation [Z]: 0.15 deg/s
```

## Notes techniques

- Le sujet initial emploie un bus I2C à **400 kHz**; notre version utilise **100 kHz** après les difficultés de communication observées pendant les essais.
- L'adresse I2C du module est **0x68**, affichée comme **104** en décimal.
- Le code utilise `0x3F` (accélération Z) et `0x47` (rotation Z), selon l'exercice.
- La conversion utilise **16384** LSB/g et **131.2** LSB/(°/s) selon la feuille d'exercice.
- Le programme ajoute les données avec le mode fichier **`a`** et ferme chaque fichier à l'aide de `with open`.
- Éviter de laisser tourner pendant des heures : une écriture très fréquente peut user la mémoire flash du microcontrôleur.
- Les valeurs d'exemple sont illustratives. Le véritable `log_mpu6050.txt` est créé et reste sur l'ESP32 au moment de l'exécution du programme, pas dans cette archive.

## Difficultés rencontrées au laboratoire

- Un ancien programme Wi-Fi démarrait automatiquement : le firmware MicroPython a été réinstallé sur l'ESP32 après la procédure d'effacement prévue.
- Un premier scan I2C a détecté `[104]`; des essais intermittents ont montré des valeurs `[]` et `[81, 104]`, puis les connexions ont été vérifiées.
- Une lecture initiale a renvoyé `OSError: [Errno 19] ENODEV`. Le montage a ensuite permis une lecture brute réussie; la fiabilité a été améliorée à 100 kHz.

La documentation PDF explique l'architecture, les fonctions du code, la procédure, les tests et les réponses aux trois questions de la feuille de TP.
