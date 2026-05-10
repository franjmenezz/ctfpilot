SUGGESTIONS = {
    21:  "FTP detectado → Prueba acceso anónimo: ftp {target}",
    22:  "SSH detectado → Prueba fuerza bruta: hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{target}",
    23:  "Telnet detectado → Protocolo inseguro, prueba credenciales por defecto",
    25:  "SMTP detectado → Enumera usuarios: smtp-user-enum -M VRFY -U users.txt -t {target}",
    53:  "DNS detectado → Prueba transferencia de zona: dig axfr @{target}",
    80:  "HTTP detectado → Enumera directorios: gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt",
    443: "HTTPS detectado → Revisa certificado SSL y enumera: gobuster dir -u https://{target} -w /usr/share/wordlists/dirb/common.txt",
    445: "SMB detectado → Enumera shares: smbclient -L //{target} -N",
    3306: "MySQL detectado → Prueba credenciales por defecto: mysql -h {target} -u root -p",
    3389: "RDP detectado → Prueba credenciales: xfreerdp /v:{target} /u:administrator",
    8080: "HTTP alternativo → Puede ser panel admin, enumera: gobuster dir -u http://{target}:8080 -w /usr/share/wordlists/dirb/common.txt",
}

def get_suggestions(open_ports: list) -> list:
    suggestions = []
    for port_info in open_ports:
        port = port_info["port"]
        if port in SUGGESTIONS:
            suggestions.append(SUGGESTIONS[port])
    return suggestions