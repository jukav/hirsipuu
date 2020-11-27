import sys  # Ladataan sys- moduli
import random  # Ladataan random- moduli
import string  # Ladataan string- moduli
import pickle  # Ladataan pickle- moduli


def menu():  # Valikon tulostus
    print("")
    print("")
    print("**** HIRSIPUU- peli ***")
    print("#######################")
    print("")
    print("Valikko:")
    print("1) Pelaa")
    print("2) Ohjeet")
    print("3) Tulostaulu")
    print("4) Lisää sana listaan")
    print("5) Tulosta sanalista")
    print("6) Tyhjennä sanalista")
    print("7) Tyhjennä tulostaulu")
    print("8) Lopeta peli")


def pelaa():  # Vertaa arvauksia satunnaisiin sanoihin listalta
    lista = (hae_sanalista())  # Hakee sanalistan tiedostosta
    if len(lista) < 3:  # Jos sanoja alle 3
        print("Listassa liian vähän sanoja. Lisää sana listaan")
        main()  # Palaa pääohjelmaan
    else:  # Suoritus jatkuu, jos 3 tai enenmmän sanaa listassa
        s_lista = random.sample(lista,3)  # Valitse 3 satunnaista sanaa listasta
        virheita = 0  # Asetetaan virhelaskuri
        for q in range(1, 4):  # Pelataan 3 kierrosta
            print("Kierros", q, "/3")
            sana = s_lista[q - 1]  # Valitsee arvattavan sanan listasta
            sana_t = "_" * len(sana)  # Muodostetaan täydennettävä sana
            arvattu = False  # Asetetaan totuusarvo, onko aravus valmis
            arvatut_kirjaimet = []  # Alustetaan lista arvatuista kirjaimista
            arvatut_sanat = []  # Alustetaan lista arvatuista sanoista
            yrityksia = 7  # Asetetaan 7 arvauskertaa/ sana
            print("Pelataan Hirsipuuta!")
            print(sana_t)
            print("\n")
            while not arvattu and yrityksia > 0:  # Suoritaan peliä kunnes arvaus valmis tai yritykset loppuvat
                arvaus= input("Arvaa sanan kirjain ")  # Kysytään kirjainta
                arvaus = arvaus.lower() # Mutetaan kirjain pieneksi
                if len(arvaus) == 1 and arvaus.isalpha():  # Suoritetaan jos arvaus sallittu (kirjain)
                    if arvaus in arvatut_kirjaimet:  # Tarkistetaan onko arvattu kirjainta aiemmin
                        print("Arvasit jo kirjaimen", arvaus)
                    elif arvaus not in sana:  # Suoritetaan jos arvattu kirjain ei ole sanassa
                        print(arvaus, "kirjain ei ole sanassa")
                        yrityksia -= 1  # Vähennetään yrityslaskuria
                        virheita += 1  # Lisätään virhelaskuriin 1
                        arvatut_kirjaimet.append(arvaus)  # Lisätään kirjain arvattujen listaan
                        print("Sinulla on ", yrityksia, "yritystä jäljellä")
                    else:  # Suortetaaan jos arvattu kirjain on sanassa
                        print("Hienoa! Arvasit oikein.", arvaus, "on sanassa")
                        arvatut_kirjaimet.append(arvaus)  # Lisätään arvattu kirjain listaan
                        sanat_listaan = list(sana_t)  # listaan arvattu sana
                        indeksit = [i for i, kirjain in enumerate(sana) if kirjain == arvaus] # Muodostetaan indeksit arvatuista kirjaimista
                        for indeksi in indeksit:  # Käydään läpi sanan indeksit
                            sanat_listaan[indeksi] = arvaus  # Muodostetaan lista arvatuista kirjaimista
                        sana_t = "".join(sanat_listaan) # Päivitetään arvattavaa sanaa
                        if "_" not in sana_t:  # Jos sana ei sisällä "_", ts. arvattu kokonaan
                            arvattu = True  # Sana arvattu, arvattu totuusarvo: True
                elif len(arvaus) == len(sana) and arvaus.isalpha():  # Jos muuttuja aravaus sis. yhtä monta kirjainta kuinmuuttuja sana ja arvaus sis. kirjaimet
                    if arvaus in arvatut_sanat:  # Jos arvaus on arvattujen joukossa
                        print("Arvasit jo sanan", arvaus)
                    elif arvaus != sana:  # Jos arvaus ei ole sana
                        print(arvaus, "ei ole sana")
                        yrityksia -= 1  # Vähennetään 1 yriksiä laskurista
                        virheita += 1  # Lisätään 1 virhelaskuriin
                        arvatut_sanat.append(
                            arvaus)  # Lisätään arvaus arvattuihin sanoihin
                else:  # Suoritetaan muutoin
                    print("Ei sallittu arvaus. Arvaa yksi kirjain kerrallaan.")
                tulosta_puu(yrityksia)  # Tulostaa hirsipuuta lisää virheiden myötä
                print(sana_t)  # Tulostaa arvatun sanan
            if arvattu:  # Suoritetaan jos koko sana arvattu
                print("")
                print("Hienoa! Läpäisit kierroksen", q, "/ 3")
            else:  # Jos arvauskerrat loppuvat
                print("")
                print("Pahus! Joudut hirsipuuhun. Sana oli", sana)
                main()  # Paluu pääohjelmaan
        print("Onnittelut! Läpäisit pelin")
        print("Arvasit väärin", virheita, "kertaa")
        tallenna_tulos(virheita)  # Kutsuu metodia tallentamaan pelaajan tulos


def tallenna_tulos(t):  # Talletaan tulos tiedostoon
    virheita = str(t)  # Muutetaan virheet- lukuarvo merkkijoksi
    nimi = input("Annan nimesi ")  # Kysytään pelaajan nimi
    print("Hienoa", nimi, "vääriä arvauksia",
          virheita)  # Tulostetaan pelaaja ja virhepisteet
    tulos_taulu = {'nimi': nimi,'virhepisteet': virheita}  # Muodostetaan hajautustaulu (nimi ja virheet)
    pickle.dump(tulos_taulu, open("tulos_taulu.txt", "ab"))  # Tallennetaan taulu- objekti tiedostoon


def hae_tulos():  # Haetaan tulokset tiedostostosta
    try: # Blokki käsittelee virheen
        tiedosto = open("tulos_taulu.txt", "r") # Avataan tiedosto
    except FileNotFoundError:  # Suorittaa jos virhe: FileNotFoundError
        print("Tulostaulu on tyhjä")
        main()  # Palataan pääohjelmaan
    print("")
    print("TULOSTAULU:")
    print("")
    with open('tulos_taulu.txt', 'rb') as f:  # Määritellään f
        while True:  # Loppumaton silmukka
            try:  # Käsitellään virhe blokissa
                a = pickle.load(f)  # Haetaan taulu- objektit tiedostosta
            except EOFError:  # Suorittaa jos virhe: End of file
                break  # Poistutaan metodista
            else:  # Suoritetaan muutoin
                print(a)  # Tulostetaan tulokset objekti kerrallaan


def ohjeet():  # Tulostaa pelin ohjeet
    print("")
    print("HIRSIPUUPELI")
    print("")
    print("Arvaa piilossa oleva sana kirjain kerrallaan.")
    print("Sana paljastuu sitä mukaa kun arvaat oikean kirjaimen.")
    print("Voit arvata kirjaimia seitsemän kertaa jokaisessa sanassa.")
    print("Jos epäonnistut arvaamaan sanan joudut hirsipuuhun.")
    print("Läpäiset pelin kun selvität kolme kierrosta.")
    print("Voit lisätä arvattavia sanoja valikosta.")
    print("")
    print("Onnea peliin!")


def lisaa_listaan():  # Lisätään sana listaan
    print("lisää listaan")
    tyhja = False
    while True:  # Loppumaton silmukka
        x = 0 # Aseteaan muuttuja x
        sana = input("Kirjoita sana: ")  # Kysytään sana
        for char in sana: # Kädään läpi merkit sanassa
            if char in string.ascii_letters:  # Jos merkit ovat kirjain
                x = x + 1 # Lisätään x- muttujan arvoa yhdellä
        if x == len(sana):  # Jos x= sanan pituus, niin kirjaimet on käyty läpi
            break  # Poistu silmukasta
        else:  # Suorita muutoin
            print("Käytä sanassa ainoastaan kirjaimia.")
            print("Skandinaavisia kirjaimia ei hyväksytä.")
            print("")
            continue  # Palaa silmukan alkuun
    sana = str.lower(sana)  # Muuttaa sanan kirjaimet pieniksi

    try:# Blokki käsittelee virheen
        tiedosto = open("sanalista.txt", "r")  # Avaa tiedosto
    except FileNotFoundError:  # Suorittaa jos virhe: tiedostoa ei löytynyt
        print("Sanalista: sanalista.txt tehtiin")
        tyhja = True  # Sanalista tyhjä, tyhja = True
    else: # Suorita muutoin
        merkki = tiedosto.read(1)  # Luetaan tiedosto
        if not merkki:  # Jos tiedosto tyhjä
            tyhja = True  # Sanalista tyhjä, tyhja = True
        tiedosto.close()  # Suljetaan tiedosto

    try:  # Blokki käsittelee virheen tiedostoa ei löytynyt
        tiedosto = open("sanalista.txt", "a")  # Avaa tiedosto
    except FileNotFoundError:  # suorittaa jo virhe: FileNotFoundError
        print("Virhe: Tiedostoa ei löytynyt")
        sys.exit(-1)  # Keskeytä suoritus
    else:  # Suorita muutoin
        if tyhja == True:  # Jos tiedosto tyhjä
            tiedosto.write(sana)  # Kirjoita sana tiedostoon
        else:  # muutoin
            tiedosto.write(
                "\n" + sana)  # Kirjoita merkki rivin vaihto "\n" + sana
        tiedosto.close()  # Sulje tiedosto


def hae_sanalista():  # Hakee sanalistan tiedostosta
    try:  # Blokki käsittelee virheen tiedostoa ei löytynyt
        tiedosto = open("sanalista.txt", "r")  # Avaa tiedoston
    except FileNotFoundError:  # Suorittaa jos virhe: file not found
        print("Virhe: tiedostoa ei löytynyt")
        sys.exit(-1)  # Suoritus keskeytyy
    if tiedosto.read(1) == "":  # Jos sanalista on tyhjä
        print("Sanalista on tyhjä. Lisää sana listaan")
        main()  # Palaa pääohjelmaan
    tiedosto.seek(0)  #
    sanalista = []  # Alustetaan sanalista
    for line in tiedosto:  # Käydään tiedoston rivit läpi
        l = len(line)  # l = rivin pituus
        if line[l - 1] == "\n":  # Jos sanassa on "\n" merkki
            line = line[:-1]  # Poistetaan sanasta "\n" merkki
        sanalista.append(line)  # Lisää sanan listaan
    return sanalista  # Palauttaa sanalistan


def tyhjenna_lista():  # Tyhjentää sanalistan
    vastaus = input("Haluatko varmasti tyhjentää listan? k = kyllä, e = ei ")  # Varmistaa tyhjennyksen
    if vastaus == "e":  # Jos vastaus ei (e)
        main()  # Palaa pääohjelmaan
    elif vastaus == "k":  # Jos vastaus kyllä (k)
        file = open("sanalista.txt", "r+")  # Avaa tiedoston
        file.truncate(0)  # Tyhjentää tiedoston
        file.close()  # Sulkee tiedoston
        print("Sanalista on tyhjennetty!")
    else:
        tyhjenna_lista()  #  Kutsuu suoritettavaa metodia, ts. palaa alkuun


def tyhjenna_tulos():  # Tyhjentää tulostaulun
    vastaus = input("Haluatko varmasti tyhjentää tulostaulun? k = kyllä, e = ei ")  # Varmistetaan tyhjennys
    if vastaus == "e":  #  Suoritetaan jos ei
        main()  # Palaa pääohjelmaan
    elif vastaus == "k":  # Suoritetaan jos kyllä
        file = open("tulos_taulu.txt", "r+")  # Avataan tiedosto
        file.truncate(0)  # Tyhjennetään tiedosto
        file.close()  # suljetaan tiedosto
        print("Tuloslista on tyhjennetty!")
    else:  # Suoritetaan muutoin
        tyhjenna_tulos()  # Kutsutaan metodia uudestaan, ts. palataan alkuun


def tulosta_puu(x):  # Tulostetaan hirsipuu vaiheittain virheiden myötä
    if x == 6:
        print("           ")
        print("           ")
        print("           ")
        print("           ")
        print("           ")
        print(" __________")

    if x == 5:
        print("            ")
        print("            ")
        print("            ")
        print("            ")
        print("           |")
        print(" __________|")

    if x == 4:
        print("            ")
        print("            ")
        print("           |")
        print("           |")
        print("           |")
        print(" __________|")
    if x == 3:
        print("           |")
        print("           |")
        print("           |")
        print("           |")
        print("           |")
        print(" __________|")
    if x == 2:
        print("     ______")
        print("           |")
        print("           |")
        print("           |")
        print("           |")
        print(" __________|")

    if x == 1:
        print("   ________")
        print("   |       |")
        print("           |")
        print("           |")
        print("           |")
        print(" __________|")

    if x == 0:
        print("   ________")
        print("   |       |")
        print("   |       |")
        print("   O       |")
        print("           |")
        print(" __________|")
    print("")



def main(): # Pääohjelma, kutsuu eri metodeja valinnan mukaan
    while True: # Loputon silmukka
        menu() # Tulostaa valikon
        while True: # Loputon silmukka
            try: # Blokki käsittelee virheen: ValueError
                print("")
                valinta = int(input("Valintasi: ")) # Kysyy käyttäjän valintaa
                if valinta >= 1 and valinta <= 8: # Jos valinta 1-8 välillä
                    break # Poistu silmukasta
                else: # Muutoin suorita
                    print("Valitse 1,2,3,4,5,6,7 tai 8")
            except ValueError: # Suorittaa, jos virhe: ValueError
                print("Valitse 1,2,3,4,5,6,7 tai 8")

        if valinta == 1: # Jos valinta 1
            pelaa() # Kutsuu pelaa() metodia (peli alkaa)
        elif valinta == 2:# Jos valinta 2
            ohjeet() # Kutsuu ohjeet() metodia (tulostaa ohjeet)
        elif valinta == 3: # Jos valinta 3
            hae_tulos() # kutsuu hae_tulos() metodia (näyttää tulostaulun)
        elif valinta == 4: # Jos valinta 4
            lisaa_listaan() # Kutsuu lisaa_listaan() metodia (lisää sanan listaan)
        elif valinta == 5: # Jos valinta 5
            print("")
            print(hae_sanalista()) # Kutsuu hae_sanalista() metodia (tulostaa sanalistan)
        elif valinta == 6: # Jos valinta 6
            tyhjenna_lista() # Kutsuu tyhjenna_lista() metodia (tyhjentää sanalistan)
        elif valinta == 7: # Jos valinta 7
            tyhjenna_tulos() # Kutsuu tyhjenna_tulos() (tyhjentää tulostaulun)
        else: # Muutoin suorita
            print("Heippa!")
            sys.exit() # Keskeyttää ohjelman suorituksen


main() # Kutsuu pääohjelmaa ja käynnistää pelin
