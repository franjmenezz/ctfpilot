import httpx
from ctfpilot.core.logger import info, success, warning, highlight

def check_cves(service: str, version: str) -> list:
    if not service or not version:
        return []
    try:
        keyword = f"{service} {version}"
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=3"
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            cves = []
            for item in data.get("vulnerabilities", []):
                cve = item.get("cve", {})
                cve_id = cve.get("id", "")
                descriptions = cve.get("descriptions", [])
                desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "")[:100]
                metrics = cve.get("metrics", {})
                score = "N/A"
                if "cvssMetricV31" in metrics:
                    score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
                elif "cvssMetricV2" in metrics:
                    score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
                cves.append({"id": cve_id, "score": score, "desc": desc})
            return cves
    except Exception:
        return []
    return []

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

                        if version:
                            cves = check_cves(service, version)
                            for cve in cves:
                                highlight(f"  CVE: {cve['id']} (Score: {cve['score']}) — {cve['desc']}...")

        return open_ports

    except ImportError:
        warning("python-nmap no esta instalado correctamente.")
        return []
    except Exception as e:
        warning(f"Nmap no disponible o error: {e}")
        warning("Instala Nmap desde https://nmap.org/download.html")
        return []