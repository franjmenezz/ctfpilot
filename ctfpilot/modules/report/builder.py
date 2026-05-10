import os
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from ctfpilot.core.session import get_session_data

TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; margin: 40px; }
  h1 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 10px; }
  h2 { color: #f0883e; margin-top: 30px; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
  .htb { background: #9fef00; color: #000; }
  .thm { background: #c11111; color: #fff; }
  .ctf { background: #58a6ff; color: #000; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; }
  th { background: #21262d; color: #58a6ff; padding: 10px; text-align: left; }
  td { padding: 8px 10px; border-bottom: 1px solid #21262d; }
  .flag { background: #1f3a1f; border-left: 4px solid #9fef00; padding: 10px; margin: 5px 0; border-radius: 4px; }
  .note { background: #1f2d3d; border-left: 4px solid #58a6ff; padding: 10px; margin: 5px 0; border-radius: 4px; }
  .footer { margin-top: 50px; color: #484f58; font-size: 12px; text-align: center; }
</style>
</head>
<body>
  <h1>🧭 CTFPilot — Reporte de Sesión</h1>

  <h2>📋 Información General</h2>
  <table>
    <tr><th>Campo</th><th>Valor</th></tr>
    <tr><td>Máquina</td><td>{{ session.name }}</td></tr>
    <tr><td>Target</td><td>{{ session.target }}</td></tr>
    <tr><td>Plataforma</td><td><span class="badge {{ session.platform }}">{{ session.platform | upper }}</span></td></tr>
    <tr><td>Inicio</td><td>{{ session.started_at }}</td></tr>
    <tr><td>Reporte generado</td><td>{{ generated_at }}</td></tr>
  </table>

  <h2>🚩 Flags Capturadas</h2>
  {% if flags %}
    {% for flag in flags %}
      <div class="flag">
        <strong>[{{ flag.type | upper }}]</strong> {{ flag.value }}
        <span style="color:#484f58; font-size:11px; float:right;">{{ flag.created_at }}</span>
      </div>
    {% endfor %}
  {% else %}
    <p style="color:#484f58;">No se registraron flags.</p>
  {% endif %}

  <h2>📝 Notas de la Sesión</h2>
  {% if notes %}
    {% for note in notes %}
      <div class="note">
        {{ note.content }}
        <span style="color:#484f58; font-size:11px; float:right;">{{ note.created_at }}</span>
      </div>
    {% endfor %}
  {% else %}
    <p style="color:#484f58;">No se registraron notas.</p>
  {% endif %}

  <div class="footer">
    Generado por CTFPilot v0.1.0 — {{ generated_at }}
  </div>
</body>
</html>
"""

def generate_report(session_id: int, fmt: str = "html") -> str:
    data = get_session_data(session_id)
    session_row = data["session"]

    session = {
        "name": session_row[1],
        "target": session_row[2],
        "platform": session_row[3],
        "started_at": session_row[4],
    }

    notes = [{"content": n[0], "created_at": n[1]} for n in data["notes"]]
    flags = [{"type": f[0], "value": f[1], "created_at": f[2]} for f in data["flags"]]
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = Template(TEMPLATE).render(
        session=session,
        notes=notes,
        flags=flags,
        generated_at=generated_at
    )

    desktop = Path.home() / "Desktop" / "CTFPilot"
    desktop.mkdir(exist_ok=True)
    filename = f"{session['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if fmt == "html":
        output_path = desktop / f"{filename}.html"
        output_path.write_text(html, encoding="utf-8")
    elif fmt == "pdf":
        try:
            from weasyprint import HTML
            output_path = desktop / f"{filename}.pdf"
            HTML(string=html).write_pdf(str(output_path))
        except Exception as e:
            output_path = desktop / f"{filename}.html"
            output_path.write_text(html, encoding="utf-8")

    return str(output_path)