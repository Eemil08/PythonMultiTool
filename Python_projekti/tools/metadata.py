import os
from PIL import Image
import piexif

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def poista_ja_tallenna_metadata(hakemisto):
    metadata_tiedosto = os.path.join(hakemisto, "metadata.txt")
    with open(metadata_tiedosto, "w", encoding="utf-8") as f:
        for juurisijainti, _, tiedostot in os.walk(hakemisto):  #os.walk() käy läpi kaikki kansiot ja alikansiot.
            #(samanlainen tiedostojen läpikäynti järjestelmä on selitetty koodissa duplikaatit.py)
            for tiedosto in tiedostot:
                if tiedosto.lower().endswith((".jpg", ".jpeg")): #endswith(...)  sallii vain .jpg ja.jpeg kuvat
                    polku = os.path.join(juurisijainti, tiedosto)
                    try:
                        kuva = Image.open(polku) #avaa kuvan käsiteltäväksi
                        exif_data = kuva.info.get("exif") #kuva.info on sanakirja, missä on kuvan metadataa. exif avain sisältää alkuperäisen exif binääridatan.
                        #- ja jos sitä ei ole, niin siirytään seuraavaan kuvaan
                        if exif_data:   #jos Exif löytyy:
                            exif_dict = piexif.load(exif_data)  #piefix.load() muuntaa exif binäärin luettavaksi sanakirjaksi
                            #piefix jakaa exif-tiedon eri kategorioihin esimerkiksi "0th", mikä sisältää perustietoja kuten kameran merkki, malli, kuvauksen aika jne...
                            #sekä esim "GPS" kertoo GPS koordinaatit. Kategorioita on 6
                            f.write(f" {polku} \n")
                            for ifd in exif_dict:   #ifd on exif-kategoria (käy läpi kaikki kategoriat)
                                for tag in exif_dict[ifd]:  #tag on avain kussakin kategoriassa (niissä on paljon tägejä ja tag on numero, mikä tarkoittaa jotain (esim. "make" eli kameran merkki))
                                    try:
                                        nimi = piexif.TAGS[ifd][tag]["name"] #piexif.TAGS[ifd][tag]["name"] hakee tägin nimen (muuttaa numeron luettavaksi nimeksi)
                                        arvo = exif_dict[ifd][tag]  #hakee tägin arvon
                                        f.write(f"{nimi}: {arvo}\n")
                                    except Exception:
                                        continue
                            f.write("\n")
                            #exif=b"" nollaa metadatan
                            kuva.save(polku, "jpeg", exif=b"") #kuva.save() tallentaa kuvan alkuperäisen päälle ilman metadataa
                            print(f"Exif poistettu: {polku}")
                        else:
                            print(f"Ei Exif-dataa: {polku}")
                    except Exception as e:
                        print(f"Virhe kuvassa {polku}: {e}")
    
    print(f"\nReportti tallennettu tiedostoon: {metadata_tiedosto}")


def kaynnista():
    tyhjenna_naytto()
    print("Kuvan metadatan tarkastelu ja poisto")
    hakemisto = input("Anna polku, mistä kuvat etsitään: ").strip('"')
    if not os.path.exists(hakemisto):
        print("Kansiota ei löytynyt.")
        return
    poista_ja_tallenna_metadata(hakemisto)

if __name__ == "__main__":
    kaynnista()

