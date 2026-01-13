# Nulleinspeisung
Balkonkraftwerk: so steuern, daß (fast) kein überschüssiger Strom anfällt

Umgebung: Balkonkraftwerk mit AhoyDTU
          erzeugter Strom wird entweder im Haus verbraucht, überschüssiger Strom geht als "Spende" an den Stromlieferanten
Ziel: Reduktion der "Spende" an den Stromlieferanten

beschrieben habe ich dies hier: Link zum Blog: [https://xxxxx](https://linux-fuer-wi.blogspot.com/2026/01/keine-spende-stromlieferanten.html)

hier liefere ich die Dateien zu meinem Text.

Aufbau der Verzeichnisse und Beschreibung der Dateien

data
Format: LibreOffice
daten-07.ods
    Daten der AhoyDTU + Stromzähler vom Juli 2025, ohne Eingriff in den Wechselrichter
daten-08.ods
    Daten von AhoyDTU + Stromzähler vom August 2025, mit Eingriff in den Wechselrichter
    
Rohdaten:
Format: json und Text
panel-2025-07.zip
zaehler-2025-07.zip
    panel: die Daten des Wechselrichters
    zaehler: die Daten des Stromzählers
    Daten für den Juli 2025, unverändert
    pro Minute einen Datensatz
error202508.zip
    die Daten für Wechselrichter, Stromzähler und den neuen Wert für Wechselrichter (verkürzte Darstellung)
    Log- und Fehlermeldungen
    im Juli wurde dies noch nicht in dieser Form protokolliert
panel-2025.08.zip
zaehler-2025-08.zip
    die Daten des Wechselrichters und des Zählers, jeweils um 22 Uhr des jeweiligen Tages
    
pgm
Python-Programme, laufen auf RasPi als cron-job
TestSolar.py
    erster Versuch, Daten von AhoyDTU und Stromzähler abgreifen und in Datei schreiben
    läuft aktuell jeden Tag um 22 Uhr, zur Kontrolle und möglicher späterer  Auswertung
LogElectricity.py
    erster Versuch der Steuerung, schreibt Vorschlag des neuen Wertes in Datei, keine Änderung an Wechselrichter/AhoyDTU
ControlInverter.py
    die Steuerung des Balkonkraftwerks
    Eintrag in cron-Tabelle:  # * 09-20 * * *        python3 /home/august/Solar/ControlInverter.py
    (aktuell auskommtiert)
    
grok
- beginnend mit Programm TestSolar.py
- verbessere dieses Programm
- frage Grok: 
    - eigentlich nicht am Veröffentlichung der gaqnzen Aktion gedacht
    - Antwort leider nicht gesichert
    - Vorschlag übernommen
- eigene Verbesserung/Änderung in das neue Programm eingebaut
- erneut Grok befragt:
    - Antwort siehe Datei grok.txt
    - oder hier: https://grok.com/share/c2hhcmQtMw%3D%3D_7bf09bff-2e82-48c9-b293-ac726ecba873
      (Anmeldung erforderlich)
    - Änderung übernommen
- kleinere Anpassungen vorgenommen
- Programm läuft in dieser Form

Programm ist somit entstanden mit Hilfe von Grok.

DISCLAIMER
frei zur allgemeinen Benutzung
eigene Risiko, übernhme keine Verantwortung bei einem eventuellen Einsatz
YOUR RISK!
