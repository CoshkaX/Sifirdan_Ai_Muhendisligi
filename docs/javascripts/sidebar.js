document$.subscribe(function () {
  var plannedLinks = document.querySelectorAll(
    '.md-sidebar--primary .md-nav__link[href*="MUFREDAT"]'
  );

  plannedLinks.forEach(function (link) {
    link.removeAttribute("href");
    link.setAttribute("aria-disabled", "true");
    link.style.pointerEvents = "none";
  });

  document.querySelectorAll(".md-sidebar--primary .md-nav__toggle").forEach(function (toggle) {
    toggle.checked = true;
  });
});
