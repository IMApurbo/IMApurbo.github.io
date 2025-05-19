<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Banlang Terminal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-dark.min.css" rel="stylesheet" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <style>
    body {
      background: #000;
      color: #00ff00;
      font-family: 'Courier New', Courier, monospace;
    }
    #terminal, #codeEditor {
      background: #000;
      border: 1px solid #00ff00;
      color: #00ff00;
      caret-color: #00ff00;
      tab-size: 4;
      padding: 10px;
      resize: none;
      font-family: 'Courier New', Courier, monospace;
      outline: none;
    }
    #terminal {
      height: 400px;
      overflow-y: auto;
      white-space: pre-wrap;
    }
    .syntax-section {
      background: #111;
      border: 1px solid #00ff00;
      padding: 1rem;
    }
    #codeEditor {
      width: 100%;
      height: 300px;
    }
    #compilerOutput {
      background: #000;
      border: 1px solid #00ff00;
      color: #00ff00;
      height: 200px;
      overflow-y: auto;
      padding: 10px;
    }
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 60px;
      height: 34px;
    }
    .toggle-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #555;
      transition: .4s;
      border-radius: 34px;
    }
    .slider:before {
      position: absolute;
      content: "";
      height: 26px;
      width: 26px;
      left: 4px;
      bottom: 4px;
      background-color: #00ff00;
      transition: .4s;
      border-radius: 50%;
    }
    input:checked + .slider {
      background-color: #00ff00;
    }
    input:checked + .slider:before {
      transform: translateX(26px);
      background-color: #000;
    }
    .output-success::before {
      content: "✅ Sofol hoyecho 🎉";
    }
    .output-error::before {
      content: "❌ Sofol hoyni, Kothao vul ache\n";
    }
    .language-banlang .token.keyword {
      color: #ff0000;
    }
    .language-banlang .token.string {
      color: #00ffff;
    }
    .language-banlang .token.number {
      color: #ff00ff;
    }
    .language-banlang .token.operator {
      color: #fff;
    }
    .language-banlang .token.punctuation {
      color: #00ff00;
    }
    .language-banlang .token.variable {
      color: #ffff00;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col">
  <header class="bg-black text-green-500 p-4 border-b border-green-500">
    <h1 class="text-2xl font-bold">Banlang Terminal</h1>
    <p class="text-sm">Bengali-inspired coding in a hacker's terminal</p>
  </header>
  <main class="flex-grow flex flex-col gap-4 p-4">
    <div class="flex items-center gap-4 syntax-section">
      <h2 class="text-lg font-semibold">Mode:</h2>
      <label class="toggle-switch">
        <input type="checkbox" id="modeToggle">
        <span class="slider"></span>
      </label>
      <span id="modeLabel">Interpreter</span>
    </div>

    <div class="flex flex-col lg:flex-row gap-4">
      <div class="w-full lg:w-1/2 flex flex-col gap-4">
        <!-- Interpreter -->
        <div id="interpreterMode" class="syntax-section">
          <h2 class="text-lg font-semibold mb-2">Interpreter</h2>
          <div id="terminal" contenteditable="true">1 >>> </div>
        </div>

        <!-- Compiler -->
        <div id="compilerMode" class="syntax-section hidden">
          <h2 class="text-lg font-semibold mb-2">Code Editor</h2>
          <textarea id="codeEditor">shuru koro
dhoro a = 15;
dhoro b = 10;
jodi (a > b) {
    dekhao "a is greater than b";
} ta na hole {
    dekhao "a is not greater than b";
}
sesh koro</textarea>
          <button id="compileButton" class="mt-2 bg-green-500 text-black px-4 py-2 rounded hover:bg-green-600">
            Compile & Run
          </button>
        </div>

        <!-- Syntax -->
        <div class="syntax-section">
          <h2 class="text-lg font-semibold mb-2">Banlang Syntax</h2>
          <ul class="list-disc ml-6 text-sm">
            <li><strong>Variables:</strong> <code>dhoro name = value;</code></li>
            <li><strong>Output:</strong> <code>dekhao expression;</code></li>
            <li><strong>Conditionals:</strong> <code>jodi (condition) {...} othoba {...} ta na hole {...}</code></li>
            <li><strong>Loops:</strong> <code>jotokkhon na (condition) {...}</code>, <code>thamo;</code></li>
            <li><strong>Start/End:</strong> <code>shuru koro</code>, <code>sesh koro</code></li>
          </ul>
        </div>
      </div>

      <div class="w-full lg:w-1/2">
        <div id="compilerOutputSection" class="syntax-section hidden">
          <h2 class="text-lg font-semibold mb-2">Output</h2>
          <pre id="compilerOutput" class="language-banlang"></pre>
        </div>
      </div>
    </div>

    <div class="syntax-section mt-4">
      <h2 class="text-lg font-semibold mb-2">Examples</h2>
      <pre><code class="language-banlang">shuru koro
dhoro name = "Ami";
dekhao name;
sesh koro</code></pre>

      <pre><code class="language-banlang">shuru koro
dhoro x = 5;
jotokkhon na (x == 0) {
  dekhao x;
  dhoro x = x - 1;
}
sesh koro</code></pre>
    </div>
  </main>

  <script>
    // Define Prism.js language for Banlang
    Prism.languages.banlang = {
      'keyword': /\b(shuru koro|sesh koro|dhoro|dekhao|jodi|othoba|ta na hole|jotokkhon na|thamo)\b/,
      'string': /"[^"]*"/,
      'number': /\b\d+\b/,
      'operator': /[+\-*/=<>!]=?|\+\+|--/,
      'punctuation': /[;{}()]/,
      'variable': /[a-zA-Z_][a-zA-Z0-9_]*/
    };

    const modeToggle = document.getElementById('modeToggle');
    const modeLabel = document.getElementById('modeLabel');
    const interpreterMode = document.getElementById('interpreterMode');
    const compilerMode = document.getElementById('compilerMode');
    const compilerOutputSection = document.getElementById('compilerOutputSection');
    const codeEditor = document.getElementById('codeEditor');
    const compilerOutput = document.getElementById('compilerOutput');
    const terminal = document.getElementById('terminal');

    // Banlang to JavaScript transpiler
    function transpileBanlang(code, isFullProgram = true) {
      try {
        let jsCode = code
          .replace(/dhoro\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=/g, 'let $1 =')
          .replace(/dekhao\s+(.+);/g, 'console.log($1);')
          .replace(/jodi\s*\((.+)\)\s*{/g, 'if ($1) {')
          .replace(/othoba\s*\((.+)\)\s*{/g, 'else if ($1) {')
          .replace(/ta na hole\s*{/g, 'else {')
          .replace(/jotokkhon na\s*\((.+)\)\s*{/g, 'while ($1) {')
          .replace(/thamo;/g, 'break;')
          .replace(/\+=/g, '+=');

        if (isFullProgram) {
          jsCode = jsCode
            .replace(/shuru koro/g, '(function() {')
            .replace(/sesh koro/g, '})();');
          if (!code.includes('shuru koro') || !code.includes('sesh koro')) {
            throw new Error('Code must start with "shuru koro" and end with "sesh koro"');
          }
        } else if (code.includes('shuru koro') || code.includes('sesh koro')) {
          jsCode = jsCode
            .replace(/shuru koro/g, '')
            .replace(/sesh koro/g, '');
        }

        return jsCode;
      } catch (error) {
        throw new Error(`Details: ${error.message}`);
      }
    }

    // Custom console.log to capture output
    let outputLog = [];
    const originalConsoleLog = console.log;
    console.log = function (...args) {
      outputLog.push(args.join(' '));
      originalConsoleLog.apply(console, args);
    };

    // Interpreter handling
    let lineCount = 1;
    let history = [];
    let historyIndex = -1;

    terminal.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const content = terminal.textContent.trim();
        const command = content.split('\n').pop().replace(/^\d+\s>>> /, '');
        if (command) {
          outputLog = [];
          history.push(command);
          historyIndex = history.length;
          try {
            const jsCode = transpileBanlang(command, false);
            eval(jsCode);
            const outputText = outputLog.length > 0 ? outputLog.join('\n') : '';
            terminal.innerHTML = terminal.innerHTML.replace(/<br\s*\/?>\s*$/, '');
            terminal.innerHTML += `<div class="output-success"></div><div>${outputText}</div><div><span class="line-number">${++lineCount} >>> </span></div>`;
          } catch (error) {
            terminal.innerHTML = terminal.innerHTML.replace(/<br\s*\/?>\s*$/, '');
            terminal.innerHTML += `<div class="output-error">Details: ${error.message}</div><div><span class="line-number">${++lineCount} >>> </span></div>`;
          }
          terminal.scrollTop = terminal.scrollHeight;
        } else {
          terminal.innerHTML = terminal.innerHTML.replace(/<br\s*\/?>\s*$/, '');
          terminal.innerHTML += `<div><span class="line-number">${++lineCount} >>> </span></div>`;
          terminal.scrollTop = terminal.scrollHeight;
        }
      } else if (e.key === 'ArrowUp') {
        if (historyIndex > 0) {
          historyIndex--;
          const lines = terminal.innerHTML.split('\n');
          lines[lines.length - 1] = `<span class="line-number">${lineCount} >>> </span>${history[historyIndex] || ''}`;
          terminal.innerHTML = lines.join('\n');
        }
      } else if (e.key === 'ArrowDown') {
        if (historyIndex < history.length - 1) {
          historyIndex++;
          const lines = terminal.innerHTML.split('\n');
          lines[lines.length - 1] = `<span class="line-number">${lineCount} >>> </span>${history[historyIndex] || ''}`;
          terminal.innerHTML = lines.join('\n');
        } else {
          const lines = terminal.innerHTML.split('\n');
          lines[lines.length - 1] = `<span class="line-number">${lineCount} >>> </span>`;
          terminal.innerHTML = lines.join('\n');
          historyIndex = history.length;
        }
      }
    });

    // Compiler handling
    document.getElementById('compileButton').addEventListener('click', () => {
      const code = codeEditor.value;
      const outputElement = document.getElementById('compilerOutput');
      outputLog = [];

      try {
        const jsCode = transpileBanlang(code);
        eval(jsCode);
        outputElement.className = 'language-banlang output-success';
        outputElement.textContent = outputLog.join('\n');
      } catch (error) {
        outputElement.className = 'language-banlang output-error';
        outputElement.textContent = `Details: ${error.message}`;
      }
    });

    // Mode toggle
    modeToggle.addEventListener('change', () => {
      if (modeToggle.checked) {
        modeLabel.textContent = 'Compiler';
        interpreterMode.classList.add('hidden');
        compilerMode.classList.remove('hidden');
        compilerOutputSection.classList.remove('hidden');
      } else {
        modeLabel.textContent = 'Interpreter';
        interpreterMode.classList.remove('hidden');
        compilerMode.classList.add('hidden');
        compilerOutputSection.classList.add('hidden');
      }
    });
  </script>
</body>
</html>
