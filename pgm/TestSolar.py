import urllib.request
import json
from datetime import datetime
# from cups import IPP_OP_ACTIVATE_PRINTER

now = datetime.now()
jetzt = now.strftime("-%Y-%m-%d-%H%M%S")
# WORKING_DIR="
# WORKING_DIR="/home/august/Configs/Blog/Linux fuer WI/SmartMeter"
# if now.hour <= 5 :
#    exit(0)

#if now.hour >= 22 :
#    exit(0)

with urllib.request.urlopen("http://192.168.0.15/api/record/live") as url:
    solar = url.read()
#     print(solar)

#    datei = open("/home/august/Solar/panel"+jetzt+".json", "w+t")
    datei = open("panel"+jetzt+".json", "w+t")
#    solar_json = json.dumps(solar)
    datei.write( solar.decode('utf-8'))
    datei.close()

with urllib.request.urlopen("http://192.168.0.16/cm?cmnd=status%2010") as url_zaehler:
    zaehler = url_zaehler.read()
    datei = open("zaehler"+jetzt+".json", "w+t")
    datei.write( zaehler.decode('utf-8'))
    datei.close()

# Zuordnung
# AC Power: 130.6 -> 14 P_AC
# Yield Day: 357 -> 20 YieldDay
# Yield Total: 142.85 -> 21 YieldTotal
# DC Power: 136.8 -> 22 P_DC
# Voltage: 227 -> 12 U_AC
# Current: 0.58 -> 13 I_AC
# Frequency: 49.98 -> 16 F_AC
# Efficiency: 95.47 -> 23 Effiency

# Channel 1:
# Power: 67.6 -> 2 P_DC
# Irradiation: 11.27 -> 5 Irradiation
# Yield Day: 174 -> 3 YieldDay
# Yield Total: 67,73 -> 4 YieldTotal
# Voltage: 32.1 -> 0 U_DC
# Current: 2.1 -> 1 I_DC

# Channel 2:
# Power: 69.2 -> 8 P_DC
# Irradiation: 11.53 -> 11 Irradiation
# Yield Day: 183 -> 9 YieldDay
# Yield Total: 75.12 -> 10 YieldTotal
# Voltage: 32.3 -> 6 U_DC
# Current: 2.14 -> 7 I_DC


# Struktur Zaehler:
# b'{
# "StatusSNS":{"Time":"2025-06-22T15:06:03",
# "SML":{"Verbrauch_Summe":4336.6199658,
#        "Einspeisung_Summe":308.7189004,
#        "Watt_L1":-464.21,
#        "Watt_L2":52.52,
#        "Watt_L3":5.88,
#        "Watt_Summe":-406.21,
#        "Volt_L1":231.5,
#        "Volt_L2":232.6,
#        "Volt_L3":232.4
#        }}}'
