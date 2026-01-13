# https://grok.com/share/c2hhcmQtMw%3D%3D_7bf09bff-2e82-48c9-b293-ac726ecba873
# https://x.com/i/grok?conversation=1950486827665625178
#
# Grok: You're very welcome! Glad I could help with your Python code. If you have any 
#       questions or need further assistance as you work through the modifications, 
#       feel free to reach out. Good luck with your inverter control project!
#


# ControlInverter
#
# Steuerung der Anlage, Ziel: Nulleinspeisung
#
# protokolliere folgende Werte:
#    - Strom der PV-Anlage
#     - aktueller Verbrauch
#     - Vorschlag zur Reduktion/Steigerung des Wechelrichters
#
# setze neuen Wert fuer Inverter (max.)

import urllib.request
from datetime import datetime
import json
import os
import requests
import logging
import socket

URL_INVERTER = "http://192.168.0.15"
URL_INVERTER_POST = URL_INVERTER + "/api/ctrl" 
URL_INVERTER_VALUES= URL_INVERTER + "/api/record/live"
URL_INVERTER_LIMIT= URL_INVERTER + "/api/record/config"
URL_ZAEHLER="http://192.168.0.16/cm?cmnd=status%2010"
INVERTER_MAX_VALUE = 600
INVERTER_MIN_VALUE = 50
INVERTER_MIN_MODIFICATION = 10
INVERTER_MIN_PLUS = 20
INVERTER_ID = "114184201268"

HOME_PATH="/home/august/"
if ( socket.gethostname() == 'MINIPC' ) :
    LOGGING_PATH = HOME_PATH+'Configs/Blog/Linux fuer WI/SmartMeter/' # Test
else :
    LOGGING_PATH = HOME_PATH+'Solar/'                               # auf RasPi
LOGGING_FNAME = "log_pv-"


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGGING_PATH, f"error_pv-{datetime.now().strftime('%Y-%m-%d')}.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def query_zaehler():
    """Query meter for current power consumption (W). Positive = consuming, negative = feeding."""
    try:
        with urllib.request.urlopen(URL_ZAEHLER, timeout=10) as url_zaehler:
            data = json.loads(url_zaehler.read().decode('utf-8'))
            return float(data['StatusSNS']['SML']['Watt_Summe'])
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error querying meter: {e}")
        return None

def query_inverter():
    """Query inverter for current power output (W)."""
    try:
        with urllib.request.urlopen(URL_INVERTER_VALUES, timeout=10) as url_solar:
            data = json.loads(url_solar.read().decode('utf-8'))
            return float(data['inverter'][0][14]['val'])
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error querying inverter: {e}")
        return None


def query_old_value():
    """Query current inverter limit (W, scaled from percentage)."""
    try:
        with urllib.request.urlopen(URL_INVERTER_LIMIT, timeout=10) as url_old_value:
            data = json.loads(url_old_value.read().decode('utf-8'))
            return float(data['inverter'][0][0]['val']) * INVERTER_MAX_VALUE / 100.0
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error querying inverter limit: {e}")
        return None

def calculate_new_value(value_zaehler, value_inverter):
    """Calculate new inverter limit (W) to minimize grid feed-in or draw.
    Formula: new_limit = current_inverter_power + consumption + buffer.
    Assumes value_zaehler > 0 means consuming from grid, < 0 means feeding to grid."""
    if value_zaehler is None or value_inverter is None:
        return None
    return value_inverter + value_zaehler + INVERTER_MIN_PLUS

def log_values(value_inverter, value_zaehler, new_value_inverter):
    """Log values to a daily CSV file in LOGGING_PATH."""
    try:
        now = datetime.now()
        date_today = now.strftime("%Y-%m-%d")
        time_now = now.strftime("%H:%M:%S")
        log_file = os.path.join(LOGGING_PATH, f"{LOGGING_FNAME}{date_today}.csv")

        # Ensure directory exists
        # os.makedirs(LOGGING_PATH, exist_ok=True)

        # Use None for invalid values
        values = [str(v) if v is not None else "N/A" for v in [value_inverter, value_zaehler, new_value_inverter]]
        with open(log_file, 'a', encoding='utf-8') as log_datei:
            log_datei.write(f"{date_today}, {time_now}, {values[0]}, {values[1]}, {values[2]}\n")
        logger.info(f"Logged values: inverter={values[0]}, meter={values[1]}, new_limit={values[2]}")
    except OSError as e:
        logger.error(f"Error writing to log file: {e}")

def set_new_value_inverter( old_value, new_value) :
# siehe: https://github.com/lumapu/ahoy/blob/main/manual/User_Manual.md
    """Adjust and send new inverter limit, respecting min/max bounds and minimum change threshold."""
    if new_value is None or old_value is None:
        logger.warning("Cannot set new inverter value due to invalid inputs")
        return None
    # Clamp new value to min/max bounds
    temp_value = max(INVERTER_MIN_VALUE, min(new_value, INVERTER_MAX_VALUE))
    # Skip small changes
    if abs(old_value - temp_value) <= INVERTER_MIN_MODIFICATION:
        # logger.info(f"No inverter update: change ({abs(old_value - temp_value):.1f}W) below threshold")
        return temp_value

    send_to_inverter = {
        "id":  INVERTER_ID,
        "cmd": "limit_nonpersistent_absolute",
        "val":  f'{temp_value:.1f}'    # neuer Wert <VALUE>
    }
    # send request to inverter
    try:
        # logger.info(f"Sending to inverter: {send_to_inverter}")
        response = requests.post(URL_INVERTER_POST, json=send_to_inverter, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        # logger.info(f"Inverter response: {response.text}")
        return temp_value 
    except requests.RequestException as e:
        logger.error(f"Error sending to inverter: {e}")
        return None

        return temp_value

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
