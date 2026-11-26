"""Derslerdeki etkileşimli örneklerin ve görevlerin doğruluğunu denetler.

Ek paket gerektirmez. Proje klasöründe çalıştır:

    python scripts/ornekleri_dogrula.py

Denetlenenler:
- Örnek kutuları ({.python-playground}): kod çalışıyor ve çıktısı beklenen çıktıyla aynı mı?
- Kendin yaz görevleri ({.python-playground-task}):
    * İskelette en az bir ___ boşluğu var mı?
    * Çözüm bloğunda ___ ya da TODO kalmamış mı?
    * Çözüm çalışıyor ve çıktısı beklenen çıktıyla aynı mı?
"""

import re
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

ORNEK = re.compile(
    r"```python \{\.python-playground\}\n(.*?)```\n"
    r"```text \{\.python-playground-expected\}\n(.*?)```",
    re.S,
)
GOREV = re.compile(
    r"```python \{\.python-playground-task\}\n(.*?)```\n"
    r"```text \{\.python-playground-expected\}\n(.*?)```\n"
    r"```text \{\.python-playground-help\}\n.*?```\n"
    r"```python \{\.python-playground-solution\}\n(.*?)```",
    re.S,
)


def calistir(kod):
    sonuc = subprocess.run(
        [sys.executable, "-I", "-c", kod],
        capture_output=True, text=True, timeout=30,
    )
    return sonuc.returncode, sonuc.stdout.strip(), sonuc.stderr.strip()


def main():
    sorunlar = []
    ornek_sayisi = gorev_sayisi = 0

    for dosya in sorted(DOCS.rglob("*.md")):
        metin = dosya.read_text(encoding="utf-8").replace("\r\n", "\n")
        ad = dosya.parent.name if dosya.name == "README.md" else dosya.name

        for kod, beklenen in ORNEK.findall(metin):
            ornek_sayisi += 1
            kod_no, cikti, hata = calistir(kod)
            if kod_no != 0 or cikti != beklenen.strip():
                sorunlar.append(f"{ad}: örnek beklenen çıktıyı vermiyor. {hata[-200:]}")

        gorevler = GOREV.findall(metin)
        if len(re.findall(r"^```python \{\.python-playground-task\}$", metin, re.M)) != len(gorevler):
            sorunlar.append(f"{ad}: bir görev kutusunun sırası bozuk "
                            "(görev, beklenen çıktı, yardım, çözüm bu sırayla gelmeli)")
        for iskelet, beklenen, cozum in gorevler:
            gorev_sayisi += 1
            if "___" not in iskelet:
                sorunlar.append(f"{ad}: görevin iskeletinde ___ boşluğu yok")
            if "___" in cozum or "TODO" in cozum:
                sorunlar.append(f"{ad}: çözümde ___ ya da TODO kalmış")
            kod_no, cikti, hata = calistir(cozum)
            if kod_no != 0 or cikti != beklenen.strip():
                sorunlar.append(f"{ad}: çözüm beklenen çıktıyı vermiyor. {hata[-200:]}")

    print(f"{ornek_sayisi} örnek, {gorev_sayisi} görev denetlendi.")
    for sorun in sorunlar:
        print("SORUN:", sorun)
    if sorunlar:
        sys.exit(1)
    print("Hepsi doğru.")


if __name__ == "__main__":
    main()
