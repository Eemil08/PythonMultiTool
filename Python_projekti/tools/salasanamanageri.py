import os
import json
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
import getpass

TIEDOSTO = "salasanat.json"
SUOLA = b"abcxyz"

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')

def tee_avain(salasana):
    avain = hashlib.pbkdf2_hmac('sha256', salasana.encode(), SUOLA, 100000) #käyttää SHA-256 algoritmia ja pääsalasanaa + "suolaa"
    #avaimen laskenta tehdään 100000 kertaa
    return base64.urlsafe_b64encode(avain) #avain muunnetaan base64 muotoon

def salaa(fernet, salasana):
    return fernet.encrypt(salasana.encode()).decode() #fernet.encrypt salaa tekstin bytes muotoon, .decode() muuntaa takaisin tekstiksi json:ia varten

def pura(fernet, salattu):
    return fernet.decrypt(salattu.encode()).decode() #fernet.decypt() palauttaa salatun salasanan alkuperäiseksi

def lataa_tiedosto():
    if os.path.exists(TIEDOSTO): #tarkistaa onko olemassa,
        #jos on, niin avaa ja lukee salasanat json:ina
        with open(TIEDOSTO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {} #muuten palauttaa tyhjän sanakirjan.

def tallenna_tiedosto(data):
    with open(TIEDOSTO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def kaynnista():
    tyhjenna_naytto()
    print("Salasanamanageri")
    salasana = getpass.getpass("Pääsalasana: ")
    fernet = Fernet(tee_avain(salasana)) #luo Fernet objektin salaukseen ja purkuun
    salasanat = lataa_tiedosto()

    while True:
        print("\n1. Lisää salasana")
        print("2. Hae salasana")
        print("3. Luo vahva salasana")
        print("4. Poistu")
        valinta = input("Valinta: ")

        if valinta == "1":
            #kysyy tunnisteen ja salasanan ja salaa salasanan salaa() funktiolla
            nimi = input("Tunniste (esim. sivusto): ")
            sal = getpass.getpass("Salasana: ")
            salasanat[nimi] = salaa(fernet, sal)
            tallenna_tiedosto(salasanat)
            print("Salasana tallennettu.")

        elif valinta == "2":
            nimi = input("Anna tunniste: ")
            if nimi in salasanat:
                try: #jos löytyy, niin koittaa purkaa sen
                    print("Salasana:", pura(fernet, salasanat[nimi]))
                except: #epäonnistuessa oletettavasti syy on väärä pääsalasana
                    print("Virhe: pääsalasana väärä?")
            else:
                print("Tunnistetta ei löytynyt.")

        elif valinta == "3": #luo vahvan salasanan käyttäen secrets, mikä sisältää kirjaimia, numeroita ja symboleja
            vahva = secrets.token_urlsafe(16)
            print("Vahva salasana:", vahva)

        elif valinta == "4":
            break

        else:
            print("Virheellinen valinta.")

if __name__ == "__main__":
    kaynnista()

