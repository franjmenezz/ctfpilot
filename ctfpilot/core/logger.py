from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "highlight": "bold magenta",
})

console = Console(theme=theme)

def info(msg: str):
    console.print(f"[info][*][/info] {msg}")

def success(msg: str):
    console.print(f"[success][✓][/success] {msg}")

def warning(msg: str):
    console.print(f"[warning][!][/warning] {msg}")

def error(msg: str):
    console.print(f"[error][✗][/error] {msg}")

def highlight(msg: str):
    console.print(f"[highlight][💡][/highlight] {msg}")

def banner():
    console.print("""
[bold cyan]
 ██████╗████████╗███████╗██████╗ ██╗██╗      ██████╗ ████████╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝
██║        ██║   █████╗  ██████╔╝██║██║     ██║   ██║   ██║   
██║        ██║   ██╔══╝  ██╔═══╝ ██║██║     ██║   ██║   ██║   
╚██████╗   ██║   ██║     ██║     ██║███████╗╚██████╔╝   ██║   
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝   
[/bold cyan]
[dim]Your co-pilot for CTFs and HackTheBox machines[/dim]
    """)