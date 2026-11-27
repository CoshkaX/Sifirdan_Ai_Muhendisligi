"""Ders 5.6 – Mini transformer: sonraki token'ı tahmin etmeyi öğrenen küçük bir model.

PyTorch gerekir. Çalıştır:  python kod/mini_transformer.py

Görev: Dizi "a b a b a b a b" biçimindedir ve a ile b her dizide rastgele seçilir.
Model, her konumda sonraki token'ı tahmin eder. Bunun için bağlamda geriye bakması gerekir.
"""

import math

import torch
from torch import nn

SOZLUK, UZUNLUK, D, KAFA, KATMAN = 8, 8, 32, 2, 2


def veri_uret(n):
    """n tane (n, UZUNLUK) boyutlu dizi üretir: a b a b a b a b."""
    a = torch.randint(0, SOZLUK, (n, 1))
    b = torch.randint(0, SOZLUK, (n, 1))
    return torch.cat([a, b] * (UZUNLUK // 2), dim=1)


class Blok(nn.Module):
    def __init__(self, d, kafa_sayisi):
        super().__init__()
        self.norm1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, kafa_sayisi, batch_first=True)
        self.norm2 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))

    def forward(self, x, maske):
        h = self.norm1(x)
        x = x + self.attn(h, h, h, attn_mask=maske, need_weights=False)[0]
        return x + self.ffn(self.norm2(x))


class MiniTransformer(nn.Module):
    def __init__(self, maskeli=True):
        super().__init__()
        self.maskeli = maskeli
        self.token_gomme = nn.Embedding(SOZLUK, D)
        self.konum_gomme = nn.Embedding(UZUNLUK - 1, D)
        self.bloklar = nn.ModuleList([Blok(D, KAFA) for _ in range(KATMAN)])
        self.norm = nn.LayerNorm(D)
        self.cikis = nn.Linear(D, SOZLUK)

    def forward(self, idler):
        n, t = idler.shape
        x = self.token_gomme(idler) + self.konum_gomme(torch.arange(t))
        maske = torch.triu(torch.ones(t, t, dtype=torch.bool), diagonal=1) if self.maskeli else None
        for blok in self.bloklar:
            x = blok(x, maske)
        return self.cikis(self.norm(x))


def kayip_hesapla(model, dizi):
    girdi, hedef = dizi[:, :-1], dizi[:, 1:]
    return nn.functional.cross_entropy(model(girdi).reshape(-1, SOZLUK), hedef.reshape(-1))


def egit(model, adim_sayisi=800, batch=64, ogrenme_hizi=3e-3, kayit_adimlari=(1, 100, 800)):
    optimizer = torch.optim.Adam(model.parameters(), lr=ogrenme_hizi)
    kayitlar = {}
    for adim in range(1, adim_sayisi + 1):
        kayip = kayip_hesapla(model, veri_uret(batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
        if adim in kayit_adimlari:
            kayitlar[adim] = kayip.item()
    return kayitlar


def dogruluk(model, n=1000):
    """Tahmin edilebilir hedeflerde (3. token'dan itibaren) doğruluk."""
    with torch.no_grad():
        dizi = veri_uret(n)
        tahmin = model(dizi[:, :-1]).argmax(dim=-1)
    return (tahmin[:, 1:] == dizi[:, 2:]).float().mean().item()


def uret(model, bas, uzunluk=UZUNLUK):
    """Verilen başlangıç token'larından açgözlü (en olası token) üretim."""
    idler = torch.tensor([bas])
    with torch.no_grad():
        while idler.shape[1] < uzunluk:
            sonraki = model(idler)[:, -1].argmax(dim=-1, keepdim=True)
            idler = torch.cat([idler, sonraki], dim=1)
    return idler[0].tolist()


def main():
    torch.manual_seed(0)
    model = MiniTransformer()
    print("Parametre sayısı:", sum(p.numel() for p in model.parameters()))
    print("Kaçınılmaz kayıp:", round(math.log(SOZLUK) / (UZUNLUK - 1), 2))
    for adim, kayip in egit(model).items():
        print(f"Adım {adim}: kayıp {kayip:.1f}")
    torch.manual_seed(123)
    print("Doğruluk:", round(dogruluk(model), 2))
    print("Üretim:", uret(model, [2, 5]))


if __name__ == "__main__":
    main()
