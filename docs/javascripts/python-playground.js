(function () {
  var runtimeUrl = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
  var nextId = 0;
  var workerSource = [
    "importScripts(" + JSON.stringify(runtimeUrl + "pyodide.js") + ");",
    "var runtimePromise;",
    "self.onmessage = async function (event) {",
    "  if (event.data.type !== 'run') return;",
    "  try {",
    "    if (!runtimePromise) {",
    "      self.postMessage({ type: 'loading' });",
    "      runtimePromise = loadPyodide({ indexURL: " + JSON.stringify(runtimeUrl) + " });",
    "      runtimePromise = runtimePromise.then(function (runtime) {",
    "        runtime.setStdout({ batched: function (text) { self.postMessage({ type: 'stdout', text: text + '\\n' }); } });",
    "        runtime.setStderr({ batched: function (text) { self.postMessage({ type: 'stderr', text: text + '\\n' }); } });",
    "      runtime.runPython([",
    "        'import ast as _lesson_ast',",
    "        'def _lesson_is_literal_print_only(source):',",
    "        '    try:',",
    "        '        tree = _lesson_ast.parse(source)',",
    "        '    except SyntaxError:',",
    "        '        return False',",
    "        '    if not tree.body:',",
    "        '        return False',",
    "        '    def is_constant_text(node):',",
    "        '        if isinstance(node, _lesson_ast.Constant):',",
    "        '            return isinstance(node.value, str)',",
    "        '        if isinstance(node, _lesson_ast.BinOp) and isinstance(node.op, _lesson_ast.Add):',",
    "        '            return is_constant_text(node.left) and is_constant_text(node.right)',",
    "        '        if isinstance(node, _lesson_ast.JoinedStr):',",
    "        '            return all(isinstance(value, _lesson_ast.Constant) and isinstance(value.value, str) for value in node.values)',",
    "        '        return False',",
    "        '    def is_print_expression(node):',",
    "        '        if isinstance(node, _lesson_ast.Tuple):',",
    "        '            return bool(node.elts) and all(is_print_expression(item) for item in node.elts)',",
    "        '        if not isinstance(node, _lesson_ast.Call) or not isinstance(node.func, _lesson_ast.Name) or node.func.id != \"print\":',",
    "        '            return False',",
    "        '        if not node.args or not all(is_constant_text(arg) for arg in node.args):',",
    "        '            return False',",
    "        '        return all(keyword.arg in (\"sep\", \"end\") and is_constant_text(keyword.value) for keyword in node.keywords)',",
    "        '    return all(isinstance(statement, _lesson_ast.Expr) and is_print_expression(statement.value) for statement in tree.body)',",
    "      ].join('\\n'));",
    "        return runtime;",
    "      });",
    "    }",
    "    var runtime = await runtimePromise;",
    "  if (event.data.checkExpected) {",
    "    runtime.globals.set('_lesson_source', event.data.code);",
    "    var validation = runtime.runPython(\"'yes' if _lesson_is_literal_print_only(_lesson_source) else 'no'\");",
    "    var isShortcut = validation && validation.toJs ? validation.toJs() : validation;",
    "    if (validation && validation.destroy) validation.destroy();",
    "    if (isShortcut === 'yes') {",
    "      self.postMessage({ type: 'shortcut', text: 'Bu kod yalnızca sabit metin yazdırıyor. Görevin istediği işlemi kodlamayı dene; adım adım yardım için kodlama yardımcısını aç.' });",
    "      return;",
    "    }",
    "  }",
    "    self.postMessage({ type: 'running' });",
    // Her çalıştırma boş bir ad alanında başlar. Böylece önceki denemede
    // tanımlanan değişkenler sessizce kalmaz; silinen satır gerçekten silinmiş olur.
    "    var namespace = runtime.globals.get('dict')();",
    "    try {",
    "      await runtime.runPythonAsync(event.data.code, { globals: namespace });",
    "    } finally {",
    "      namespace.destroy();",
    "    }",
    "    self.postMessage({ type: 'done' });",
    "  } catch (error) {",
    "    var message = error && error.message ? error.message : String(error);",
    // Pyodide'in kendi iç dosyalarını gösteren satırları atıp yalnızca
    // öğrencinin kodundaki kısmı bırakırız.
    "    var start = message.indexOf('  File \"<exec>\"');",
    "    if (start !== -1) message = 'Traceback (most recent call last):\\n' + message.slice(start);",
    "    self.postMessage({ type: 'error', text: message.replace(/\\n+$/, '') });",
    "  }",
    "};"
  ].join("\n");

  function makeWorker() {
    var blob = new Blob([workerSource], { type: "text/javascript" });
    var url = URL.createObjectURL(blob);
    var worker;
    try {
      worker = new Worker(url);
    } finally {
      URL.revokeObjectURL(url);
    }
    return worker;
  }

  function addPlayground(block) {
    var code = block.querySelector("code");
    if (!code) return;
    // "Kendin yaz" kutuları (.python-playground-task) boşluk doldurmalı görevlerdir;
    // diğerleri "Örnek"tir: çalıştırılır, değiştirilir, ama başarı rozeti verilmez.
    var isTask = block.classList.contains("python-playground-task");

    var nextBlock = block.nextElementSibling;
    var expectedBlock = nextBlock &&
      nextBlock.classList.contains("python-playground-expected")
      ? nextBlock
      : null;
    var expectedCode = expectedBlock ? expectedBlock.querySelector("code") : null;
    var expectedOutput = expectedCode
      ? expectedCode.textContent.replace(/\n$/, "")
      : null;
    var possibleHelpBlock = expectedBlock
      ? expectedBlock.nextElementSibling
      : nextBlock;
    var helpBlock = possibleHelpBlock &&
      possibleHelpBlock.classList.contains("python-playground-help")
      ? possibleHelpBlock
      : null;
    var helpCode = helpBlock ? helpBlock.querySelector("code") : null;
    var helpSteps = helpCode
      ? helpCode.textContent.split(/\r?\n/).map(function (line) {
          return line.trim();
        }).filter(Boolean)
      : [];

    // "Kendin yaz" görevlerinde çözümün tamamı ayrı bir blokta gelir; yardım
    // düğmesine basılınca yeşil kod olarak gösterilir.
    var afterHelp = helpBlock ? helpBlock.nextElementSibling : possibleHelpBlock;
    var solutionBlock = afterHelp &&
      afterHelp.classList.contains("python-playground-solution")
      ? afterHelp
      : null;
    var solutionCode = solutionBlock ? solutionBlock.querySelector("code") : null;
    var solutionText = solutionCode ? solutionCode.textContent.replace(/\n$/, "") : "";

    var widget = document.createElement("section");
    widget.className = "python-playground-widget " +
      (isTask ? "python-playground-widget--task" : "python-playground-widget--example");
    widget.setAttribute("aria-label", "Etkileşimli Python çalışma alanı");

    var kind = document.createElement("p");
    kind.className = "python-playground-kind";
    kind.textContent = isTask ? "Kendin yaz" : "Örnek";
    widget.appendChild(kind);

    var hint = document.createElement("p");
    hint.className = "python-playground-hint";
    hint.textContent = isTask
      ? "Kodun içindeki boş kutulara istenen kodu yaz. Kodun geri kalanı değişmez (# ile başlayan satırlar açıklamadır). Yorumlardaki × işareti Python'da * olarak yazılır. Takılırsan aşağıdaki yardım düğmesine bas."
      : "Önce çalıştır. Sonra koddaki bir sayıyı ya da metni değiştirip tekrar çalıştır ve çıktının nasıl değiştiğine bak.";
    widget.appendChild(hint);

    var label = document.createElement("label");
    label.className = "python-playground-label";
    label.textContent = isTask ? "Boş kutuları doldur ve çalıştır" : "Python kodunu düzenle ve çalıştır";

    var editor = document.createElement("textarea");
    editor.className = "python-playground-editor";
    editor.value = code.textContent.replace(/\n$/, "");
    editor.rows = Math.max(5, Math.min(isTask ? 16 : 10, editor.value.split("\n").length));
    editor.spellcheck = false;
    editor.autocapitalize = "off";
    editor.autocomplete = "off";
    editor.setAttribute("autocorrect", "off");
    editor.setAttribute("aria-label", "Python kodu");
    editor.id = "python-playground-editor-" + (++nextId);
    label.htmlFor = editor.id;
    widget.appendChild(label);

    // "Kendin yaz" görevlerinde kod salt okunurdur; her ___ yazılabilir bir kutuya
    // dönüşür. Öğrenci kodun geri kalanını değiştiremez, yalnızca kutulara yazar.
    var taskSegments = isTask ? editor.value.split("___") : [];
    var useBlanks = taskSegments.length > 1;
    var blanks = [];
    if (useBlanks) {
      var view = document.createElement("div");
      view.className = "python-playground-taskcode";
      view.setAttribute("role", "group");
      view.setAttribute("aria-label", "Tamamlanacak Python kodu");
      taskSegments.forEach(function (segment, index) {
        view.appendChild(document.createTextNode(segment));
        if (index < taskSegments.length - 1) {
          var blank = document.createElement("input");
          blank.type = "text";
          blank.className = "python-playground-blank";
          blank.placeholder = "yaz";
          blank.spellcheck = false;
          blank.autocomplete = "off";
          blank.autocapitalize = "off";
          blank.setAttribute("autocorrect", "off");
          blank.setAttribute("aria-label", "Kutu " + (index + 1) + " / " + (taskSegments.length - 1));
          blank.style.width = "7ch";
          blanks.push(blank);
          view.appendChild(blank);
        }
      });
      label.htmlFor = "";
      widget.appendChild(view);
    } else {
      widget.appendChild(editor);
    }

    function currentCode() {
      if (!useBlanks) return editor.value;
      var assembled = taskSegments[0];
      for (var i = 0; i < blanks.length; i += 1) {
        assembled += blanks[i].value.trim() + taskSegments[i + 1];
      }
      return assembled;
    }

    function setEditable(flag) {
      editor.disabled = !flag;
      blanks.forEach(function (blank) { blank.disabled = !flag; });
    }

    var actions = document.createElement("div");
    actions.className = "python-playground-actions";

    var run = document.createElement("button");
    run.type = "button";
    run.className = "python-playground-run";
    run.textContent = "Çalıştır";
    actions.appendChild(run);

    var shortcut = document.createElement("span");
    shortcut.className = "python-playground-shortcut";
    shortcut.textContent = "Ctrl+Enter";
    actions.appendChild(shortcut);

    var stop = document.createElement("button");
    stop.type = "button";
    stop.className = "python-playground-stop";
    stop.textContent = "Durdur";
    stop.disabled = true;
    stop.hidden = true;
    actions.appendChild(stop);
    widget.appendChild(actions);

    var status = document.createElement("p");
    status.className = "python-playground-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    status.textContent = isTask
      ? "Boşlukları tamamlayıp çalıştır."
      : "Kod tarayıcında çalışır. Çalıştır, sonra bir değeri değiştirip tekrar dene.";
    widget.appendChild(status);

    var outputLabel = document.createElement("p");
    outputLabel.className = "python-playground-output-label";
    outputLabel.textContent = "Çıktı";
    widget.appendChild(outputLabel);

    var output = document.createElement("pre");
    output.className = "python-playground-output";
    output.setAttribute("aria-label", "Python çıktısı");
    output.textContent = "Çıktı burada görünecek.";
    widget.appendChild(output);

    var expectedDetails = null;
    if (expectedOutput !== null) {
      expectedDetails = document.createElement("details");
      expectedDetails.className = "python-playground-expected-details";

      var expectedSummary = document.createElement("summary");
      expectedSummary.textContent = isTask ? "Beklenen çıktıyı gör" : "Başlangıç koduyla çıkan çıktı";
      expectedDetails.appendChild(expectedSummary);

      var expected = document.createElement("pre");
      expected.className = "python-playground-expected-output";
      expected.textContent = expectedOutput;
      expectedDetails.appendChild(expected);
      widget.appendChild(expectedDetails);

      if (isTask) {
        var learningNote = document.createElement("p");
        learningNote.className = "python-playground-learning-note";
        learningNote.textContent = "Beklenen metni doğrudan yazdırma; kodun istenen işlemi yapmasını sağla.";
        widget.appendChild(learningNote);
      }
    }

    if (helpSteps.length) {
      var helpButton = document.createElement("button");
      helpButton.type = "button";
      helpButton.className = "python-playground-help-toggle";
      var helpOpenText = isTask ? "Yapamazsan buna bas" : "Anlamadıysan bas";
      helpButton.textContent = helpOpenText;
      helpButton.setAttribute("aria-expanded", "false");

      var helpPanel = document.createElement("div");
      helpPanel.className = "python-playground-help";
      helpPanel.id = "python-playground-help-" + nextId;
      helpPanel.hidden = true;
      helpButton.setAttribute("aria-controls", helpPanel.id);

      if (isTask && solutionText) {
        var solutionTitle = document.createElement("p");
        solutionTitle.className = "python-playground-solution-title";
        solutionTitle.textContent = "Çözüm · kodun tamamı";
        helpPanel.appendChild(solutionTitle);

        var solutionPre = document.createElement("pre");
        solutionPre.className = "python-playground-solution-code";
        solutionPre.textContent = solutionText;
        helpPanel.appendChild(solutionPre);

        var solutionNote = document.createElement("p");
        solutionNote.className = "python-playground-solution-note";
        solutionNote.textContent = "Önce kendi kodunla karşılaştır; sonra kendi kutuna yaz ve çalıştır. Aşağıda satır satır açıklaması var.";
        helpPanel.appendChild(solutionNote);
      }

      var helpTitle = document.createElement("p");
      helpTitle.className = "python-playground-help-title";
      helpTitle.textContent = "Kodlama yardımcısı · adım adım";
      helpPanel.appendChild(helpTitle);

      var helpList = document.createElement("ol");
      helpSteps.forEach(function (step) {
        var item = document.createElement("li");
        var separator = step.indexOf("|");
        var expression = separator >= 0 ? step.slice(0, separator).trim() : "";
        var explanation = separator >= 0 ? step.slice(separator + 1).trim() : step;

        if (expression) {
          var codeLine = document.createElement("code");
          codeLine.className = "python-playground-help-expression";
          codeLine.textContent = expression.replace(/^`|`$/g, "");
          item.appendChild(codeLine);
        }

        var description = document.createElement("p");
        description.className = "python-playground-help-description";
        explanation.split("`").forEach(function (part, index) {
          if (index % 2 === 1) {
            var inlineCode = document.createElement("code");
            inlineCode.textContent = part;
            description.appendChild(inlineCode);
          } else {
            description.appendChild(document.createTextNode(part));
          }
        });
        item.appendChild(description);
        helpList.appendChild(item);
      });
      helpPanel.appendChild(helpList);
      widget.appendChild(helpButton);
      widget.appendChild(helpPanel);

      helpButton.addEventListener("click", function () {
        var isOpen = !helpPanel.hidden;
        helpPanel.hidden = isOpen;
        helpButton.setAttribute("aria-expanded", String(!isOpen));
        helpButton.textContent = isOpen ? helpOpenText : "İpuçlarını kapat";
      });
    }

    var worker = null;
    var timeout = null;
    var busy = false;
    var hasRun = false;

    function clearTimeoutHandle() {
      if (timeout) {
        window.clearTimeout(timeout);
        timeout = null;
      }
    }

    function setTimeoutHandle(delay, message) {
      clearTimeoutHandle();
      timeout = window.setTimeout(function () {
        if (!busy) return;
        if (worker) worker.terminate();
        worker = null;
        busy = false;
        setEditable(true);
        run.disabled = false;
        stop.disabled = true;
        stop.hidden = true;
        run.textContent = "Çalıştır";
        status.textContent = message;
      }, delay);
    }

    function finish(message, destroyWorker, successful) {
      clearTimeoutHandle();
      busy = false;
      setEditable(true);
      run.disabled = successful === true;
      stop.disabled = true;
      stop.hidden = true;
      status.textContent = message;
      run.textContent = successful ? "✓ Başarılı" : "Çalıştır";
      widget.classList.toggle("python-playground-widget--success", successful === true);
      if (destroyWorker && worker) {
        worker.terminate();
        worker = null;
      }
    }

    function normalizeOutput(text) {
      return text.replace(/\r\n/g, "\n").replace(/\n+$/, "");
    }

    function appendOutput(text) {
      if (output.textContent === "Çıktı burada görünecek.") output.textContent = "";
      output.textContent += text;
      output.scrollTop = output.scrollHeight;
    }

    function getWorker() {
      if (worker) return worker;
      worker = makeWorker();
      worker.addEventListener("message", function (event) {
        if (event.data.type === "loading") {
          status.textContent = "Python ilk kullanım için indiriliyor ve hazırlanıyor...";
        } else if (event.data.type === "running") {
          status.textContent = "Kod çalışıyor...";
          setTimeoutHandle(15000, "Çalışma süresi 15 saniyeyi aştığı için durduruldu.");
        } else if (event.data.type === "stdout" || event.data.type === "stderr") {
          appendOutput(event.data.text);
        } else if (event.data.type === "done") {
          if (!isTask) {
            finish("Çalıştırıldı. Şimdi koddaki bir değeri değiştirip tekrar çalıştır.", false);
          } else if (expectedOutput === null) {
            finish("Çalıştırma tamamlandı.", false);
          } else if (normalizeOutput(output.textContent) === normalizeOutput(expectedOutput)) {
            finish("Beklenen çıktı eşleşti. Harika!", false, true);
          } else {
            if (expectedDetails) expectedDetails.open = true;
            finish("Çıktı henüz eşleşmedi. Kodunu ve beklenen sonucu karşılaştırıp yeniden dene.", false);
          }
        } else if (event.data.type === "shortcut") {
          appendOutput(event.data.text + "\n");
          finish("Çıktıyı doğrudan yazdırmak çözüm sayılmıyor; kodu göreve göre düzenle.", false);
        } else if (event.data.type === "error") {
          appendOutput(event.data.text + "\n");
          finish("Kod çalışırken hata oluştu.", false);
        }
      });
      worker.addEventListener("error", function () {
        appendOutput("Python çalışma zamanı yüklenemedi. İnternet bağlantını kontrol edip yeniden dene.\n");
        finish("Python yüklenemedi veya çalışma alanında bir hata oluştu.", true);
      });
      return worker;
    }

    run.addEventListener("click", function () {
      if (busy) return;
      if (useBlanks) {
        var empty = blanks.filter(function (blank) { return !blank.value.trim(); });
        blanks.forEach(function (blank) {
          blank.classList.toggle("python-playground-blank--empty", !blank.value.trim());
        });
        if (empty.length) {
          status.textContent = "Önce boş kutuları doldur, sonra çalıştır.";
          empty[0].focus();
          return;
        }
      }
      busy = true;
      hasRun = true;
      setEditable(false);
      run.disabled = true;
      run.textContent = "Çalışıyor...";
      stop.disabled = false;
      stop.hidden = false;
      output.textContent = "";
      status.textContent = "Python çalışma alanı başlatılıyor...";
      setTimeoutHandle(60000, "Python yüklemesi zaman aşımına uğradı. Bağlantını kontrol edip yeniden dene.");
      try {
        getWorker().postMessage({
          type: "run",
          code: currentCode(),
          checkExpected: isTask && expectedOutput !== null
        });
      } catch (error) {
        finish("Python çalışma alanı başlatılamadı.", true);
        appendOutput(error.message + "\n");
      }
    });

    function editorChanged() {
      if (!hasRun) return;
      widget.classList.remove("python-playground-widget--success");
      run.disabled = false;
      run.textContent = "Yeniden dene";
      status.textContent = "Kodu değiştirdin. Yeni sonucu görmek için yeniden çalıştır.";
    }

    editor.addEventListener("input", editorChanged);

    blanks.forEach(function (blank) {
      blank.addEventListener("input", function () {
        blank.classList.remove("python-playground-blank--empty");
        blank.style.width = Math.max(7, blank.value.length + 2) + "ch";
        editorChanged();
      });
      blank.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          run.click();
        }
      });
    });

    stop.addEventListener("click", function () {
      if (!busy) return;
      finish("Çalıştırma durduruldu.", true);
    });

    editor.addEventListener("keydown", function (event) {
      if (event.key === "Tab") {
        event.preventDefault();
        var start = editor.selectionStart;
        var end = editor.selectionEnd;
        editor.value = editor.value.slice(0, start) + "    " + editor.value.slice(end);
        editor.selectionStart = editor.selectionEnd = start + 4;
        editorChanged();
      } else if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        run.click();
      }
    });

    if (expectedBlock) expectedBlock.remove();
    if (helpBlock) helpBlock.remove();
    if (solutionBlock) solutionBlock.remove();
    block.replaceWith(widget);
  }

  document.querySelectorAll(".python-playground, .python-playground-task").forEach(addPlayground);
})();
