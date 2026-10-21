"""
main.py - Varastonhallintajärjestelmän komentorivikäyttöliittymä.
"""

import os
import json
from tuote import Tuote

VARASTO_TIEDOSTO = "varasto.json"


def lataa_varasto(tiedostopolku: str = VARASTO_TIEDOSTO) -> list[Tuote]:
    """
    Lataa tuotteet JSON-tiedostosta. Mikäli tiedostoa ei ole tai se on virheellinen,
    palauttaa tyhjän listan.
    """
    if not os.path.exists(tiedostopolku):
        return []

    try:
        with open(tiedostopolku, "r", encoding="utf-8") as tiedosto:
            data = json.load(tiedosto)
            tuotteet = [Tuote.from_dict(item) for item in data]
            return tuotteet
    except json.JSONDecodeError:
        print(f"\nVaroitus: Tiedosto {tiedostopolku} sisältää virheellistä JSON-muotoa.")
        return []
    except Exception as virhe:
        print(f"\nVirhe varaston lataamisessa: {virhe}")
        return []


def tallenna_varasto(tuotteet: list[Tuote], tiedostopolku: str = VARASTO_TIEDOSTO) -> bool:
    """
    Tallentaa tuotelistan JSON-tiedostoon.
    """
    try:
        data = [tuote.to_dict() for tuote in tuotteet]
        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            json.dump(data, tiedosto, indent=2, ensure_ascii=False)
        return True
    except Exception as virhe:
        print(f"\nVirhe varaston tallentamisessa: {virhe}")
        return False


def pyyda_merkkijono(kehote: str, sallitaanko_tyhja: bool = False) -> str:
    """
    Pyytää käyttäjältä merkkijonon ja varmistaa, ettei se ole tyhjä ellei sallita.
    """
    while True:
        try:
            syote = input(kehote).strip()
            if not syote and not sallitaanko_tyhja:
                print("Kenttä ei voi olla tyhjä! Yritä uudelleen.")
                continue
            return syote
        except (KeyboardInterrupt, EOFError):
            print("\nToiminto keskeytetty.")
            return ""


def pyyda_liukuluku(kehote: str, vain_positiivinen: bool = True) -> float:
    """
    Pyytää käyttäjältä liukuluvun (esim. hinta). Tukee myös pilkkua desimaalierottimena.
    """
    while True:
        try:
            syote = input(kehote).strip().replace(",", ".")
            if not syote:
                print("Syöte ei voi olla tyhjä!")
                continue
            luku = float(syote)
            if vain_positiivinen and luku <= 0:
                print("Luvun on oltava positiivinen (suurempi kuin 0)! Yritä uudelleen.")
                continue
            return luku
        except ValueError:
            print("Virheellinen luku! Anna kelvollinen numero (esim. 19.95 tai 19,95).")
        except (KeyboardInterrupt, EOFError):
            print("\nToiminto keskeytetty.")
            raise


def pyyda_kokonaisluku(kehote: str, minimi: int = 0) -> int:
    """
    Pyytää käyttäjältä kokonaisluvun ja varmistaa sen vähimmäisarvon.
    """
    while True:
        try:
            syote = input(kehote).strip()
            if not syote:
                print("Syöte ei voi olla tyhjä!")
                continue
            luku = int(syote)
            if luku < minimi:
                print(f"Luvun on oltava vähintään {minimi}! Yritä uudelleen.")
                continue
            return luku
        except ValueError:
            print("Virheellinen kokonaisluku! Anna numeroina (esim. 10).")
        except (KeyboardInterrupt, EOFError):
            print("\nToiminto keskeytetty.")
            raise


def tulosta_tuotelistaus(tuotteet: list[Tuote]):
    """
    Tulostaa tuotteet selkeästi sarakkeittain muotoiltuna taulukkona.
    """
    viiva = "─" * 78
    print(viiva)
    print(f"{'Tunniste':<10} {'Nimi':<28} {'Hinta (€)':>10} {'Määrä':>8} {'Yhteensä (€)':>14}")
    print(viiva)
    for t in tuotteet:
        print(
            f"{t.tuotenumero:<10} "
            f"{t.nimi[:27]:<28} "
            f"{t.hinta:>10.2f} "
            f"{t.maara:>8} "
            f"{t.laske_kokonaisarvo():>14.2f}"
        )
    print(viiva)


def nayta_kaikki_tuotteet(tuotteet: list[Tuote]):
    """
    Valinta 1: Näyttää kaikki varaston tuotteet.
    """
    print("\n=== KAIKKI VARASTON TUOTTEET ===")
    if not tuotteet:
        print("Varasto on tyhjä.")
        return

    tulosta_tuotelistaus(tuotteet)
    print(f"Tuotteita yhteensä: {len(tuotteet)} kpl eri nimikettä.")


def lisaa_tuote(tuotteet: list[Tuote]):
    """
    Valinta 2: Lisää uuden tuotteen varastoon.
    Tarkistaa duplikaattitunnisteet, tyhjät nimet ja positiivisen hinnan/määrän.
    """
    print("\n=== LISÄÄ UUSI TUOTE ===")
    try:
        # Tuotenumero ja duplikaattitarkistus
        while True:
            tuotenumero = pyyda_merkkijono("Anna tuotenumero (tai 'p' peruuttaaksesi): ")
            if tuotenumero.lower() == 'p':
                print("Tuotteen lisääminen peruutettu.")
                return

            on_duplikaatti = any(t.tuotenumero.lower() == tuotenumero.lower() for t in tuotteet)
            if on_duplikaatti:
                print(f"Virhe: Tuotenumero '{tuotenumero}' on jo käytössä! Valitse toinen tunniste.")
                continue
            break

        nimi = pyyda_merkkijono("Anna tuotteen nimi: ")
        hinta = pyyda_liukuluku("Anna tuotteen hinta (€): ", vain_positiivinen=True)
        # Määrän oltava positiivinen kokonaisluku (vähintään 1)
        maara = pyyda_kokonaisluku("Anna tuotteen määrä (kpl, positiivinen luku): ", minimi=1)

        uusi_tuote = Tuote(tuotenumero, nimi, hinta, maara)
        tuotteet.append(uusi_tuote)

        if tallenna_varasto(tuotteet):
            print(f"\n✓ Tuote '{nimi}' (ID: {tuotenumero}) lisätty onnistuneesti varastoon!")
        else:
            print("\nVaroitus: Tuote lisättiin muistiin, mutta tallennus tiedostoon epäonnistui.")

    except (KeyboardInterrupt, EOFError):
        print("\nLisäys peruutettu keskeytyksen vuoksi.")


def muuta_maaraa(tuotteet: list[Tuote]):
    """
    Valinta 3: Muuttaa olemassa olevan tuotteen varastomäärää.
    Estää negatiiviset luvut.
    """
    print("\n=== MUUTA TUOTTEEN MÄÄRÄÄ ===")
    if not tuotteet:
        print("Varasto on tyhjä, ei muutettavia tuotteita.")
        return

    try:
        tuotenumero = pyyda_merkkijono("Anna muokattavan tuotteen tuotenumero: ")
        loytynyt = next((t for t in tuotteet if t.tuotenumero.lower() == tuotenumero.lower()), None)

        if not loytynyt:
            print(f"Virhe: Tuotetta tuotenumerolla '{tuotenumero}' ei löytynyt.")
            return

        print(f"\nValittu tuote: {loytynyt.nimi}")
        print(f"Nykyinen määrä: {loytynyt.maara} kpl")

        uusi_maara = pyyda_kokonaisluku("Anna uusi määrä (kpl, ei-negatiivinen): ", minimi=0)
        vanha_maara = loytynyt.maara
        loytynyt.maara = uusi_maara

        if tallenna_varasto(tuotteet):
            print(f"\n✓ Tuotteen '{loytynyt.nimi}' määrä päivitetty: {vanha_maara} -> {uusi_maara} kpl.")
        else:
            print("\nVaroitus: Määrä päivitetty muistiin, mutta tallennus epäonnistui.")

    except (KeyboardInterrupt, EOFError):
        print("\nMäärän muuttaminen peruutettu.")


def etsi_tuote(tuotteet: list[Tuote]):
    """
    Valinta 4: Etsii tuotteita nimen tai tuotenumeron osamerkkijonolla (kirjainkoosta riippumaton).
    """
    print("\n=== ETSI TUOTETTA ===")
    if not tuotteet:
        print("Varasto on tyhjä.")
        return

    try:
        hakusana = pyyda_merkkijono("Anna hakusana (etsii nimestä ja tuotenumerosta): ").lower()
        tulokset = [
            t for t in tuotteet
            if hakusana in t.nimi.lower() or hakusana in t.tuotenumero.lower()
        ]

        if not tulokset:
            print(f"\nHakusanalla '{hakusana}' ei löytynyt yhtään tuotetta.")
        else:
            print(f"\nLöytyi {len(tulokset)} hakuehtoa vastaavaa tuotetta:")
            tulosta_tuotelistaus(tulokset)

    except (KeyboardInterrupt, EOFError):
        print("\nHaku peruutettu.")


def poista_tuote(tuotteet: list[Tuote]):
    """
    Valinta 5: Poistaa tuotteen varastosta käyttäjän vahvistuksen (k/e) jälkeen.
    """
    print("\n=== POISTA TUOTE ===")
    if not tuotteet:
        print("Varasto on tyhjä, ei poistettavia tuotteita.")
        return

    try:
        tuotenumero = pyyda_merkkijono("Anna poistettavan tuotteen tuotenumero: ")
        loytynyt = next((t for t in tuotteet if t.tuotenumero.lower() == tuotenumero.lower()), None)

        if not loytynyt:
            print(f"Virhe: Tuotetta tuotenumerolla '{tuotenumero}' ei löytynyt.")
            return

        print(f"\nPoistettava tuote: {loytynyt.nimi} (ID: {loytynyt.tuotenumero}, Määrä: {loytynyt.maara} kpl)")
        vahvistus = input("Haluatko varmasti poistaa tämän tuotteen? (k/e): ").strip().lower()

        if vahvistus in ("k", "kylla", "kyllä"):
            tuotteet.remove(loytynyt)
            if tallenna_varasto(tuotteet):
                print(f"\n✓ Tuote '{loytynyt.nimi}' on poistettu onnistuneesti varastosta.")
            else:
                print("\nVaroitus: Tuote poistettiin muistista, mutta tiedoston tallennus epäonnistui.")
        else:
            print("Poistaminen peruutettu.")

    except (KeyboardInterrupt, EOFError):
        print("\nPoisto peruutettu.")


def nayta_varaston_arvo(tuotteet: list[Tuote]):
    """
    Valinta 6: Laskee ja tulostaa varaston kokonaisarvon ja tilastot.
    """
    print("\n=== VARASTON ARVO JA YHTEENVETO ===")
    if not tuotteet:
        print("Varasto on tyhjä. Kokonaisarvo: 0,00 €")
        return

    kokonaisarvo = sum(t.laske_kokonaisarvo() for t in tuotteet)
    kappalemaara_yhteensa = sum(t.maara for t in tuotteet)
    nimikkeet_yhteensa = len(tuotteet)

    print("┌──────────────────────────────────────────────┐")
    print(f"│ Eri nimikkeitä yhteensä:      {nimikkeet_yhteensa:>14} kpl │")
    print(f"│ Tuotteita varastossa yht.:    {kappalemaara_yhteensa:>14} kpl │")
    print(f"│ Varaston kokonaisarvo:        {kokonaisarvo:>14.2f} € │")
    print("└──────────────────────────────────────────────┘")


def tulosta_valikko():
    """
    Tulostaa ohjelman päävalikon.
    """
    print("\n" + "=" * 40)
    print("      VARASTONHALLINTAJÄRJESTELMÄ      ")
    print("=" * 40)
    print("1. Näytä kaikki tuotteet")
    print("2. Lisää tuote")
    print("3. Muuta tuotteen määrää")
    print("4. Etsi tuote")
    print("5. Poista tuote")
    print("6. Näytä varaston arvo")
    print("0. Lopeta")
    print("=" * 40)


def main():
    """
    Pääohjelmasilmukka.
    """
    print("Käynnistetään Varastonhallintajärjestelmä...")
    tuotteet = lataa_varasto(VARASTO_TIEDOSTO)
    print(f"Varastotiedot ladattu ({len(tuotteet)} tuotetta).")

    while True:
        tulosta_valikko()
        try:
            valinta = input("Valitse toiminto (0-6): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nOhjelma keskeytetty. Näkemiin!")
            break

        if valinta == "1":
            nayta_kaikki_tuotteet(tuotteet)
        elif valinta == "2":
            lisaa_tuote(tuotteet)
        elif valinta == "3":
            muuta_maaraa(tuotteet)
        elif valinta == "4":
            etsi_tuote(tuotteet)
        elif valinta == "5":
            poista_tuote(tuotteet)
        elif valinta == "6":
            nayta_varaston_arvo(tuotteet)
        elif valinta == "0":
            # Varmuustallennus ennen poistumista
            tallenna_varasto(tuotteet)
            print("\nKiitos ohjelman käytöstä. Näkemiin!")
            break
        else:
            print("\nVirheellinen valinta! Valitse numero väliltä 0-6.")


if __name__ == "__main__":
    main()
