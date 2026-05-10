import typer
from typing import Optional
from ctfpilot.core.logger import banner, info, success, warning, error
from ctfpilot.core.session import (
    create_session, get_active_session, add_note, add_flag
)

app = typer.Typer(
    help="CTFPilot — Your co-pilot for CTFs and HackTheBox machines",
    no_args_is_help=True
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        banner()

@app.command()
def start(
    target: str = typer.Option(..., "--target", "-t", help="IP o dominio del objetivo"),
    name: str = typer.Option(..., "--name", "-n", help="Nombre de la máquina"),
    platform: str = typer.Option("htb", "--platform", "-p", 
                                  help="Plataforma: htb, thm, ctf, other")
):
    """Inicia una nueva sesión de pentesting."""
    banner()
    info(f"Iniciando sesión: [bold]{name}[/bold]")
    info(f"Target: [bold]{target}[/bold]")
    info(f"Plataforma: [bold]{platform.upper()}[/bold]")

    session_id = create_session(name, target, platform)
    success(f"Sesión creada con ID: {session_id}")
    info("Lanzando reconocimiento automático...")

    from ctfpilot.core.engine import run_recon
    run_recon(target, session_id)

@app.command()
def note(
    content: str = typer.Argument(..., help="Texto de la nota")
):
    """Añade una nota a la sesión activa."""
    session = get_active_session()
    if not session:
        error("No hay sesión activa. Usa 'ctfpilot start' primero.")
        raise typer.Exit()
    add_note(session["id"], content)
    success(f"Nota guardada en sesión: {session['name']}")

@app.command()
def flag(
    value: str = typer.Option(..., "--value", "-v", help="Valor de la flag"),
    flag_type: str = typer.Option("user", "--type", "-t", help="Tipo: user, root")
):
    """Registra una flag capturada."""
    session = get_active_session()
    if not session:
        error("No hay sesión activa. Usa 'ctfpilot start' primero.")
        raise typer.Exit()
    add_flag(session["id"], flag_type, value)
    success(f"Flag [{flag_type.upper()}] registrada en sesión: {session['name']}")

@app.command()
def status():
    """Muestra el estado de la sesión activa."""
    session = get_active_session()
    if not session:
        warning("No hay ninguna sesión activa.")
        raise typer.Exit()
    from rich.table import Table
    from ctfpilot.core.logger import console
    table = Table(title="Sesión Activa")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="white")
    table.add_row("ID", str(session["id"]))
    table.add_row("Nombre", session["name"])
    table.add_row("Target", session["target"])
    table.add_row("Plataforma", session["platform"].upper())
    table.add_row("Iniciada", session["started_at"])
    console.print(table)

if __name__ == "__main__":
    app()