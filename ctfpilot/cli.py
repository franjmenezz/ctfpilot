import typer
from ctfpilot.core.logger import banner, info, success, warning, error
from ctfpilot.core.session import (
    create_session, get_active_session, add_note, add_flag
)

app = typer.Typer(
    help="CTFPilot - Your co-pilot for CTFs and HackTheBox machines",
    no_args_is_help=True
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        banner()

@app.command()
def start(
    target: str = typer.Option(..., "--target", "-t", help="IP o dominio del objetivo"),
    name: str = typer.Option(..., "--name", "-n", help="Nombre de la maquina"),
    platform: str = typer.Option(None, "--platform", "-p", help="Plataforma: htb, thm, ctf, other")
):
    """Inicia una nueva sesion de pentesting."""
    banner()
    from ctfpilot.core.session import detect_platform
    if platform is None:
        platform = detect_platform(target)
        info(f"Plataforma detectada automaticamente: [bold]{platform.upper()}[/bold]")
    info(f"Iniciando sesion: [bold]{name}[/bold]")
    info(f"Target: [bold]{target}[/bold]")
    info(f"Plataforma: [bold]{platform.upper()}[/bold]")
    session_id = create_session(name, target, platform)
    success(f"Sesion creada con ID: {session_id}")
    info("Lanzando reconocimiento automatico...")
    from ctfpilot.core.engine import run_recon
    run_recon(target, session_id)

@app.command()
def note(
    content: str = typer.Argument(..., help="Texto de la nota")
):
    """Anade una nota a la sesion activa."""
    session = get_active_session()
    if not session:
        error("No hay sesion activa. Usa 'ctfpilot start' primero.")
        raise typer.Exit()
    add_note(session["id"], content)
    success(f"Nota guardada en sesion: {session['name']}")

@app.command()
def flag(
    value: str = typer.Option(..., "--value", "-v", help="Valor de la flag"),
    flag_type: str = typer.Option("user", "--type", "-t", help="Tipo: user, root")
):
    """Registra una flag capturada."""
    session = get_active_session()
    if not session:
        error("No hay sesion activa. Usa 'ctfpilot start' primero.")
        raise typer.Exit()
    add_flag(session["id"], flag_type, value)
    success(f"Flag [{flag_type.upper()}] registrada en sesion: {session['name']}")

@app.command()
def status():
    """Muestra el estado de la sesion activa."""
    session = get_active_session()
    if not session:
        warning("No hay ninguna sesion activa.")
        raise typer.Exit()
    from rich.table import Table
    from ctfpilot.core.logger import console
    table = Table(title="Sesion Activa")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="white")
    table.add_row("ID", str(session["id"]))
    table.add_row("Nombre", session["name"])
    table.add_row("Target", session["target"])
    table.add_row("Plataforma", session["platform"].upper())
    table.add_row("Iniciada", session["started_at"])
    console.print(table)

@app.command()
def report(
    fmt: str = typer.Option("html", "--format", "-f", help="Formato: html, pdf")
):
    """Genera el reporte de la sesion activa."""
    session = get_active_session()
    if not session:
        error("No hay sesion activa.")
        raise typer.Exit()
    from ctfpilot.modules.report.builder import generate_report
    info(f"Generando reporte en formato {fmt.upper()}...")
    path = generate_report(session["id"], fmt)
    success(f"Reporte guardado en: {path}")

@app.command()
def finish():
    """Finaliza la sesion activa."""
    session = get_active_session()
    if not session:
        error("No hay sesion activa.")
        raise typer.Exit()
    from ctfpilot.core.session import finish_session
    finish_session(session["id"])
    success(f"Sesion [bold]{session['name']}[/bold] finalizada.")

@app.command()
def history():
    """Muestra el historial de todas las sesiones."""
    from ctfpilot.core.session import get_all_sessions
    from rich.table import Table
    from ctfpilot.core.logger import console
    sessions = get_all_sessions()
    if not sessions:
        warning("No hay sesiones registradas.")
        raise typer.Exit()
    table = Table(title="Historial de Sesiones")
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Nombre", style="white")
    table.add_column("Target", style="yellow")
    table.add_column("Plataforma", style="magenta")
    table.add_column("Estado", style="green")
    table.add_column("Inicio", style="dim")
    for s in sessions:
        estado = "activa" if s[6] == "active" else "finalizada"
        table.add_row(str(s[0]), s[1], s[2], s[3].upper(), estado, s[4][:16])
    console.print(table)

if __name__ == "__main__":
    app()