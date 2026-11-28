"""Ders 6.6 – Küçük Türkçe veriyle deney: model boyutu, dropout ve veri miktarının etkisi.

PyTorch gerekir. Çalıştır:  python kod/deney.py   (birkaç dakika sürer)

6.4'teki mini GPT'yi dört farklı ayarla eğitir. Her 250 adımda doğrulama kaybını ölçer,
en iyi doğrulama kaybını ve o anki modeli saklar (erken durdurma), sonunda sonuç tablosu yazar.
"""

import copy
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "04-mini-gpt-egitimi" / "kod"))
import mini_gpt as mg  # noqa: E402

DENEYLER = [
    # ad, gömme boyutu, dropout, eğitim verisinin kullanılan oranı
    ("temel (D=32, dropout 0.2)", 32, 0.2, 1.0),
    ("dropout yok", 32, 0.0, 1.0),
    ("büyük model (D=64), dropout yok", 64, 0.0, 1.0),
    ("yarım veri", 32, 0.2, 0.5),
]


def model_kur(sozluk_boyutu, d, dropout):
    """mini_gpt'deki ayarları değiştirip yeni bir model kurar."""
    mg.D, mg.DROPOUT = d, dropout
    return mg.MiniGPT(sozluk_boyutu)


def deney_yap(egitim, dogrulama, sozluk_boyutu, d, dropout, oran,
              adim_sayisi=3000, aralik=250, batch=32, ogrenme_hizi=1e-3):
    torch.manual_seed(0)
    model = model_kur(sozluk_boyutu, d, dropout)
    egitim = egitim[: int(len(egitim) * oran)]
    optimizer = torch.optim.AdamW(model.parameters(), lr=ogrenme_hizi)
    gecmis, en_iyi = [], (float("inf"), 0, None)
    for adim in range(adim_sayisi + 1):
        if adim % aralik == 0:
            e, v = mg.kayip_olc(model, egitim), mg.kayip_olc(model, dogrulama)
            gecmis.append((adim, e, v))
            if v < en_iyi[0]:
                en_iyi = (v, adim, copy.deepcopy(model.state_dict()))
        if adim == adim_sayisi:
            break
        kayip = mg.kayip_hesapla(model, *mg.batch_al(egitim, batch))
        optimizer.zero_grad()
        kayip.backward()
        optimizer.step()
    parametre = sum(p.numel() for p in model.parameters())
    return gecmis, en_iyi, parametre


def main():
    metin = mg.VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = mg.veri_hazirla(metin)
    sonuclar = []
    for ad, d, dropout, oran in DENEYLER:
        gecmis, (en_iyi_kayip, en_iyi_adim, _), parametre = deney_yap(
            egitim, dogrulama, len(karakterler), d, dropout, oran)
        print(ad)
        print("  doğrulama kaybı:", " ".join(f"{v:.2f}" for _, _, v in gecmis))
        sonuclar.append((ad, parametre, en_iyi_kayip, en_iyi_adim, gecmis[-1][1], gecmis[-1][2]))

    print()
    print(f"{'deney':33} {'parametre':>9} {'en iyi doğr.':>12} {'adım':>5} {'son eğitim':>10} {'son doğr.':>9}")
    for ad, parametre, en_iyi_kayip, adim, son_e, son_v in sonuclar:
        print(f"{ad:33} {parametre:>9} {en_iyi_kayip:>12.2f} {adim:>5} {son_e:>10.2f} {son_v:>9.2f}")


if __name__ == "__main__":
    main()
