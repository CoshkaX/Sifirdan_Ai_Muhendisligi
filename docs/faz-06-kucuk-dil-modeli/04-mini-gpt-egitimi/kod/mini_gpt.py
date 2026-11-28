"""Ders 6.4 – Mini GPT: küçük bir Türkçe metinde karakter düzeyinde dil modeli eğitmek.

PyTorch gerekir. Çalıştır:  python kod/mini_gpt.py

Adımlar: metni oku → karakterleri sayılara çevir → eğitim/doğrulama diye ikiye böl →
rastgele pencerelerden batch al → 5.6'daki transformer'ı sonraki karakteri tahmin etmeye eğit →
belirli aralıklarla iki kaybı da ölç → eğitilmiş modelle metin üret.
"""

import math
import pathlib

import torch
from torch import nn

VERI_YOLU = pathlib.Path(__file__).parent / "veri" / "kasaba.txt"
BLOK, D, KAFA, KATMAN, DROPOUT = 32, 32, 4, 2, 0.2


# ---------- Veri ----------

def veri_hazirla(metin):
    """Karakter sözlüğünü kurar; metni sayılara çevirip %90 eğitim, %10 doğrulama diye böler."""
    karakterler = sorted(set(metin))
    stoi = {k: i for i, k in enumerate(karakterler)}
    veri = torch.tensor([stoi[k] for k in metin])
    sinir = int(len(veri) * 0.9)
    return karakterler, stoi, veri[:sinir], veri[sinir:]


def batch_al(veri, batch, blok=BLOK):
    """Metnin rastgele yerlerinden `batch` tane pencere alır. Hedef, girdinin bir sağa kaymışıdır."""
    baslar = torch.randint(0, len(veri) - blok - 1, (batch,))
    girdi = torch.stack([veri[i:i + blok] for i in baslar])
    hedef = torch.stack([veri[i + 1:i + blok + 1] for i in baslar])
    return girdi, hedef


# ---------- Model (5.6'daki transformer) ----------

class Blok(nn.Module):
    def __init__(self, d, kafa_sayisi):
        super().__init__()
        self.norm1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, kafa_sayisi, dropout=DROPOUT, batch_first=True)
        self.norm2 = nn.LayerNorm(d)
        self.ffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d), nn.Dropout(DROPOUT))

    def forward(self, x, maske):
        h = self.norm1(x)
        x = x + self.attn(h, h, h, attn_mask=maske, need_weights=False)[0]
        return x + self.ffn(self.norm2(x))


class MiniGPT(nn.Module):
    def __init__(self, sozluk_boyutu):
        super().__init__()
        self.token_gomme = nn.Embedding(sozluk_boyutu, D)
        self.konum_gomme = nn.Embedding(BLOK, D)
        self.bloklar = nn.ModuleList([Blok(D, KAFA) for _ in range(KATMAN)])
        self.norm = nn.LayerNorm(D)
        self.cikis = nn.Linear(D, sozluk_boyutu)

    def forward(self, idler):
        t = idler.shape[1]
        x = self.token_gomme(idler) + self.konum_gomme(torch.arange(t))
        maske = torch.triu(torch.ones(t, t, dtype=torch.bool), diagonal=1)
        for blok in self.bloklar:
            x = blok(x, maske)
        return self.cikis(self.norm(x))


def kayip_hesapla(model, girdi, hedef):
    logitler = model(girdi)
    return nn.functional.cross_entropy(logitler.reshape(-1, logitler.shape[-1]), hedef.reshape(-1))


@torch.no_grad()
def kayip_olc(model, veri, tekrar=20, batch=32):
    """Kaybı tek batch yerine birkaç batch'in ortalamasıyla ölçer; daha az gürültülü olur."""
    model.eval()
    kayiplar = [kayip_hesapla(model, *batch_al(veri, batch)).item() for _ in range(tekrar)]
    model.train()
    return sum(kayiplar) / len(kayiplar)


# ---------- Eğitim ve üretim ----------

def egit(model, egitim, dogrulama, adim_sayisi=1500, batch=32, ogrenme_hizi=1e-3, aralik=250):
    optimizer = torch.optim.AdamW(model.parameters(), lr=ogrenme_hizi)
    gecmis = []
    for adim in range(adim_sayisi + 1):
        if adim % aralik == 0:
            gecmis.append((adim, kayip_olc(model, egitim), kayip_olc(model, dogrulama)))
        if adim == adim_sayisi:
            break
        kayip = kayip_hesapla(model, *batch_al(egitim, batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
    return gecmis


@torch.no_grad()
def uret(model, baslangic, stoi, karakterler, uzunluk=120):
    """Her adımda olasılıklara göre bir sonraki karakteri örnekler (6.1'deki gibi)."""
    model.eval()
    idler = torch.tensor([[stoi[k] for k in baslangic]])
    for _ in range(uzunluk):
        logitler = model(idler[:, -BLOK:])[:, -1]
        olasiliklar = torch.softmax(logitler, dim=-1)
        sonraki = torch.multinomial(olasiliklar, 1)
        idler = torch.cat([idler, sonraki], dim=1)
    return "".join(karakterler[i] for i in idler[0].tolist())


def main():
    metin = VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = veri_hazirla(metin)
    print(f"Karakter sayısı: {len(metin)}, sözlük: {len(karakterler)}")
    print(f"Eğitim: {len(egitim)}, doğrulama: {len(dogrulama)}")

    torch.manual_seed(0)
    model = MiniGPT(len(karakterler))
    print("Parametre sayısı:", sum(p.numel() for p in model.parameters()))
    print(f"Rastgele tahminin kaybı: ln({len(karakterler)}) = {math.log(len(karakterler)):.2f}")

    for adim, e, d in egit(model, egitim, dogrulama):
        print(f"Adım {adim:4}: eğitim kaybı {e:.2f}, doğrulama kaybı {d:.2f}")

    torch.manual_seed(1)
    print("Üretilen metin:")
    print(uret(model, "ali ", stoi, karakterler))


if __name__ == "__main__":
    main()
