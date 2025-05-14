import os
import subprocess
import time
import sys
import argparse
import json
import signal
import platform
import tempfile
import shutil
from groq import Groq
from colorama import init, Fore, Style
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
import keyboard  # For cross-platform keyboard interrupt handling

# Initialize colorama for cross-platform console colors
init(autoreset=True, strip=False)

# Initialize rich console
console = Console(stderr=True, style="bold red")

# Define config path (cross-platform)
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".code_solver_config.json")

# Supported languages and their execution commands
LANGUAGES = {
    "python": {
        "ext": ".py",
        "run": "python {file}" if platform.system() == "Windows" else "python3 {file}"
    },
    "javascript": {
        "ext": ".js",
        "run": "node {file}"
    },
    "java": {
        "ext": ".java",
        "run": "javac {file} && java {class_name}",
        "class_name": lambda code: code.split("class ")[1].split()[0] if "class " in code else "Main"
    },
    "cpp": {
        "ext": ".cpp",
        "run": "g++ {file} -o temp && temp.exe" if platform.system() == "Windows" else "g++ {file} -o temp && ./temp"
    },
}

# Global variables for command execution state
current_process = None
is_command_running = False
was_interrupted = False

# Cross-platform keyboard interrupt handler
def handle_interrupt():
    global current_process, is_command_running, was_interrupted
    if is_command_running and current_process:
        current_process.terminate()
        try:
            current_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            current_process.kill()
        console.print("\n[bold yellow]Code execution stopped by user! 🛑[/]")
        was_interrupted = True
    else:
        console.print("\n[bold cyan]Exiting... 👋[/]")
        sys.exit(0)

# Register keyboard interrupt handler
keyboard.on_press_key("ctrl+c", lambda e: handle_interrupt())

# Typewriter animation
def typewriter_print(text, delay=0.03):
    if isinstance(text, str):
        text = Text(text)
    for char in str(text):
        styled_char = Text(char, style=text.style)
        console.print(styled_char, end='', soft_wrap=True)
        sys.stdout.flush()
        time.sleep(delay)
    console.print()

# Display animated logo
def display_logo():
    f = Figlet(font='slant')
    logo = f.renderText("Code Solver")
    color_styles = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    for i, line in enumerate(logo.splitlines()):
        styled_line = Text(line, style=f"bold {color_styles[i % len(color_styles)]}")
        console.print(styled_line)
        time.sleep(0.2)
    typewriter_print(Text("AI Code Problem Solver 🔥 Powered by AKM Korishee Apurbo ☠️", style="bold cyan"))

def load_api_key():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            return config.get("api_key")
    return None

def save_api_key(api_key):
    config = {"api_key": api_key}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)
    console.print(f"[bold green]API key saved to 👉 {CONFIG_PATH}! 👈[/]")

def validate_api_key(api_key):
    try:
        client = Groq(api_key=api_key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Test"}],
            max_tokens=1
        )
        return True
    except Exception:
        return False

def check_language_support(language):
    """Check if the language's runtime is available."""
    try:
        if language == "python":
            subprocess.run(["python" if platform.system() == "Windows" else "python3", "--version"], check=True, capture_output=True)
        elif language == "javascript":
            subprocess.run(["node", "--version"], check=True, capture_output=True)
        elif language == "java":
            subprocess.run(["javac", "--version"], check=True, capture_output=True)
        elif language == "cpp":
            subprocess.run(["g++", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def detect_language(code):
    """Detect programming language based on code patterns."""
    code = code.lower()
    if "def " in code or "import " in code:
        return "python"
    elif "function " in code or "console.log" in code:
        return "javascript"
    elif "public class " in code or "public static void main" in code:
        return "java"
    elif "#include" in code or "int main(" in code:
        return "cpp"
    return None

def run_code_in_background(language, code):
    global current_process, is_command_running, was_interrupted
    temp_dir = tempfile.mkdtemp()
    try:
        if not check_language_support(language):
            return None, f"Runtime for {language} is not installed or not found 😞"

        is_command_running = True
        was_interrupted = False
        lang_config = LANGUAGES.get(language)
        if not lang_config:
            return None, f"Unsupported language: {language} 😞"

        file_ext = lang_config["ext"]
        file_path = os.path.join(temp_dir, f"temp{file_ext}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        command = lang_config["run"].format(
            file=file_path,
            class_name=lang_config.get("class_name", lambda x: "Main")(code) if "class_name" in lang_config else ""
        )

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=temp_dir
        )
        current_process = process

        rotators = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
        spinners = ['⠦', '⠧', '⠇', '⠏', '⠋', '⠙', '⠹', '⠸']
        step = 0

        with Progress(
            TextColumn("{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            transient=True
        ) as progress:
            task = progress.add_task(
                description=Text(f"[bright_red] {spinners[step % len(spinners)]} Running {language} code {rotators[step % len(rotators)]}"),
                total=None
            )

            while process.poll() is None:
                step += 1
                progress.update(
                    task,
                    description=Text(f"[bright_red] {spinners[step % len(spinners)]} Running {language} code {rotators[step % len(rotators)]}")
                )
                time.sleep(0.1)

            elapsed_time = progress.tasks[task].elapsed
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f"{minutes}:{seconds:02d}"
            progress.update(
                task,
                description=Text(f"[bold green]🔥 Completed {language} code {time_str}", style="#c20693"),
                completed=True
            )
            time.sleep(2)

        stdout, stderr = process.communicate()
        current_process = None
        is_command_running = False

        if was_interrupted:
            return None, "Code execution was interrupted by user."
        elif process.returncode == 0:
            return stdout.strip() if stdout else "Code executed successfully! ☠️", None
        else:
            error_msg = stderr.strip() or "Code execution failed with no specific error output."
            return None, error_msg
    except Exception as e:
        return None, f"Unexpected error running code: {str(e)} 😵"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def analyze_and_fix_error(client, language, code, error):
    system_prompt = (
        "You are 'Korishee,' an expert AI coding assistant. "
        "Given a programming language, code, and error message, analyze the issue and suggest a fix. "
        "Respond with ONLY these two elements:\n"
        "1. 'ANALYSIS: <detailed analysis of the error>'\n"
        "2. 'FIX_SUGGESTION: <suggested fix or corrected code>' (use a concrete code snippet if possible)\n"
        "Keep it concise, actionable, and engaging! 😎"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Language: {language}\nCode: {code}\nError: {error}"}
    ]
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ANALYSIS: Couldn’t analyze due to AI error: {str(e)}\nFIX_SUGGESTION: Please try again later or check manually! 😞"

def get_groq_response(client, user_input, chat_history=None):
    if chat_history is None:
        chat_history = []

    system_prompt = (
        "You are 'Korishee,' an expert AI coding assistant created by AKM Korishee Apurbo. "
        "Assist the user interactively to solve coding problems or write code in any programming language. "
        "For code-related requests, respond with ONLY these three elements:\n"
        "1. 'CODE: <complete code snippet>' (no backticks, avoid placeholders unless input is incomplete)\n"
        "2. 'EXPLANATION: <brief explanation>'\n"
        "3. 'QUESTION: <question>' with emojis 🤔 (omit if no further input needed)\n"
        "For other inputs:\n"
        "- If vague (e.g., 'hi'), respond with a greeting and 'QUESTION: <question>'\n"
        "- If asked for your name, say 'I’m Korishee, your coding sidekick! 🔥'\n"
        "- If asked for your creator, say 'I was crafted by the awesome AKM Korishee Apurbo! 🚀'\n"
        "Keep it fun, concise, and engaging! 😎"
    )

    messages = [{"role": "system", "content": system_prompt}] + chat_history + [{"role": "user", "content": user_input}]
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[bold red]Oops! AI Error: {str(e)} 😢[/]")
        return "Sorry, I hit a snag with the AI service! Try again later. 😞"

def main():
    parser = argparse.ArgumentParser(description="Code Solver: AI-powered coding assistant")
    parser.add_argument("--api", type=str, help="Set the Groq API key (overrides config file if provided)")
    args = parser.parse_args()

    api_key = args.api if args.api else load_api_key()
    if not api_key:
        console.print("[bold red]No API key found! 😱 Please provide it via --api <key> to save it to config.[/]")
        api_key = input("Enter your Groq API key: ").strip()
        if validate_api_key(api_key):
            save_api_key(api_key)
        else:
            console.print("[bold red]Invalid API key! 😞 Exiting...[/]")
            sys.exit(1)
    elif not validate_api_key(api_key):
        console.print("[bold red]Stored API key is invalid! 😞 Please provide a new one via --api <key>.[/]")
        sys.exit(1)

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        console.print(f"[bold red]Failed to initialize Groq client: {str(e)} 😱[/]")
        sys.exit(1)

    display_logo()
    typewriter_print(Text("Welcome to Code Solver! 🎉 Type 'exit' or use Ctrl+C to quit. 🚪", style="bold green"))

    chat_history = []
    pending_code = None
    pending_language = None

    while True:
        try:
            user_input = input(f"{Fore.YELLOW}{Style.BRIGHT}You 👤: {Style.RESET_ALL}")
        except KeyboardInterrupt:
            console.print("\n[bold cyan]Exiting... 👋[/]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[bold red]Input error: {str(e)}. Falling back to basic input.[/]")
            user_input = input(f"{Fore.YELLOW}{Style.BRIGHT}You 👤: {Style.RESET_ALL}")

        if user_input.lower() == "exit":
            typewriter_print(Text("Goodbye! 👋 Catch you later! 😄", style="bold cyan"))
            break

        if pending_code:
            code = pending_code.replace("<input>", user_input)
            typewriter_print(Text(f"Korishee 🤖: CODE: {code} ⚡", style="bold magenta"))
            result, error = run_code_in_background(pending_language, code)
            if result:
                console.print(Panel(
                    result,
                    title="Result 🌟",
                    border_style="bold green_yellow",
                    padding=(1, 2),
                    expand=False
                ))
            elif error and not was_interrupted:
                typewriter_print(Text(f"Error 🚨: {error}", style="bold red"))
                fix_response = analyze_and_fix_error(client, pending_language, code, error)
                lines = fix_response.split("\n")
                for line in lines:
                    if line.startswith("ANALYSIS:"):
                        typewriter_print(Text(f"Analysis 🔍: {line.replace('ANALYSIS: ', '')}", style="bold yellow"))
                    elif line.startswith("FIX_SUGGESTION:"):
                        typewriter_print(Text(f"Fix Suggestion 💡: {line.replace('FIX_SUGGESTION: ', '')}", style="bold green"))
            elif was_interrupted:
                typewriter_print(Text("Skipping error analysis. 😊", style="bold yellow"))
            pending_code = None
            pending_language = None
            continue

        chat_history.append({"role": "user", "content": user_input})
        ai_response = get_groq_response(client, user_input, chat_history)

        code = None
        language = None
        question_present = False
        response_text = ""
        lines = ai_response.split("\n")
        for line in lines:
            if line.startswith("CODE:"):
                code = line.replace("CODE: ", "").strip()
                language = detect_language(code) or "python"  # Default to python if detection fails
                typewriter_print(Text(f"Korishee 🤖: CODE: {code} ⚡", style="bold magenta"))
            elif line.startswith("EXPLANATION:"):
                typewriter_print(Text(f"Explanation 📚: {line.replace('EXPLANATION: ', '')}", style="cyan"))
            elif line.startswith("QUESTION:"):
                question_present = True
                response_text = line.replace("QUESTION: ", "").strip()
            else:
                response_text += line + "\n"

        if response_text and not question_present:
            typewriter_print(Text(f"Korishee 🤖: {response_text.strip()} 💬", style="bold magenta"))

        if question_present:
            typewriter_print(Text(f"Korishee asks ❓: {response_text}", style="bold green"))

        if code and "<" not in code and ">" not in code:
            result, error = run_code_in_background(language, code)
            if result:
                console.print(Panel(
                    result,
                    title="Result 🌟",
                    border_style="bold green_yellow",
                    padding=(1, 2),
                    expand=False
                ))
            elif error and not was_interrupted:
                typewriter_print(Text(f"Error 🚨: {error}", style="bold red"))
                fix_response = analyze_and_fix_error(client, language, code, error)
                lines = fix_response.split("\n")
                for line in lines:
                    if line.startswith("ANALYSIS:"):
                        typewriter_print(Text(f"Analysis 🔍: {line.replace('ANALYSIS: ', '')}", style="bold yellow"))
                    elif line.startswith("FIX_SUGGESTION:"):
                        typewriter_print(Text(f"Fix Suggestion 💡: {line.replace('FIX_SUGGESTION: ', '')}", style="bold green"))
            elif was_interrupted:
                typewriter_print(Text("Code execution stopped, skipping error analysis. 😊", style="bold yellow"))
        elif code:
            pending_code = code
            pending_language = language

        chat_history.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()
