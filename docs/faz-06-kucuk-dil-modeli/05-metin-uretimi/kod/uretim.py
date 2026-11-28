"""Ders 6.5 – Metin üretimi: açgözlü seçim, sıcaklık, top-k ve top-p.

PyTorch gerekir. Çalıştır:  python kod/uretim.py

6.4'teki mini GPT'yi eğitir, sonra aynı modelden farklı üretim ayarlarıyla metin üretir.
"""

import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "04-mini-gpt-egitimi" / "kod"))
import mini_gpt as mg  # noqa: E402


def sonraki_token(logitler, sicaklik=1.0, top_k=None, top_p=None):
    """Tek bir konumun logitlerinden (1 boyutlu tensör) bir sonraki token'ı seçer.

    sicaklik=0 açgözlü seçimdir: en yüksek puanlı token.
    """
    if sicaklik == 0:
        return int(logitler.argmax())
    logitler = logitler / sicaklik
    if top_k is not None:
        esik = torch.topk(logitler, top_k).values[-1]
        logitler = logitler.masked_fill(logitler < esik, float("-inf"))
    if top_p is not None:
        sirali, sira = torch.sort(logitler, descending=True)
        birikimli = torch.softmax(sirali, dim=-1).cumsum(dim=-1)
        at = birikimli - torch.softmax(sirali, dim=-1) >= top_p  # öncekiler zaten p'yi doldurduysa at
        logitler = logitler.clone()
        logitler[sira[at]] = float("-inf")
    olasiliklar = torch.softmax(logitler, dim=-1)
    return int(torch.multinomial(olasiliklar, 1))


@torch.no_grad()
def uret(model, baslangic, stoi, karakterler, uzunluk=80, **ayarlar):
    model.eval()
    idler = [stoi[k] for k in baslangic]
    for _ in range(uzunluk):
        logitler = model(torch.tensor([idler[-mg.BLOK:]]))[0, -1]
        idler.append(sonraki_token(logitler, **ayarlar))
    return "".join(karakterler[i] for i in idler)


def main():
    metin = mg.VERI_YOLU.read_text(encoding="utf-8")
    karakterler, stoi, egitim, dogrulama = mg.veri_hazirla(metin)
    torch.manual_seed(0)
    model = mg.MiniGPT(len(karakterler))
    mg.egit(model, egitim, dogrulama)

    denemeler = [
        ("açgözlü", dict(sicaklik=0)),
        ("sıcaklık 0.5", dict(sicaklik=0.5)),
        ("sıcaklık 1.0", dict(sicaklik=1.0)),
        ("sıcaklık 2.0", dict(sicaklik=2.0)),
        ("top-k 3", dict(top_k=3)),
        ("top-p 0.8", dict(top_p=0.8)),
    ]
    for ad, ayarlar in denemeler:
        torch.manual_seed(1)
        print(f"{ad}:")
        print("  " + uret(model, "çocuklar ", stoi, karakterler, uzunluk=200, **ayarlar).replace("\n", " "))


if __name__ == "__main__":
    main()
