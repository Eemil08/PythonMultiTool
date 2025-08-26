import os
import hashlib
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))     #sys.argv[0] sisältää polun skriptiin, josta ohjelma käynnistetään, os.path.asbath(...) muuntaa sen täydelliseksi poluksi, os.path.dirname(...)Poistaa tiedostonimen, jäljelle jää kansio, os.chdir(...)Asettaa sen nykyiseksi työhakemistoksi
#eli lyhyesti muuttaa käyttäjän "nykisen sijainnin", sinne missä koodi suoritetaan

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')

def hash_haku(tiedostopolku):
    hasher = hashlib.md5()  #toimii ns "sormenjälkenä", mikä luodaan tiedoston sisällöstä
    try:
        with open(tiedostopolku, 'rb') as f:    #avaa binääri muodossa tarkan sisällön vuoksi
            for chunck in iter(lambda: f.read(4096), b""):  #lukee tiedoston osissa (kerrallaan 4096 tavua)
                hasher.update(chunck)   #syöttää aina osan hajautuslaskentaan
        return hasher.hexdigest()   #palauttaa hashin merkkijonona (käytetään vertaamiseen)
    except:
        return None
    
def kaynnista():
    tyhjenna_naytto()
    hakemisto = input("Anna hakemisto, mistä etsitään duplikaatit: ")
    tiedostot = {}
    for root, _, files in os.walk(hakemisto):       #käy läpi koko hakemistorakenteen (root on se päähakemisto, dir on "_" sillä sitä ei käytetä
        for file in files:                          #ja files on  on lista kansion tiedostonimistä
            polku = os.path.join(root, file)        #yhdistää hakemiston ja tiedoston
            file_hash = hash_haku(polku)            #lasketaan tiedoston hash
            if file_hash:
                tiedostot.setdefault(file_hash, []).append(polku)
             
    raporttikansio = "Raportit"                  
    os.makedirs(raporttikansio, exist_ok=True)
    
    raporttipolku = os.path.join(raporttikansio, "duplikaatit_Raportti.txt")

    with open(raporttipolku, "w", encoding="utf-8") as raportti:    #"utf8" avulla, varmistetaan, että ääkköset toimivat
        for hash_,paths in tiedostot.items():       
            if len(paths) > 1:      #jos "paths" sisältää yhden tiedoston, se ei ole duplikaatti
                raportti.write(f"\nDuplikaatti ({len(paths)} kpl):\n")         
                for path in paths:      #käy läpi jokaisen tiedostopolun, jolla on sama hash          
                    raportti.write(f" {path}\n")
    print(f"\nHaku valmis. Löydät tulokset täältä: {raporttipolku}")
    print("(Jos duplikaatteja ei löytynt, silloin tiedosto on tyhjä)")
    input(f"\npaina Enter sulkeaksesi ")

if __name__ == "__main__":
    kaynnista()

