from ctfpilot.core.config import get_groq_key, save_groq_key
from ctfpilot.core.logger import info, warning, highlight, console

def prompt_for_groq_key() -> str | None:
    from rich.panel import Panel
    from rich.prompt import Prompt

    console.print(Panel(
        "[bold cyan]CTFPilot AI Suggestions[/bold cyan]\n\n"
        "Esta funcion requiere una API key de Groq (gratuita).\n\n"
        "[bold]Como obtenerla:[/bold]\n"
        "  1. Ve a [link=https://console.groq.com]console.groq.com[/link]\n"
        "  2. Crea una cuenta gratuita\n"
        "  3. Ve a API Keys y genera una nueva\n"
        "  4. Pégala aqui\n\n"
        "[dim]Presiona Ctrl+C para omitir esta funcion[/dim]",
        title="🤖 IA requerida",
        border_style="cyan"
    ))

    try:
        key = Prompt.ask("\n[cyan]Introduce tu Groq API key[/cyan]")
        if key.strip():
            save_groq_key(key.strip())
            info("API key guardada en ~/.ctfpilot/config.env")
            return key.strip()
    except KeyboardInterrupt:
        warning("Funcion de IA omitida. Puedes activarla mas tarde con 'ctfpilot ai-setup'")
        return None

def get_ai_suggestions(target: str, open_ports: list) -> list:
    key = get_groq_key()
    if not key:
        key = prompt_for_groq_key()
    if not key:
        return []

    try:
        from groq import Groq
        client = Groq(api_key=key)

        ports_info = "\n".join([
            f"- Puerto {p['port']}/{p['proto']}: {p['service']} {p['version']}"
            for p in open_ports
        ])

        prompt = f"""Eres un experto en pentesting y CTFs de HackTheBox.
Analiza estos puertos abiertos en el target {target}:

{ports_info}

Da sugerencias concretas y especificas de:
1. Vectores de ataque mas probables
2. Herramientas especificas a usar con los comandos exactos
3. CVEs o vulnerabilidades conocidas para estas versiones
4. Orden recomendado de ataque

Se conciso, practico y orientado a CTF. Maximo 10 sugerencias."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        result = response.choices[0].message.content
        return [result]

    except KeyboardInterrupt:
        warning("Sugerencias de IA omitidas.")
        return []
    except Exception as e:
        warning(f"Error con la API de Groq: {e}")
        return []