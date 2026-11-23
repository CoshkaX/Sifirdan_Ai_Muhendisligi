(function () {
  if (location.pathname.indexOf("/faz-") === -1) return;

  var colors = [
    ["Sarı", "#d8c878"],
    ["Yeşil", "#91b39b"],
    ["Mavi", "#86a5c7"],
    ["Pembe", "#c49aab"]
  ];
  var menu = null;
  var pending = null;

  function article() {
    return document.querySelector(".md-content article .md-typeset") ||
      document.querySelector("article.md-content__inner .md-typeset") ||
      document.querySelector(".md-typeset");
  }

  function key() {
    return "ders-vurgular:" + location.pathname;
  }

  function saved() {
    try {
      return JSON.parse(localStorage.getItem(key()) || "[]");
    } catch (_) {
      return [];
    }
  }

  function store(items) {
    localStorage.setItem(key(), JSON.stringify(items));
  }

  function ensureMenu() {
    if (menu) return menu;
    menu = document.createElement("div");
    menu.className = "lesson-highlight-menu";
    colors.forEach(function (item) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "lesson-highlight-color";
      button.dataset.color = item[1];
      button.style.setProperty("--highlight-color", item[1]);
      button.title = item[0];
      button.addEventListener("mousedown", function (event) {
        event.preventDefault();
        event.stopPropagation();
      });
      menu.appendChild(button);
    });

    var clear = document.createElement("button");
    clear.type = "button";
    clear.className = "lesson-highlight-clear";
    clear.textContent = "×";
    clear.title = "Tüm vurguları temizle";
    clear.addEventListener("mousedown", function (event) {
      event.preventDefault();
      event.stopPropagation();
    });
    menu.appendChild(clear);
    document.body.appendChild(menu);
    return menu;
  }

  function textOffset(root, container, offset) {
    var range = document.createRange();
    range.selectNodeContents(root);
    range.setEnd(container, offset);
    return range.toString().length;
  }

  function textPoint(root, offset) {
    var left = offset;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      if (left <= node.nodeValue.length) {
        return { node: node, offset: left };
      }
      left -= node.nodeValue.length;
    }
    return null;
  }

  function applyRange(item) {
    var root = article();
    var start = textPoint(root, item.start);
    var end = textPoint(root, item.end);
    if (!start || !end) return;

    var range = document.createRange();
    range.setStart(start.node, start.offset);
    range.setEnd(end.node, end.offset);
    if (range.collapsed) return;

    var mark = document.createElement("mark");
    mark.className = "lesson-highlight";
    mark.dataset.color = item.color;
    mark.style.setProperty("--highlight-color", item.color);

    try {
      range.surroundContents(mark);
    } catch (_) {
      var fragment = range.extractContents();
      mark.appendChild(fragment);
      range.insertNode(mark);
    }
  }

  function restore() {
    var root = article();
    if (!root) return;
    root.querySelectorAll("mark.lesson-highlight").forEach(function (mark) {
      mark.replaceWith(document.createTextNode(mark.textContent));
    });
    saved().forEach(applyRange);
  }

  function showMenu(rect) {
    var menu = ensureMenu();
    menu.classList.add("visible");
    var left = Math.max(82, Math.min(rect.left + rect.width / 2, innerWidth - 82));
    var top = rect.top - 50;
    if (top < 8) top = rect.bottom + 8;
    menu.style.left = left + "px";
    menu.style.top = top + "px";
  }

  function hideMenu() {
    if (menu) menu.classList.remove("visible");
  }

  function selectionChanged() {
    var root = article();
    var selection = getSelection();
    if (!root || !selection || selection.isCollapsed || selection.rangeCount === 0) {
      hideMenu();
      return;
    }

    var range = selection.getRangeAt(0);
    var text = selection.toString().trim();
    if (!text || !root.contains(range.startContainer) || !root.contains(range.endContainer)) {
      hideMenu();
      return;
    }

    pending = {
      start: textOffset(root, range.startContainer, range.startOffset),
      end: textOffset(root, range.endContainer, range.endOffset)
    };
    showMenu(range.getBoundingClientRect());
  }

  document.addEventListener("mouseup", selectionChanged);
  document.addEventListener("keyup", function (event) {
    if (event.shiftKey) selectionChanged();
  });

  document.addEventListener("click", function (event) {
    var color = event.target.closest(".lesson-highlight-color");
    if (color && pending) {
      var items = saved();
      items.push({ start: pending.start, end: pending.end, color: color.dataset.color });
      store(items);
      getSelection().removeAllRanges();
      pending = null;
      restore();
      hideMenu();
      return;
    }

    if (event.target.closest(".lesson-highlight-clear")) {
      store([]);
      restore();
      pending = null;
      getSelection().removeAllRanges();
      hideMenu();
    }
  });

  document.addEventListener("mousedown", function (event) {
    if (menu && !menu.contains(event.target)) hideMenu();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      getSelection().removeAllRanges();
      hideMenu();
    }
  });

  document.addEventListener("DOMContentLoaded", restore);
  window.addEventListener("load", restore);
})();
