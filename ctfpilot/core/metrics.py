from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

SESSIONS_CREATED = Counter(
    'ctfpilot_sessions_total',
    'Total de sesiones creadas',
    ['platform']
)

FLAGS_CAPTURED = Counter(
    'ctfpilot_flags_total',
    'Total de flags capturadas',
    ['flag_type']
)

REPORTS_GENERATED = Counter(
    'ctfpilot_reports_total',
    'Total de reportes generados',
    ['format']
)

SESSION_DURATION = Histogram(
    'ctfpilot_session_duration_seconds',
    'Duracion de las sesiones en segundos',
    buckets=[300, 600, 1800, 3600, 7200, 14400]
)

ACTIVE_SESSIONS = Gauge(
    'ctfpilot_active_sessions',
    'Sesiones activas actualmente'
)

def start_metrics_server(port: int = 8000):
    try:
        start_http_server(port)
    except Exception:
        pass

def record_session_created(platform: str):
    SESSIONS_CREATED.labels(platform=platform).inc()
    ACTIVE_SESSIONS.inc()

def record_flag_captured(flag_type: str):
    FLAGS_CAPTURED.labels(flag_type=flag_type).inc()

def record_report_generated(fmt: str):
    REPORTS_GENERATED.labels(format=fmt).inc()

def record_session_finished(duration_seconds: float):
    SESSION_DURATION.observe(duration_seconds)
    ACTIVE_SESSIONS.dec()