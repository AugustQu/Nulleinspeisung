# https://grok.com/share/c2hhcmQtMw%3D%3D_7bf09bff-2e82-48c9-b293-ac726ecba873

# LogElectricity
#
# Vorstufe zur Steuerung der Anlage, Ziel: Nulleinspeisung
#
# protokolliere folgende Werte:
#    - Strom der PV-Anlage
#     - aktueller Verbrauch
#     - Vorschlag zur Reduktion/Steigerung des Wechelrichters
#
import urllib.request
from datetime import datetime
import json

URL_INVERTER_VALUES="http://192.168.0.15/api/record/live"
URL_INVERTER_LIMIT="http://192.168.0.15/api/record/config"
URL_ZAEHLER="http://192.168.0.16/cm?cmnd=status%2010"
INVERTER_MAX_VALUE = 600
INVERTER_MIN_VALUE = 50
INVERTER_MIN_MODIFICATION = 10
INVERTER_MIN_PLUS = 20

HOME_PATH="/home/august/"
LOGGING_PATH = HOME_PATH+'Configs/Blog/Linux fuer WI/SmartMeter/' # Test
# LOGGING_PATH = HOME_PATH+'Solar/'                               # auf RasPi
LOGGING_FNAME = "log_pv-"



def query_zaehler() :
    with urllib.request.urlopen(URL_ZAEHLER) as url_zaehler:
        values_zaehler = url_zaehler.read()
#        print( "zaehler")
#        print(values_zaehler)
        daten = json.loads(values_zaehler)
        this_value = float(daten['StatusSNS']['SML']['Watt_Summe'])
        return this_value
    return 0

def query_inverter() :
    with urllib.request.urlopen(URL_INVERTER_VALUES) as url_solar:
        values_solar = url_solar.read()
#        print( "inverter")
#        print( values_solar)
        daten = json.loads(values_solar)
        this_value = float(daten['inverter'][0][14]['val'])
        return this_value
    return 0

def query_old_value( ) :
    with urllib.request.urlopen(URL_INVERTER_LIMIT) as url_old_value:
        value_old_limit = url_old_value.read()
#       print( 'old limit')
#        print( value_old_limit)
        daten = json.loads(value_old_limit)
        this_value = float(daten['inverter'][0][0]['val']) * INVERTER_MAX_VALUE / 100.0
        return this_value
    return 0

def calculate_new_value( value_zaehler, value_inverter):
    # Faelle:
    # value_zaehler <= 0 ==> geht an Stromliefeeranten
    # value_zaheler > 0  ==> beziehe Strom vom Lieferanten
    # neuer Wert fuer Inverter: 
    new_value = value_inverter + value_zaehler + INVERTER_MIN_PLUS
    return new_value

def log_values( value_inverter, value_zaehler, new_value_inverter) :
    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    log_datei = open(LOGGING_PATH+LOGGING_FNAME+date_today+'.csv', 'a+t')
    log_datei.write( date_today+', '+time_now+', '+str(value_inverter)+', '+str(value_zaehler)+', '+str(new_value_inverter)+"\n")
    log_datei.close()

def set_new_value_inverter( old_value, new_value) :
    temp_value = new_value
    # Grenze nach unten:
    if ( new_value < INVERTER_MIN_VALUE ) :
        temp_value = INVERTER_MIN_VALUE
    # Grenze nach oben
    elif ( new_value > INVERTER_MAX_VALUE ) :
        temp_value = INVERTER_MAX_VALUE
    # keine kleinen Aenderungen
    elif ( abs(old_value - new_value) <= INVERTER_MIN_MODIFICATION ) :
        # keine Aenderung
        temp_value = old_value
    return int(temp_value)

# main pgm
def main():
    """Main function to query, calculate, and log PV system data."""
    value_inverter = query_inverter()
    value_zaehler = query_zaehler()
    value_old_inverter = query_old_value()
    value_new_inverter = calculate_new_value( value_zaehler, value_inverter)
    value_new_inverter = set_new_value_inverter( value_old_inverter, value_new_inverter)
    log_values( value_inverter, value_zaehler, value_new_inverter)

if __name__ == "__main__":
    main()
