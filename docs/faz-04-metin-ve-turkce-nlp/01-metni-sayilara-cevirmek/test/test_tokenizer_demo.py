import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kod"))

from tokenizer_demo import (  # noqa: E402
    ORNEK_SOZLUK,
    acgozlu_altkelime,
    karakter_tokenizer,
    kelime_tokenizer,
    turkce_kucuk_harf,
    unicode_normallestir,
    utf8_bayt_sayisi,
)


class TokenizerTesti(unittest.TestCase):
    def test_karakter(self):
        self.assertEqual(karakter_tokenizer("saç"), ["s", "a", "ç"])

    def test_kelime(self):
        self.assertEqual(kelime_tokenizer("bu bir deneme"), ["bu", "bir", "deneme"])

    def test_utf8_bayt(self):
        self.assertEqual(utf8_bayt_sayisi("sac"), 3)
        self.assertEqual(utf8_bayt_sayisi("saç"), 4)  # ç iki bayt
        self.assertEqual(utf8_bayt_sayisi("Türkçe"), 8)  # ü ve ç ikişer bayt

    def test_turkce_kucuk_harf(self):
        self.assertEqual(turkce_kucuk_harf("ISPARTA"), "ısparta")
        self.assertEqual(turkce_kucuk_harf("İSTANBUL"), "istanbul")
        # Python'un varsayılan davranışı Türkçe için yanlış:
        self.assertNotEqual("ISPARTA".lower(), "ısparta")
        self.assertNotEqual("İSTANBUL".lower(), "istanbul")

    def test_unicode_normallestirme(self):
        tek, iki_parca = "ü", "u\u0308"
        self.assertNotEqual(tek, iki_parca)  # ekranda aynı, bilgisayarda farklı
        self.assertEqual(unicode_normallestir(iki_parca), tek)
        self.assertEqual(unicode_normallestir(tek), tek)  # zaten NFC ise değişmez

    def test_altkelime(self):
        self.assertEqual(
            acgozlu_altkelime("evlerimizden", ORNEK_SOZLUK),
            ["ev", "ler", "imiz", "den"],
        )
        self.assertEqual(
            acgozlu_altkelime("kitaplarımızdan", ORNEK_SOZLUK),
            ["kitap", "lar", "ımız", "dan"],
        )

    def test_bilinmeyen_karakter(self):
        sonuc = acgozlu_altkelime("evx", ORNEK_SOZLUK)
        self.assertEqual(sonuc, ["ev", "[BİLİNMEYEN]"])

    def test_sozluk_disi_kelime(self):
        # "okuldan": 'okul' sözlükte yok, o,k,u,l bilinmeyen; 'dan' bulunur
        sonuc = acgozlu_altkelime("okuldan", ORNEK_SOZLUK)
        self.assertEqual(sonuc, ["[BİLİNMEYEN]"] * 4 + ["dan"])

    def test_sozluge_okul_eklenince(self):
        sonuc = acgozlu_altkelime("okuldan", ORNEK_SOZLUK | {"okul"})
        self.assertEqual(sonuc, ["okul", "dan"])

    def test_acgozlu_her_zaman_en_iyi_degil(self):
        # "a" + "bcd" kusursuz bir bölme olurdu, ama açgözlü yöntem önce
        # en uzun eşleşmeyi ("ab") alıyor ve geri dönemiyor.
        sozluk = {"a", "ab", "bcd"}
        self.assertEqual(
            acgozlu_altkelime("abcd", sozluk),
            ["ab", "[BİLİNMEYEN]", "[BİLİNMEYEN]"],
        )


if __name__ == "__main__":
    unittest.main()
