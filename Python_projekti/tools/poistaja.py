import os
import ctypes

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def poista_tiedosto(polku): #windowsin määritelmiä mitä tarvitaan CreateFilew-funktiolle
    GENERIC_WRITE = 0x40000000 #avaa tiedoston kirjoitusoikeudella
    FILE_SHARE_DELETE = 0x00000004 #sallii poiston vaikka tiedostoa käytetään
    OPEN_EXISTING = 3 #avaa vain, jos tiedosto on olemassa
    FILE_FLAG_DELETE_ON_CLOSE = 0x04000000 #poistaa tiedoston heti kun kahva suljetaan

    kahva = ctypes.windll.kernel32.CreateFileW(polku,GENERIC_WRITE,FILE_SHARE_DELETE,None,OPEN_EXISTING,FILE_FLAG_DELETE_ON_CLOSE,None)
       #Windows C-funktio joka avaa tiedoston ja palauttaa kahvan siihen.#Jos kahva onnistuu niin tiedosto merkistään poistettavaksi heti kun kahva suljetaan.
       #Palautuu -1 jos ei onnistunut. 

    if kahva == -1: #tarkistetaan epäonnistuiko tiedoston avaaminen
        print("CTypes-poisto ei onnistunut. Yritetään os.remove()")
        try: #jos ctypes ei toimi, niin käytetään os.remove()
            os.remove(polku)
            print(f"Tiedosto poistettu os.remove(): {polku}")
        except Exception as e:
            print(f"Virhe: Tiedoston poisto epäonnistui. ({e})")
        return

    ctypes.windll.kernel32.CloseHandle(kahva) #sulkee kahvan. Kun kahva suljetaan, niin Windows vapauttaa tiedoston ja poistaa sen
    print(f"Tiedosto poistettu: {polku}")

def kaynnista():
    tyhjenna_naytto()
    print("=== Tiedostopoistaja ===")
    polku = input("Anna poistettavan tiedoston polku: ").strip('"')
    if not os.path.isfile(polku):
        print("Tiedostoa ei löytynyt.")
        return
    poista_tiedosto(polku)

if __name__ == "__main__":
    kaynnista()

