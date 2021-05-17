from time import sleep
from configparser import ConfigParser

from vars import VAC_CENTERS
from Client.Client import BrowserClient


config = ConfigParser()
config.read("config.ini")

center = config["Appointment"]["center"]
if center in VAC_CENTERS.keys():
    center = VAC_CENTERS[center]
else:
    print("Unknown center, please check your config. || Unbekanntes Impfcenter, bitte Konfiguration überprüfen.")
    input()
    exit()

search_date = config["Appointment"]["date"]

pref_day = config["Appointment"]["pref_day"]
if pref_day == "Wochentag":
    pref_day = "3"
elif pref_day == "Wochenende":
    pref_day = "4"
elif pref_day == "None":
    pref_day = "2"
else:
    print("Wrong configuration at pref_day, please check your config. || False Einstellung bei pref_day, bitte Konfiguration überprüfen.")
    input()
    exit()
    
day_time = config["Appointment"]["day_time"]
if day_time == "Nachmittags":
    day_time = "2"
elif day_time == "Vormittags":
    day_time = "3"
elif day_time == "None":
    day_time = "4"
else:
    print("Wrong configuration at day_time, please check your config. || False Einstellung bei day_time, bitte Konfiguration überprüfen.")
    input()
    exit()

client = BrowserClient(config["General"]["browser"], config["General"]["url"])

client.start_browser()
while True:
    if not client.is_logged_in():
        client.login(config["Login"]["username"], config["Login"]["password"])
    elif client.is_at_choose_action():
        client.choose_action()
    elif client.is_at_find_appointment():
        client.find_appointment(center, search_date, pref_day, day_time)
    elif client.is_at_appointment_result():
        if client.is_no_appointment():
            client.go_back()
        else:
            client.maximize()
            print("Possibly found an appointmet, please check browser. Hit Enter to continue searching, or CTRL+C to end || Es wurde eventuell ein Termin gefunden. Bitte den Browser überprüfen. Enter drücken um mit der Suche fortzufahren, STRG+C um die Suche zu beenden.")
            input()

    sleep(int(config["General"]["sleep_time"]))