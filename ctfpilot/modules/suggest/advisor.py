PORT_SUGGESTIONS = {
    21: [
        "FTP detectado → Prueba acceso anonimo: ftp {target}",
        "Enumera con: nmap -sV -sC -p 21 {target}",
        "Busca credenciales por defecto: anonymous/anonymous",
        "Revisa si permite subida de archivos",
    ],
    22: [
        "SSH detectado → Enumera version: ssh -V",
        "Prueba fuerza bruta: hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{target}",
        "Busca claves privadas expuestas (.ssh/id_rsa)",
        "Prueba usuario por defecto segun el OS detectado",
    ],
    23: [
        "Telnet detectado → Protocolo inseguro sin cifrado",
        "Prueba credenciales por defecto: admin/admin, root/root",
        "Captura trafico con Wireshark (credenciales en claro)",
    ],
    25: [
        "SMTP detectado → Enumera usuarios: smtp-user-enum -M VRFY -U /usr/share/wordlists/metasploit/unix_users.txt -t {target}",
        "Prueba open relay: telnet {target} 25",
        "Busca version vulnerable con: nmap -sV -p 25 {target}",
    ],
    53: [
        "DNS detectado → Prueba transferencia de zona: dig axfr @{target}",
        "Enumera subdominios: dnsenum {target}",
        "Busca registros TXT con info sensible: dig txt {target}",
    ],
    80: [
        "HTTP detectado → Enumera directorios: gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt",
        "Identifica tecnologias: whatweb http://{target}",
        "Busca robots.txt y sitemap.xml",
        "Prueba LFI en parametros: ?page=../../../etc/passwd",
        "Revisa codigo fuente en busca de comentarios y credenciales",
        "Escanea vulnerabilidades web: nikto -h http://{target}",
    ],
    443: [
        "HTTPS detectado → Revisa certificado SSL: openssl s_client -connect {target}:443",
        "Enumera directorios: gobuster dir -u https://{target} -w /usr/share/wordlists/dirb/common.txt",
        "Comprueba versiones SSL debiles: sslscan {target}",
        "Busca subdominios en el certificado (SANs)",
    ],
    445: [
        "SMB detectado → Enumera shares: smbclient -L //{target} -N",
        "Escanea vulnerabilidades: nmap --script smb-vuln* -p 445 {target}",
        "Enumera usuarios: enum4linux -a {target}",
        "Prueba EternalBlue si es Windows antiguo: MS17-010",
        "Revisa permisos de shares: smbmap -H {target}",
    ],
    110: [
        "POP3 detectado → Prueba credenciales por defecto",
        "Telnet para enumerar: telnet {target} 110",
        "USER admin / PASS admin",
    ],
    111: [
        "RPCbind detectado → Enumera servicios RPC: rpcinfo -p {target}",
        "Si NFS esta disponible: showmount -e {target}",
        "Monta shares NFS: mount -t nfs {target}:/ /mnt/nfs",
    ],
    139: [
        "NetBIOS detectado → Enumera con: nbtscan {target}",
        "Usa enum4linux: enum4linux -a {target}",
    ],
    389: [
        "LDAP detectado → Enumera sin credenciales: ldapsearch -x -h {target} -b 'dc=domain,dc=com'",
        "Busca usuarios y grupos en AD",
        "Prueba LDAP injection en formularios web",
    ],
    1433: [
        "MSSQL detectado → Prueba credenciales: sa/sa, sa/(vacio)",
        "Enumera con: nmap -sV -p 1433 --script ms-sql-* {target}",
        "Si tienes credenciales prueba xp_cmdshell para RCE",
    ],
    2049: [
        "NFS detectado → Lista shares: showmount -e {target}",
        "Monta el share: mount -t nfs {target}:/ /mnt/nfs",
        "Busca archivos con permisos incorrectos o claves SSH",
    ],
    3306: [
        "MySQL detectado → Prueba credenciales: mysql -h {target} -u root -p",
        "Credenciales por defecto: root/(vacio), root/root",
        "Si tienes acceso prueba: SELECT ... INTO OUTFILE para escribir webshell",
    ],
    3389: [
        "RDP detectado → Prueba credenciales: xfreerdp /v:{target} /u:administrator",
        "Busca BlueKeep (CVE-2019-0708) si es Windows antiguo",
        "Fuerza bruta: hydra -l administrator -P rockyou.txt rdp://{target}",
    ],
    5985: [
        "WinRM detectado → Prueba con: evil-winrm -i {target} -u usuario -p password",
        "Necesitas credenciales validas del sistema",
        "Muy comun en HTB para movimiento lateral",
    ],
    6379: [
        "Redis detectado → Prueba acceso sin auth: redis-cli -h {target}",
        "Comandos utiles: INFO, KEYS *, CONFIG GET *",
        "Posible escritura de webshell o clave SSH con CONFIG SET",
    ],
    8080: [
        "HTTP alternativo → Puede ser panel de administracion",
        "Enumera: gobuster dir -u http://{target}:8080 -w /usr/share/wordlists/dirb/common.txt",
        "Busca Tomcat manager, Jenkins, o paneles similares",
        "Credenciales Tomcat por defecto: tomcat/tomcat, admin/admin",
    ],
    8443: [
        "HTTPS alternativo → Revisa si hay panel de admin",
        "Puede ser Tomcat HTTPS o panel de administracion",
    ],
    27017: [
        "MongoDB detectado → Prueba acceso sin auth: mongo {target}",
        "Enumera bases de datos: show dbs",
        "Busca credenciales y datos sensibles",
    ],
}

COMBO_SUGGESTIONS = [
    {
        "ports": [80, 443],
        "msg": "Web completa (HTTP+HTTPS) → Busca diferencias entre HTTP y HTTPS, posible redireccion con info extra"
    },
    {
        "ports": [139, 445],
        "msg": "SMB completo → Alta probabilidad de enum4linux exitoso: enum4linux -a {target}"
    },
    {
        "ports": [80, 8080],
        "msg": "Dos puertos web → Compara contenido, el secundario suele tener panel admin"
    },
    {
        "ports": [22, 80],
        "msg": "SSH + Web → Busca credenciales en la web para reutilizar en SSH"
    },
    {
        "ports": [445, 3389],
        "msg": "SMB + RDP → Objetivo Windows, prueba pass-the-hash si consigues hashes NTLM"
    },
    {
        "ports": [80, 3306],
        "msg": "Web + MySQL → Busca SQLi en la web o credenciales de BD en archivos de config"
    },
    {
        "ports": [22, 2049],
        "msg": "SSH + NFS → Monta el NFS y busca claves SSH para acceder directamente"
    },
]

def get_suggestions(open_ports: list) -> list:
    suggestions = []
    port_numbers = [p["port"] for p in open_ports]

    for port_info in open_ports:
        port = port_info["port"]
        target = "{target}"
        if port in PORT_SUGGESTIONS:
            suggestions.append(f"\n  [Puerto {port}]")
            for s in PORT_SUGGESTIONS[port]:
                suggestions.append(f"  → {s}")

    for combo in COMBO_SUGGESTIONS:
        if all(p in port_numbers for p in combo["ports"]):
            suggestions.append(f"\n  [COMBO {'+'.join(map(str, combo['ports']))}]")
            suggestions.append(f"  → {combo['msg']}")

    return suggestions