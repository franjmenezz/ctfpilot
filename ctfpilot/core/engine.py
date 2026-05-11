from ctfpilot.core.logger import info, success, warning, highlight

def run_recon(target: str, session_id: int):
    info("Iniciando escaneo de puertos...")

    from ctfpilot.modules.recon.portscan import scan_ports
    results = scan_ports(target)

    if not results:
        warning("No se encontraron puertos abiertos o Nmap no esta instalado.")
        return

    from ctfpilot.modules.suggest.advisor import get_suggestions
    suggestions = get_suggestions(results)

    if suggestions:
        highlight("Vectores de ataque sugeridos:")
        for s in suggestions:
            highlight(f"  {s}")

    from ctfpilot.modules.suggest.ai_advisor import get_ai_suggestions
    ai_suggestions = get_ai_suggestions(target, results)

    if ai_suggestions:
        highlight("\n Analisis IA:")
        for s in ai_suggestions:
            highlight(s)