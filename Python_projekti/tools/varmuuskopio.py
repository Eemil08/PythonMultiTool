import os
import shutil

def tyhjenna_naytto():
    os.system('cls' if os.name == 'nt' else 'clear')

def kaynnista():
    tyhjenna_naytto()
    lahde = input("Anna hakemisto, jonka haluat varmuuskopioida: ").strip() #strip() poistaa välilöynnit alusta ja lopusta
    if not os.path.exists(lahde):
        print("Lähdekansiota ei löytynyt.")
        return

    kohde_perus = input("Anna hakemisto, minne varmuuskopio tallennetaan: ").strip()
    if not kohde_perus:
        print("Kohdekansiota ei annettu.")
        return

    os.makedirs(kohde_perus, exist_ok=True)

    for root, dirs, files in os.walk(lahde):    #käy läpi kaikki kansiot ja tiedostot lahde kansiossa
        for tiedosto in files:
            lahdepolku = os.path.join(root, tiedosto)   #muodostaa tiedostopolun

            suhteellinen_polku = os.path.relpath(lahdepolku, lahde)     #tiedoston sijainti suhteessa lähdekansioon
            kohdepolku = os.path.join(kohde_perus, suhteellinen_polku)

            os.makedirs(os.path.dirname(kohdepolku), exist_ok=True)     #luo tarvittavt alikansiot kohteessa

            shutil.copy2(lahdepolku, kohdepolku)
            #kopioi tiedoston ja säilyttää muokkaus- ja luontiajat

    print(f"\n Varmuuskopiointi valmis.\nTiedostot tallennettu: {kohde_perus}")

if __name__ == "__main__":
    kaynnista()

