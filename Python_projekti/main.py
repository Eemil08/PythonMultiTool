import os
from tools import duplikaatit, kuvajarjestaja, metadata, poistaja, salasanamanageri, varmuuskopio

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        tyhjenna_naytto()
        print("    Monitoimityökalu    ")
        print("1. Duplikaatit")
        print("2. Kuvajärjestäjä")
        print("3. Metadatan tarkastus/poisto")
        print("4. Tiedostopoistaja")
        print("5. Salasanamanageri")
        print("6. Varmuuskopiointi")
        print("0. Poistu")

        valinta = input("Valinta: ")

        if valinta == "1":
            duplikaatit.kaynnista()
        elif valinta == "2":
            kuvajarjestaja.kaynnista()
        elif valinta == "3":
            metadata.kaynnista()
        elif valinta == "4":
            poistaja.kaynnista()
        elif valinta == "5":
            salasanamanageri.kaynnista()
        elif valinta == "6":
            varmuuskopio.kaynnista()
        elif valinta == "0":
            print("Poistutaan ohjelmasta...")
            break
        else:
            print("Virheellinen valinta.")
        input("\nPaina Enter jatkaaksesi...")

if __name__ == "__main__":
    main()

