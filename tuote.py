"""
tuote.py - Tuote-luokka varastonhallintajärjestelmälle.
"""

class Tuote:
    """
    Luokka edustaa yksittäistä varastossa olevaa tuotetta.
    """

    def __init__(self, tuotenumero: str, nimi: str, hinta: float, maara: int):
        """
        Alustaa uuden Tuote-olion.

        Parametrit:
            tuotenumero (str): Tuotteen uniikki tunniste.
            nimi (str): Tuotteen nimi.
            hinta (float): Tuotteen yksikköhinta euroina.
            maara (int): Tuotteen kappalemäärä varastossa.
        """
        self.tuotenumero = str(tuotenumero).strip()
        self.nimi = str(nimi).strip()
        self.hinta = float(hinta)
        self.maara = int(maara)

    def laske_kokonaisarvo(self) -> float:
        """
        Laskee tuotteen varastoarvon (yksikköhinta * kappalemäärä).

        Palauttaa:
            float: Tuotteen kokonaisarvo euroina.
        """
        return self.hinta * self.maara

    def to_dict(self) -> dict:
        """
        Muuntaa Tuote-olion sanakirjaksi JSON-sarjallistamista varten.

        Palauttaa:
            dict: Tuotteen tiedot sanakirjamuodossa.
        """
        return {
            "tuotenumero": self.tuotenumero,
            "nimi": self.nimi,
            "hinta": round(self.hinta, 2),
            "maara": self.maara
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tuote":
        """
        Luo uuden Tuote-olion sanakirjasta (desarjallistaminen).

        Parametrit:
            data (dict): Tuotteen tiedot sisältävä sanakirja.

        Palauttaa:
            Tuote: Luotu Tuote-olio.
        """
        return cls(
            tuotenumero=str(data.get("tuotenumero", "")),
            nimi=str(data.get("nimi", "")),
            hinta=float(data.get("hinta", 0.0)),
            maara=int(data.get("maara", 0))
        )

    def __str__(self) -> str:
        """
        Palauttaa tuotteen selkeän merkkijonoesityksen.
        """
        return (
            f"Tunniste: {self.tuotenumero:<8} | "
            f"Nimi: {self.nimi:<26} | "
            f"Hinta: {self.hinta:>8.2f} € | "
            f"Määrä: {self.maara:>5} kpl | "
            f"Kokonaisarvo: {self.laske_kokonaisarvo():>10.2f} €"
        )

    def __repr__(self) -> str:
        return f"Tuote(tuotenumero='{self.tuotenumero}', nimi='{self.nimi}', hinta={self.hinta}, maara={self.maara})"
