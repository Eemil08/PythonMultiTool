import os
import shutil
import sys
from datetime import datetime
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Palauttaa päivämäärän Exif-datasta tai muokkausajasta
def hae_paivamaara(polku):
    try:
        kuva = Image.open(polku)
        exif = kuva._getexif()      #._getefix() hakee kuvan efix-metadatat
        if exif and 36867 in exif:  #36867 on avain, joka meinaa alkuperäistä ottopäivämäärää
            pvm_str = exif[36867]   #pvm merkkijono
            return datetime.strptime(pvm_str, "%Y:%m:%d %H:%M:%S")      #muutaa merkkijonon datetime-objektiksi
    except Exception:   #jos jokin menee vikaan, esim. tiedosto ei ole kuva tai ei ole exif dataa
        pass

    mod_time = os.path.getmtime(polku)  #tiedoston muokausaika (sekunnit 1970 lähtien)
    return datetime.fromtimestamp(mod_time) #muuttaa ylhäällä olevan datetime- objektiksi

# Päätoiminto
def kaynnista():
    tyhjenna_naytto()
    hakemisto = input("Anna kansio, josta kuvat etsitään: ").strip()    #strip() poistaa turhat välilyönnit
    if not os.path.isdir(hakemisto):
        print("Annettu kansio ei ole olemassa.")
        return

    kohdekansio = input("Anna olemassa oleva kohdekansio, johon kuvat kopioidaan: ").strip()
    if not os.path.isdir(kohdekansio):
        print("Kohdekansiota ei ole olemassa. Luo se ensin.")
        return

    print("\nJärjestä kuvat:")
    print("1) Päivämäärän mukaan")
    print("2) Tiedostokoon mukaan")
    valinta = input("Valitse (1/2): ").strip()

    sallitut_tyypit = (".jpg", ".jpeg", ".png", ".tiff")
    kuvapolut = []

    for tiedosto in os.listdir(hakemisto):  #listdir listaa kaikki tiedostot ja kansiot hakemistossa
        polku = os.path.join(hakemisto, tiedosto)
        if os.path.isfile(polku) and tiedosto.lower().endswith(sallitut_tyypit):    #isfile tarkistaa onko tiedosto, eikä kansio
            #tiedosto.lower().... varmistaa, että tiedosto on sallittu kuvatyyppi
            kuvapolut.append(polku)

    if valinta == "1":
        kuvapolut.sort(key=lambda p: hae_paivamaara(p)) #kuville haetaan päivämäärä, minkä mukaan lista järjestetään
    elif valinta == "2":
        kuvapolut.sort(key=lambda p: os.path.getsize(p))    #järjestää kuvat koon mukaan
    else:
        print("Tuntematon valinta.")
        return

    for polku in kuvapolut:
        uusi_polku = os.path.join(kohdekansio, os.path.basename(polku))
        shutil.copy2(polku, uusi_polku) #kopioi tiedostot lähdepolusta päätekansioon
        print(f"> Kopioitu: {os.path.basename(polku)}")

if __name__ == "__main__":
    kaynnista()
