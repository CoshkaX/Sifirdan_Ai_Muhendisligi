(function () {
  if (location.pathname.indexOf("/faz-") === -1) return;

  var colors = [
    ["Sarı", "#d8c878"],
    ["Yeşil", "#91b39b"],
    ["Mavi", "#86a5c7"],
    ["Pembe", "#c49aab"]
  ];
  var menu = null;
  var notesButton = null;
  var notesPanel = null;
  var notesCurrentButton = null;
  var notesAllButton = null;
  var notesList = null;
  var notesStatus = null;
  var notesTab = "current";
  var pending = null;
  var overlays = [];
  var pendingRange = null;
  var storageErrors = {};
  var blockedStorage = {};
  var storagePrefix = "ders-vurgular:";

  function article() {
    return document.querySelector(".md-content article .md-typeset") ||
      document.querySelector("article.md-content__inner .md-typeset") ||
      document.querySelector(".md-typeset");
  }

  function renderHint() {
    var root = article();
    if (!root || document.querySelector(".lesson-highlight-hint")) return;

    var hint = document.createElement("p");
    hint.className = "lesson-highlight-hint";
    hint.setAttribute("role", "note");
    hint.textContent = "Metni seç; açılan araç çubuğundan bir renk seçerek vurgula veya Not ile açıklama ekle. Vurgular bu tarayıcıda saklanır.";
    root.parentNode.insertBefore(hint, root);
  }

  function initialize() {
    renderHint();
    ensureNotesUi();
    renderOverlays();
    renderNotes();
  }

  function key(path) {
    return storagePrefix + (path || location.pathname);
  }

  function isValidItem(item) {
    return item &&
      typeof item.id === "string" &&
      Number.isInteger(item.start) &&
      Number.isInteger(item.end) &&
      item.start >= 0 &&
      item.end > item.start &&
      colors.some(function (color) { return color[1] === item.color; }) &&
      typeof item.note === "string" &&
      (item.text === undefined || typeof item.text === "string") &&
      (item.lessonTitle === undefined || typeof item.lessonTitle === "string");
  }

  function colorLabel(color) {
    var match = colors.find(function (item) { return item[1] === color; });
    return match ? match[0] : "belirsiz";
  }

  function newId() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    return String(Date.now()) + "-" + String(Math.random()).slice(2);
  }

  function saved(path) {
    var storageKey = key(path);
    try {
      var raw = localStorage.getItem(storageKey);
      if (!raw) {
        delete storageErrors[storageKey];
        delete blockedStorage[storageKey];
        return [];
      }

      var parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) throw new Error("Kayıt biçimi geçersiz.");
      var items = parsed.filter(isValidItem);
      if (items.length !== parsed.length) {
        storageErrors[storageKey] = "Bazı not kayıtları okunamadı; mevcut veriler korunuyor.";
        blockedStorage[storageKey] = true;
      } else {
        delete storageErrors[storageKey];
        delete blockedStorage[storageKey];
      }
      return items;
    } catch (error) {
      storageErrors[storageKey] = "Notlar okunamadı. Tarayıcı depolamasını kontrol et.";
      blockedStorage[storageKey] = true;
      return [];
    }
  }

  function store(items, path) {
    var storageKey = key(path);
    if (blockedStorage[storageKey]) return false;
    try {
      localStorage.setItem(storageKey, JSON.stringify(items));
      delete storageErrors[storageKey];
      saveError = "";
      renderNotes();
      return true;
    } catch (error) {
      saveError = "Notlar kaydedilemedi. Tarayıcı depolama alanı kullanılamıyor.";
      renderNotes();
      return false;
    }
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

  function rangeForItem(root, item) {
    var start = textPoint(root, item.start);
    var end = textPoint(root, item.end);
    if (!start || !end) return null;
    try {
      var range = document.createRange();
      range.setStart(start.node, start.offset);
      range.setEnd(end.node, end.offset);
      return range;
    } catch (error) {
      return null;
    }
  }

  function ensureMenu() {
    if (menu) return menu;
    menu = document.createElement("div");
    menu.className = "lesson-highlight-menu";
    menu.setAttribute("role", "toolbar");
    menu.setAttribute("aria-label", "Metni vurgula");

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

  function refreshMenuPosition() {
    if (!menu || !menu.classList.contains("visible") || !pendingRange) return;
    var rect = pendingRange.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > innerHeight) {
      hideMenu();
      return;
    }
    showMenu(rect);
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
    textarea.setAttribute("aria-label", "Vurgu için not");
    editor.appendChild(textarea);

    var status = document.createElement("p");
    status.className = "lesson-highlight-note-status";
    status.setAttribute("role", "alert");
    status.hidden = true;
    editor.appendChild(status);

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
      if (blockedStorage[key()]) {
        status.textContent = storageErrors[key()];
        status.hidden = false;
        return;
      }
      var target = items.find(function (entry) { return entry.id === item.id; });
      if (target) {
        target.note = textarea.value.trim();
        if (!target.text) target.text = item.text || "";
        if (!target.lessonTitle) target.lessonTitle = item.lessonTitle || lessonTitle(location.pathname);
      } else {
        items.push({
          id: item.id,
          start: item.start,
          end: item.end,
          color: item.color,
          note: textarea.value.trim(),
          text: item.text || "",
          lessonTitle: item.lessonTitle || lessonTitle(location.pathname)
        });
      }
      if (!store(items)) {
        status.textContent = saveError || storageErrors[key()] || "Not kaydedilemedi.";
        status.hidden = false;
        return;
      }
      var selection = getSelection();
      if (selection) selection.removeAllRanges();
      pending = null;
      pendingRange = null;
      hideMenu();
      hideNoteEditor();
      renderOverlays();
    });

    remove.addEventListener("click", function () {
      var items = saved();
      if (blockedStorage[key()] || !store(items.filter(function (entry) { return entry.id !== item.id; }))) {
        status.textContent = storageErrors[key()] || saveError || "Vurgu silinemedi.";
        status.hidden = false;
        return;
      }
      var selection = getSelection();
      if (selection) selection.removeAllRanges();
      pending = null;
      pendingRange = null;
      hideMenu();
      hideNoteEditor();
      renderOverlays();
    });
  }

  var pendingRect = null;
  var saveError = "";

  function setNotesOpen(open) {
    if (!notesPanel || !notesButton) return;
    notesPanel.hidden = !open;
    notesButton.setAttribute("aria-expanded", String(open));
    if (open) renderNotes();
  }

  function ensureNotesUi() {
    if (notesButton) return;

    notesButton = document.createElement("button");
    notesButton.type = "button";
    notesButton.className = "lesson-notes-button";
    notesButton.textContent = "Notlar";
    notesButton.setAttribute("aria-expanded", "false");
    notesButton.setAttribute("aria-controls", "lesson-notes-panel");
    notesButton.addEventListener("click", function () {
      setNotesOpen(notesPanel.hidden);
    });

    notesPanel = document.createElement("section");
    notesPanel.id = "lesson-notes-panel";
    notesPanel.className = "lesson-notes-panel";
    notesPanel.setAttribute("role", "region");
    notesPanel.setAttribute("aria-label", "Ders notları");
    notesPanel.hidden = true;

    var header = document.createElement("div");
    header.className = "lesson-notes-header";

    var title = document.createElement("h2");
    title.textContent = "Notlarım";
    header.appendChild(title);

    var close = document.createElement("button");
    close.type = "button";
    close.className = "lesson-notes-close";
    close.textContent = "Kapat";
    close.setAttribute("aria-label", "Not panelini kapat");
    close.addEventListener("click", function () {
      setNotesOpen(false);
      notesButton.focus();
    });
    header.appendChild(close);
    notesPanel.appendChild(header);

    var tabs = document.createElement("div");
    tabs.className = "lesson-notes-tabs";
    tabs.setAttribute("role", "group");
    tabs.setAttribute("aria-label", "Not kapsamı");

    notesCurrentButton = document.createElement("button");
    notesCurrentButton.type = "button";
    notesCurrentButton.addEventListener("click", function () {
      notesTab = "current";
      renderNotes();
    });
    tabs.appendChild(notesCurrentButton);

    notesAllButton = document.createElement("button");
    notesAllButton.type = "button";
    notesAllButton.addEventListener("click", function () {
      notesTab = "all";
      renderNotes();
    });
    tabs.appendChild(notesAllButton);
    notesPanel.appendChild(tabs);

    notesStatus = document.createElement("p");
    notesStatus.className = "lesson-notes-status";
    notesStatus.setAttribute("role", "status");
    notesStatus.setAttribute("aria-live", "polite");
    notesPanel.appendChild(notesStatus);

    notesList = document.createElement("div");
    notesList.className = "lesson-notes-list";
    notesPanel.appendChild(notesList);

    document.body.appendChild(notesPanel);
    document.body.appendChild(notesButton);
  }

  function validLessonPath(path) {
    try {
      var url = new URL(path, location.origin);
      if (url.origin !== location.origin || url.pathname.indexOf("/faz-") === -1) return null;
      return url.pathname;
    } catch (error) {
      return null;
    }
  }

  function lessonPaths() {
    var paths = [];
    try {
      for (var index = 0; index < localStorage.length; index += 1) {
        var storageKey = localStorage.key(index);
        if (!storageKey || storageKey.indexOf(storagePrefix) !== 0) continue;
        var path = validLessonPath(storageKey.slice(storagePrefix.length));
        if (path && paths.indexOf(path) === -1) paths.push(path);
      }
      delete storageErrors["*"];
    } catch (error) {
      storageErrors["*"] = "Ders notlarının listesi okunamadı. Tarayıcı depolamasını kontrol et.";
    }
    return paths.sort();
  }

  function noteRecords(path) {
    return saved(path).filter(function (item) {
      return item.note.trim().length > 0;
    }).map(function (item) {
      return { item: item, path: path };
    });
  }

  function allNoteRecords() {
    var records = [];
    lessonPaths().forEach(function (path) {
      records = records.concat(noteRecords(path));
    });
    return records.sort(function (a, b) {
      return a.path === b.path
        ? a.item.start - b.item.start
        : a.path.localeCompare(b.path);
    });
  }

  function lessonTitle(path, item) {
    if (item && item.lessonTitle) return item.lessonTitle;
    if (path === location.pathname) {
      var root = article();
      var heading = root && root.querySelector("h1");
      if (heading) return heading.textContent.trim();
    }
    var parts = path.split("/").filter(Boolean);
    return parts.length ? parts[parts.length - 1].replace(/-/g, " ") : "Ders";
  }

  function noteExcerpt(record) {
    if (record.item.text) return record.item.text;
    if (record.path === location.pathname) {
      var root = article();
      var range = root && rangeForItem(root, record.item);
      if (range) return range.toString().trim();
    }
    return "Seçilen metin eski not kaydında saklanmamış.";
  }

  function addNoteCard(record) {
    var item = record.item;
    var card = document.createElement("article");
    card.className = "lesson-notes-card";

    var header = document.createElement("div");
    header.className = "lesson-notes-card-header";

    var link = document.createElement("a");
    link.href = record.path;
    link.textContent = lessonTitle(record.path, item);
    header.appendChild(link);

    var swatch = document.createElement("span");
    swatch.className = "lesson-notes-swatch";
    swatch.style.backgroundColor = item.color;
    swatch.setAttribute("aria-label", "Vurgu rengi: " + colorLabel(item.color));
    header.appendChild(swatch);
    card.appendChild(header);

    var excerpt = document.createElement("p");
    excerpt.className = "lesson-notes-excerpt";
    excerpt.textContent = "“" + noteExcerpt(record) + "”";
    card.appendChild(excerpt);

    var note = document.createElement("p");
    note.className = "lesson-notes-text";
    note.textContent = item.note;
    card.appendChild(note);

    var remove = document.createElement("button");
    remove.type = "button";
    remove.className = "lesson-notes-delete";
    remove.textContent = "Notu ve vurguyu sil";
    remove.setAttribute("aria-label", "Notu ve vurguyu sil: " + lessonTitle(record.path, item));
    remove.addEventListener("click", function () {
      var items = saved(record.path);
      if (blockedStorage[key(record.path)]) {
        renderNotes();
        return;
      }
      if (store(items.filter(function (entry) { return entry.id !== item.id; }), record.path)) {
        if (record.path === location.pathname) renderOverlays();
        renderNotes();
      }
    });
    card.appendChild(remove);
    notesList.appendChild(card);
  }

  function renderNotes() {
    if (!notesPanel || !notesList) return;

    var current = noteRecords(location.pathname);
    var all = allNoteRecords();
    notesCurrentButton.textContent = "Bu ders (" + current.length + ")";
    notesAllButton.textContent = "Tüm dersler (" + all.length + ")";
    notesCurrentButton.setAttribute("aria-pressed", String(notesTab === "current"));
    notesAllButton.setAttribute("aria-pressed", String(notesTab === "all"));

    var messages = [];
    if (saveError) messages.push(saveError);
    Object.keys(storageErrors).forEach(function (storageKey) {
      if (messages.indexOf(storageErrors[storageKey]) === -1) {
        messages.push(storageErrors[storageKey]);
      }
    });
    notesStatus.textContent = messages.join(" ");
    notesStatus.hidden = messages.length === 0;

    notesList.textContent = "";
    var records = notesTab === "current" ? current : all;
    if (!records.length) {
      var empty = document.createElement("p");
      empty.className = "lesson-notes-empty";
      empty.textContent = notesTab === "current"
        ? "Bu derste henüz notun yok."
        : "Henüz hiçbir derste notun yok.";
      notesList.appendChild(empty);
      return;
    }
    records.forEach(addNoteCard);
  }

  function clearOverlays() {
    overlays.forEach(function (node) { node.remove(); });
    overlays = [];
  }

  function renderOverlays() {
    clearOverlays();
    var root = article();
    if (!root) return;

    var items = saved();
    var changed = false;
    items.forEach(function (item) {
      var range = rangeForItem(root, item);
      if (!range) return;
      if (!item.text) {
        item.text = range.toString().trim();
        changed = true;
      }
      if (!item.lessonTitle) {
        item.lessonTitle = lessonTitle(location.pathname);
        changed = true;
      }
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
          event.preventDefault();
          event.stopPropagation();
          pendingRect = rect;
          openNoteEditor(item);
        });
        document.body.appendChild(overlay);
        overlays.push(overlay);
      });
    });
    if (changed) store(items);
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
    pendingRange = range.cloneRange();
    pending = {
      start: textOffset(root, range.startContainer, range.startOffset),
      end: textOffset(root, range.endContainer, range.endOffset),
      text: text,
      lessonTitle: lessonTitle(location.pathname)
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
      if (blockedStorage[key()]) {
        setNotesOpen(true);
        return;
      }
      items.push({
        id: newId(),
        start: pending.start,
        end: pending.end,
        color: color.dataset.color,
        note: "",
        text: pending.text,
        lessonTitle: pending.lessonTitle
      });
      if (!store(items)) {
        setNotesOpen(true);
        return;
      }
      getSelection().removeAllRanges();
      pending = null;
      pendingRange = null;
      hideMenu();
      renderOverlays();
      return;
    }

    var note = event.target.closest(".lesson-highlight-note");
    if (note && pending) {
      var draft = {
        id: newId(),
        start: pending.start,
        end: pending.end,
        color: "#d8c878",
        note: "",
        text: pending.text,
        lessonTitle: pending.lessonTitle,
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

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && notesPanel && !notesPanel.hidden) {
      setNotesOpen(false);
      notesButton.focus();
    }
  });

  window.addEventListener("scroll", function () {
    renderOverlays();
    refreshMenuPosition();
  }, true);
  window.addEventListener("resize", function () {
    renderOverlays();
    refreshMenuPosition();
  });
  document.addEventListener("DOMContentLoaded", initialize);
  window.addEventListener("load", initialize);
})();
