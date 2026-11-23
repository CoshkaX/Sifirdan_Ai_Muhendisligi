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
  var overlays = [];

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
      button.setAttribute("aria-label", item[0] + " ile vurgula");
      button.addEventListener("mousedown", function (event) {
        event.preventDefault();
        event.stopPropagation();
      });
      menu.appendChild(button);
    });

    var note = document.createElement("button");
    note.type = "button";
    note.className = "lesson-highlight-note";
    note.textContent = "Not";
    note.title = "Seçime not ekle";
    note.addEventListener("mousedown", function (event) {
      event.preventDefault();
      event.stopPropagation();
    });
    menu.appendChild(note);
    document.body.appendChild(menu);
    return menu;
  }

  function showMenu(rect) {
    var menu = ensureMenu();
    menu.classList.add("visible");
    var left = Math.max(105, Math.min(rect.left + rect.width / 2, innerWidth - 105));
    var top = rect.top - 52;
    if (top < 8) top = rect.bottom + 8;
    menu.style.left = left + "px";
    menu.style.top = top + "px";
  }

  function hideMenu() {
    if (menu) menu.classList.remove("visible");
  }

  function hideNoteEditor() {
    var editor = document.querySelector(".lesson-highlight-note-editor");
    if (editor) editor.remove();
  }

  function openNoteEditor(item) {
    hideNoteEditor();
    var editor = document.createElement("div");
    editor.className = "lesson-highlight-note-editor";

    var title = document.createElement("div");
    title.className = "lesson-highlight-note-title";
    title.textContent = "Vurguya not";
    editor.appendChild(title);

    var textarea = document.createElement("textarea");
    textarea.value = item.note || "";
    textarea.placeholder = "Notunu buraya yaz...";
    editor.appendChild(textarea);

    var actions = document.createElement("div");
    actions.className = "lesson-highlight-note-actions";

    var remove = document.createElement("button");
    remove.type = "button";
    remove.className = "lesson-highlight-delete";
    remove.textContent = "Bu vurguyu sil";

    var save = document.createElement("button");
    save.type = "button";
    save.className = "lesson-highlight-save";
    save.textContent = "Kaydet";

    actions.appendChild(remove);
    actions.appendChild(save);
    editor.appendChild(actions);
    document.body.appendChild(editor);

    var rect = pendingRect || item.rect;
    var left = rect ? Math.max(8, Math.min(rect.left + rect.width / 2, innerWidth - 260)) : 20;
    var top = rect ? rect.bottom + 8 : 100;
    if (top + 210 > innerHeight) top = Math.max(8, rect.top - 210);
    editor.style.left = left + "px";
    editor.style.top = top + "px";
    textarea.focus();

    save.addEventListener("click", function () {
      var items = saved();
      var target = items.find(function (entry) { return entry.id === item.id; });
      if (target) {
        target.note = textarea.value.trim();
        store(items);
      }
      hideNoteEditor();
      renderOverlays();
    });

    remove.addEventListener("click", function () {
      store(saved().filter(function (entry) { return entry.id !== item.id; }));
      hideNoteEditor();
      renderOverlays();
    });
  }

  var pendingRect = null;

  function clearOverlays() {
    overlays.forEach(function (node) { node.remove(); });
    overlays = [];
  }

  function renderOverlays() {
    clearOverlays();
    var root = article();
    if (!root) return;

    saved().forEach(function (item) {
      var start = textPoint(root, item.start);
      var end = textPoint(root, item.end);
      if (!start || !end) return;

      var range = document.createRange();
      range.setStart(start.node, start.offset);
      range.setEnd(end.node, end.offset);
      var rects = range.getClientRects();

      Array.prototype.forEach.call(rects, function (rect) {
        if (rect.width < 2 || rect.height < 2) return;
        var lineRect = rect;
        var top = lineRect.top + window.scrollY;
        var height = Math.min(lineRect.height, 24);
        var left = lineRect.left + window.scrollX;
        var width = lineRect.width;
        var overlay = document.createElement("div");
        overlay.className = "lesson-highlight-overlay";
        overlay.dataset.id = item.id;
        overlay.style.setProperty("--highlight-color", item.color);
        overlay.style.left = left + "px";
        overlay.style.top = top + "px";
        overlay.style.width = width + "px";
        overlay.style.height = height + "px";
        overlay.title = item.note ? "Not: " + item.note : "Vurguyu aç";
        overlay.addEventListener("click", function (event) {
          event.preventEvent = true;
          event.stopPropagation();
          pendingRect = rect;
          openNoteEditor(item);
        });
        document.body.appendChild(overlay);
        overlays.push(overlay);
      });
    });
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

    pendingRect = range.getBoundingClientRect();
    pending = {
      start: textOffset(root, range.startContainer, range.startOffset),
      end: textOffset(root, range.endContainer, range.endOffset)
    };
    showMenu(pendingRect);
  }

  document.addEventListener("mouseup", selectionChanged);
  document.addEventListener("keyup", function (event) {
    if (event.shiftKey) selectionChanged();
  });

  document.addEventListener("click", function (event) {
    var color = event.target.closest(".lesson-highlight-color");
    if (color && pending) {
      var items = saved();
      items.push({
        id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()),
        start: pending.start,
        end: pending.end,
        color: color.dataset.color,
        note: ""
      });
      store(items);
      getSelection().removeAllRanges();
      pending = null;
      hideMenu();
      renderOverlays();
      return;
    }

    var note = event.target.closest(".lesson-highlight-note");
    if (note && pending) {
      var draft = {
        id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()),
        start: pending.start,
        end: pending.end,
        color: "#d8c878",
        note: "",
        rect: pendingRect
      };
      openNoteEditor(draft);
      hideMenu();
    }
  });

  document.addEventListener("mousedown", function (event) {
    if (menu && !menu.contains(event.target) &&
        !event.target.closest(".lesson-highlight-note-editor")) {
      hideMenu();
    }
  });

  window.addEventListener("scroll", renderOverlays, true);
  window.addEventListener("resize", renderOverlays);
  document.addEventListener("DOMContentLoaded", renderOverlays);
  window.addEventListener("load", renderOverlays);
})();
