// Material teması yıldız sayısını tarayıcıda önbelleğe alır ve eski kalabilir.
// Bu betik her sayfa açılışında güncel sayıyı GitHub'dan okuyup gösterir.
(function () {
  var API = "https://api.github.com/repos/CoshkaX/Sifirdan_Ai_Muhendisligi";

  function yaz(sayi) {
    var deneme = 0;
    var zamanlayici = setInterval(function () {
      var alan = document.querySelector(".md-source__fact--stars");
      if (alan) alan.textContent = sayi;
      if (alan || ++deneme > 40) clearInterval(zamanlayici);
    }, 250);
  }

  fetch(API)
    .then(function (yanit) { return yanit.ok ? yanit.json() : null; })
    .then(function (veri) {
      if (veri && typeof veri.stargazers_count === "number") yaz(String(veri.stargazers_count));
    })
    .catch(function () { /* bağlantı yoksa temanın gösterdiği sayı kalır */ });
})();
