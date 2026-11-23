(function () {
  "use strict";

  var lessonPage = /\/faz-[^/]+\//.test(window.location.pathname);
  if (!lessonPage) return;

  var menu;
  var activeSelection = null;
  var palette = [
    { name: "Sarı", value: "#d8c878" },
    { name: "Yeşil", value: "#91b39b" },
    { name: "Mavi", value: "#86a5c7" },
    { name: "Pembe", value: "#c49aab" }
  ];

  function lessonArticle() {
    return document.querySelector(".md-content article .md-typeset") ||
      document.querySelector(".md-content__inner .md-typeset");
  }

  function storageKey() {
    return "ders-vurgular:" + window.location.pathname;
  }

  function loadMarks() {
    try {
      return JSON.parse(localStorage.getItem(storageKey()) || "[]");
    } catch (_) {
      return [];
    }
  }

  function saveMarks(marks) {
    localStorage.setItem(storageKey(), JSON.stringify(marks));
  }

  function createMenu() {
    menu = document.createElement("div");
    menu.className = "lesson-highlight-menu";
    menu.setAttribute("role", "toolbar");
    menu.setAttribute("aria-label", "Metin vurgusu");

    palette.forEach(function (color) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "lesson-highlight-color";
      button.style.setProperty("--highlight-color", color.value);
      button.title = color.name + " ile vurgula";
      button.setAttribute("aria-label", color.name + " ile vurgula");
      button.dataset.color = color.value;
      menu.appendChild(button);
    });

    var clear = document.createElement("button");
    clear.type = "button";
    clear.className = "lesson-highlight-clear";
    clear.textContent = "×";
    clear.title = "Bu dersin tüm vurgularını temizle";
    clear.setAttribute("aria-label", "Tüm vurguları temizle");
    menu.appendChild(clear);

    document.body.appendChild(menu);

    menu.addEventListener("mousedown", function (event) {
      event.preventDefault();
      event.stopPropagation();
    });
  }

  function pointByOffset(article, offset) {
    var remaining = offset;
    var walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT);
    var node;

    while ((node = walker.nextNode())) {
      if (remaining <= node.data.length) {
        return { node: node, offset: remaining };
      }
      remaining -= node.data.length;
    }

    var last = article.lastChild;
    while (last && last.lastChild) last = last.lastChild;
    return { node: last, offset: last ? last.data.length : 0 };
  }

  function offsetOfRange(article, range) {
    var before = document.createRange();
    before.selectNodeContents(article);
    before.setEnd(range.startContainer, range.startOffset);
    var start = before.toString().length;
    before.setEnd(range.endContainer, range.endOffset);
    return { start: start, end: before.toString().length };
  }

  function wrapRange(article, start, end, color) {
    var startPoint = pointByOffset(article, start);
    var endPoint = pointByOffset(article, end);
    var range = document.createRange();
    range.setStart(startPoint.node, startPoint.offset);
    range.setEnd(endPoint.node, endPoint.offset);
    if (range.collapsed) return;

    var mark = document.createElement("mark");
    mark.className = "lesson-highlight";
    mark.dataset.color = color;
    mark.style.setProperty("--highlight-color", color);

    try {
      range.surroundContents(mark);
    } catch (_) {
      var fragment = range.extractContents();
      mark.appendChild(fragment);
      range.insertNode(mark);
    }
  }

  function restoreMarks() {
    var article = lessonArticle();
    if (!article) return;
    document.querySelectorAll(".lesson-highlight").forEach(function (mark) {
      mark.replaceWith(mark.textContent);
    });

    loadMarks().slice().sort(function (a, b) {
      return b.start - a.start;
    }).forEach(function (mark) {
      wrapRange(article, mark.start, mark.end, mark.color);
    });
  }

  function showMenu(rect) {
    if (!menu) createMenu();
    menu.classList.add("visible");
    var left = Math.max(8, Math.min(rect.left + rect.width / 2, window.innerWidth - 150));
    var top = rect.top - 48;
    if (top < 8) top = rect.bottom + 8;
    menu.style.left = left + "px";
    menu.style.top = top + "px";
  }

  function hideMenu() {
    if (menu) menu.classList.remove("visible");
  }

  function onMouseUp(event) {
    if (menu && menu.contains(event.target)) return;

    var article = lessonArticle();
    if (!article) return;

    var selection = window.getSelection();
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed) {
      hideMenu();
      return;
    }

    var range = selection.getRangeAt(0);
    if (!article.contains(range.startContainer) || !article.contains(range.endContainer)) {
      hideMenu();
      return;
    }

    var text = range.toString().trim();
    if (!text) {
      hideMenu();
      return;
    }

    activeSelection = offsetOfRange(article, range);
    showMenu(range.getBoundingClientRect());
  }

  document.addEventListener("mouseup", onMouseUp);
  document.addEventListener("touchend", onMouseUp);

  document.addEventListener("mousedown", function (event) {
    if (menu && !menu.contains(event.target)) hideMenu();
  });

  document.addEventListener("click", function (event) {
    if (!menu) return;

    var colorButton = event.target.closest(".lesson-highlight-color");
    if (colorButton && activeSelection) {
      var marks = loadMarks();
      marks.push({
        start: activeSelection.start,
        end: activeSelection.end,
        color: colorButton.dataset.color
      });
      saveMarks(marks);
      window.getSelection().removeAllRanges();
      document.querySelectorAll(".lesson-highlight").forEach(function (mark) {
        mark.replaceWith(mark.textContent);
      });
      restoreMarks();
      hideMenu();
      return;
    }

    if (event.target.closest(".lesson-highlight-clear")) {
      saveMarks([]);
      document.querySelectorAll(".lesson-highlight").forEach(function (mark) {
        mark.replaceWith(mark.textContent);
      });
      window.getSelection().removeAllRanges();
      hideMenu();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      window.getSelection().removeAllRanges();
      hideMenu();
    }
  });

  window.addEventListener("load", restoreMarks);
  document.addEventListener("DOMContentLoaded", restoreMarks);
})();
