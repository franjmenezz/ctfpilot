from ctfpilot.core.logger import info, success, warning, highlight

def run_recon(target: str, session_id: int):
    info("Iniciando escaneo de puertos...")
    
    from ctfpilot.modules.recon.portscan import scan_ports
    results = scan_ports(target)
    
    if not results:
        warning("No se encontraron puertos abiertos o Nmap no está instalado.")
        return

    from ctfpilot.modules.suggest.advisor import get_suggestions
    suggestions = get_suggestions(results)

    if suggestions:
        highlight("Vectores de ataque sugeridos:")
        for s in suggestions:
            highlight(f"  {s}")