from dataclasses import dataclass


@dataclass(frozen=True)
class Gözlem:
    özellikler: dict[str, object]


class BasitKararSistemi:
    """Gözlemleri belleğe kaydeden ve basit kurallarla karar veren küçük bir örnek."""

    def __init__(self, kurallar: dict[str, tuple[object, str]]) -> None:
        self.bellek: list[Gözlem] = []
        self.kurallar = kurallar

    def gözlemle(self, özellikler: dict[str, object]) -> Gözlem:
        gözlem = Gözlem(özellikler)
        self.bellek.append(gözlem)
        return gözlem

    def çıkarım_yap(self, gözlem: Gözlem) -> tuple[str, str]:
        for anahtar, (beklenen, açıklama) in self.kurallar.items():
            if gözlem.özellikler.get(anahtar) == beklenen:
                return anahtar, açıklama
        return "belirsiz", "Hiçbir tanımlı kural gözlemle eşleşmedi."

    def özetle(self) -> dict[str, int]:
        özet: dict[str, int] = {}
        for gözlem in self.bellek:
            for anahtar in gözlem.özellikler:
                özet[anahtar] = özet.get(anahtar, 0) + 1
        return özet


if __name__ == "__main__":
    sistem = BasitKararSistemi({
        "hava": ("yağmurlu", "Islak zeminde kayma riski artabilir."),
        "plan": ("bahçede fidan dikmek", "Fidanı dikmeden önce toprağın nemini kontrol et."),
    })

    for gözlem in (
        {"hava": "yağmurlu", "plan": "eve gitmek"},
        {"hava": "güneşli", "plan": "bahçede fidan dikmek"},
    ):
        kaydı = sistem.gözlemle(gözlem)
        anahtar, açıklama = sistem.çıkarım_yap(kaydı)
        print(f"{anahtar}: {açıklama}")

    print("Bellek özeti:", sistem.özetle())
