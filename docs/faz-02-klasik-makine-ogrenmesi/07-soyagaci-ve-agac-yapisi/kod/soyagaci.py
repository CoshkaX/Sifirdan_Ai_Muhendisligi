from functools import lru_cache
from typing import Dict, Optional, Tuple


Soyagaci = Dict[str, Optional[Tuple[str, str]]]


def dogrula_soyagaci(soya: Soyagaci) -> None:
    def ziyaret(kisi: str, yol: Tuple[str, ...]) -> None:
        if kisi in yol:
            dongu = " -> ".join((*yol, kisi))
            raise ValueError(f"Soyağacında döngü bulundu: {dongu}")
        ebeveynler = soya[kisi]
        if ebeveynler is None:
            return
        for ebeveyn in ebeveynler:
            ziyaret(ebeveyn, (*yol, kisi))

    for kisi, ebeveynler in soya.items():
        if kisi not in soya:
            raise KeyError(kisi)
        if ebeveynler is None:
            continue
        if len(ebeveynler) != 2:
            raise ValueError(f"{kisi} için iki ebeveyn gerekli")
        for ebeveyn in ebeveynler:
            if ebeveyn not in soya:
                raise ValueError(f"{kisi} kaydı bilinmeyen {ebeveyn} ebeveynini gösteriyor")
        ziyaret(kisi, ())


def akrabalik_katsayisi(soya: Soyagaci, a: str, b: str) -> float:
    """Döngüsüz bir soyağacında iki bireyin akrabalık katsayısını hesaplar."""
    dogrula_soyagaci(soya)
    if a not in soya or b not in soya:
        raise KeyError("Soyağacında bulunmayan birey")

    @lru_cache(maxsize=None)
    def phi(x: str, y: str) -> float:
        if x == y:
            ebeveynler = soya[x]
            if ebeveynler is None:
                return 0.5
            p1, p2 = ebeveynler
            return 0.5 * (1.0 + phi(p1, p2))

        x_ebeveynler = soya[x]
        y_ebeveynler = soya[y]

        if x_ebeveynler is None and y_ebeveynler is None:
            return 0.0
        if x_ebeveynler is None:
            p1, p2 = y_ebeveynler
            return 0.5 * (phi(x, p1) + phi(x, p2))
        if y_ebeveynler is None:
            p1, p2 = x_ebeveynler
            return 0.5 * (phi(p1, y) + phi(p2, y))

        xp1, xp2 = x_ebeveynler
        return 0.5 * (phi(xp1, y) + phi(xp2, y))

    return phi(a, b)
