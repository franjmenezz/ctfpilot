from ctfpilot.core.logger import info, success, warning

def scan_ports(target: str) -> list:
    try:
        import nmap
        nm = nmap.PortScanner()
        info(f"Escaneando {target} (esto puede tardar unos segundos)...")
        nm.scan(hosts=target, arguments="-sV -T4 --top-ports 1000")
        
        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    state = nm[host][proto][port]["state"]
                    if state == "open":
                        service = nm[host][proto][port]["name"]
                        version = nm[host][proto][port]["version"]
                        open_ports.append({
                            "port": port,
                            "proto": proto,
                            "service": service,
                            "version": version
                        })
                        success(f"Puerto {port}/{proto} — {service} {version}")
        return open_ports

    except ImportError:
        warning("python-nmap no está instalado correctamente.")
        return []
    except Exception as e:
        warning(f"Nmap no disponible o error: {e}")
        warning("Instala Nmap desde https://nmap.org/download.html")
        return []