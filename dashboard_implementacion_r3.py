"""
Dashboard: Progreso de Implementación Ronda 3 – Aulas en Re-Conexión
=====================================================================
Reads the 'Seleccionados' sheet from the project Google Spreadsheet and
generates a self-contained HTML monitoring dashboard using the
Aulas en Re-Conexión design system.

Usage:
    python3.13 dashboard_implementacion_r3.py

Output:
    outputs/dashboard_implementacion_r3.html
"""

import calendar
import os
import re
import webbrowser
from collections import defaultdict
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
# When running in CI (GitHub Actions) or locally inside the site repo,
# output goes to monitoreo.html next to this script.
SITE_OUTPUT      = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'monitoreo.html')
OUTPUT           = SITE_OUTPUT  # same file
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'service_account.json')

SPREADSHEET_ID = '1-5i3p0lxTrorr8ObhDi1DJIo6caTUdR9UKS679BL9rc'
SHEET_NAME     = 'Seleccionados'

# ---------------------------------------------------------------------------
# Design tokens  (Aulas en Re-Conexión system)
# ---------------------------------------------------------------------------
RAINBOW_BAR_CSS = (
    'linear-gradient(to right, '
    '#E8302A 0%, #E8302A 16.6%, '
    '#F47920 16.6%, #F47920 33.2%, '
    '#F9C200 33.2%, #F9C200 49.8%, '
    '#4BAD4E 49.8%, #4BAD4E 66.4%, '
    '#3AABE3 66.4%, #3AABE3 83%, '
    '#8B4EA6 83%, #8B4EA6 100%)'
)

# Dupla → (background, text-color, short label)
DUPLA_COLORS = {
    'Camila - Paula V':   ('#3AABE3', '#fff',    'C·PV'),
    'Tania V - Yulieth':  ('#F47920', '#fff',    'TV·Y'),
    'Wendy - Wilmer':     ('#4BAD4E', '#fff',    'W·W'),
    'Juliana - Tania M':  ('#8B4EA6', '#fff',    'J·TM'),
    'Naiara - Loren':     ('#E8302A', '#fff',    'N·L'),
    'Vanne - Conny':      ('#F9C200', '#1a1a2e', 'V·C'),
    'Laura H - Nathalia': ('#1A8C7A', '#fff',    'LH·N'),
}

STATUS_CFG = {
    'Completada':  ('#4BAD4E', '#fff'),
    'Agendada':    ('#3AABE3', '#fff'),
    'Por agendar': ('#e5e7eb', '#9ca3af'),
}

# Session → (background, text-color) — palette colors in order
SESSION_COLORS = {
    0: ('#8B4EA6', '#fff'),   # morado  – S0 Diagnóstico
    1: ('#E8302A', '#fff'),   # rojo    – S1 Emociones
    2: ('#F47920', '#fff'),   # naranja – S2 Empatía
    3: ('#4BAD4E', '#fff'),   # verde   – S3 Convivencia
    4: ('#3AABE3', '#fff'),   # azul    – S4 Herramientas
}

SESSION_NAMES = [
    ('S0', 'Diagnóstico'),
    ('S1', 'Emociones'),
    ('S2', 'Empatía'),
    ('S3', 'Convivencia'),
    ('S4', 'Herramientas'),
]

MESES_ES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
}

DIAS_ES = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie']

MESES_LABEL = {
    4: 'Abril', 5: 'Mayo', 6: 'Junio',
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def safe_str(val, default=''):
    if val is None:
        return default
    s = str(val).strip()
    return default if s in ('', 'nan', 'NaN') else s


def parse_date_es(text, year=2026):
    """Parse 'lunes, 20 de abril' → date(2026, 4, 20). Returns None on failure."""
    t = safe_str(text).lower()
    m = re.search(r'(\d{1,2})\s+de\s+(\w+)', t)
    if not m:
        return None
    day  = int(m.group(1))
    mes  = MESES_ES.get(m.group(2).strip())
    if not mes:
        return None
    try:
        return date(year, mes, day)
    except ValueError:
        return None


def dupla_style(dupla):
    bg, fg, _ = DUPLA_COLORS.get(dupla, ('#e5e7eb', '#555', dupla[:4]))
    return bg, fg


def dupla_short(dupla):
    return DUPLA_COLORS.get(dupla, ('#e5e7eb', '#555', dupla[:4]))[2]


def status_chip(estado):
    bg, fg = STATUS_CFG.get(estado, ('#e5e7eb', '#9ca3af'))
    icon = '✓' if estado == 'Completada' else ('📅' if estado == 'Agendada' else '○')
    return (
        f'<span class="chip" style="background:{bg};color:{fg};">'
        f'{icon} {estado}</span>'
    )


# ---------------------------------------------------------------------------
# Load data from Google Sheets
# ---------------------------------------------------------------------------
def load_seleccionados():
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc      = gspread.authorize(creds)
        ws      = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        all_rows = ws.get_all_values()
    except Exception as e:
        print(f'ERROR fetching Google Sheet: {e}')
        raise

    if len(all_rows) < 2:
        return []

    headers = all_rows[0]

    def col(row, name, default=''):
        try:
            return safe_str(row[headers.index(name)], default)
        except (ValueError, IndexError):
            return default

    schools = []
    for row in all_rows[1:]:
        n_raw = safe_str(row[0] if row else '')
        if not n_raw or not n_raw.isdigit():
            continue

        sessions = []
        for i in range(5):
            fecha_str = col(row, f'Fecha sesión {i}')
            estado    = col(row, f'Estado sesión {i}') or 'Por agendar'
            sessions.append({
                'fecha':     fecha_str,
                'fecha_dt':  parse_date_es(fecha_str),
                'estado':    estado,
            })

        schools.append({
            'n':           int(n_raw),
            'gestor':      col(row, 'Gestor(a) o dupla de contacto del colegio'),
            'codigo':      col(row, 'Codigo AeR'),
            'dane':        col(row, 'DANE Colegio'),
            'localidad':   col(row, 'Localidad').title(),
            'colegio':     col(row, 'Colegio'),
            'jornada':     col(row, 'Jornada').title(),
            'aula':        col(row, 'Aula'),
            'estudiantes': col(row, 'Estudiantes'),
            'director':    col(row, 'Director(a) de curso').title(),
            'contacto':    col(row, 'Contacto en Colegio').title(),
            'rol':         col(row, 'Rol'),
            'celular':     col(row, 'Celular'),
            'sessions':    sessions,
        })

    return schools


# ---------------------------------------------------------------------------
# Calendar builder
# ---------------------------------------------------------------------------
def build_calendar_events(schools):
    """
    Returns dict: date → list of {dupla, colegio, aula, session_idx, estado, codigo}
    """
    events = defaultdict(list)
    for s in schools:
        for i, ses in enumerate(s['sessions']):
            if ses['fecha_dt']:
                events[ses['fecha_dt']].append({
                    'dupla':       s['gestor'],
                    'colegio':     s['colegio'],
                    'aula':        s['aula'],
                    'codigo':      s['codigo'],
                    'session_idx': i,
                    'estado':      ses['estado'],
                })
    return events


def render_calendar_month(year, month, events):
    """Render a full calendar month as HTML (Mon–Fri only)."""
    month_label = MESES_LABEL.get(month, str(month))

    cal = calendar.monthcalendar(year, month)  # list of weeks, 0 = not this month

    day_headers = ''.join(
        f'<div class="cal-day-hdr">{d}</div>' for d in DIAS_ES
    )

    weeks_html = ''
    for week in cal:
        weekdays = week[:5]  # Mon–Fri only (indices 0–4)
        # Skip weeks where all 5 weekdays are outside the month
        if all(d == 0 for d in weekdays):
            continue
        weeks_html += '<div class="cal-week">'
        for d in weekdays:
            if d == 0:
                weeks_html += '<div class="cal-cell cal-cell-empty"></div>'
                continue
            dt = date(year, month, d)
            day_events = events.get(dt, [])

            today_cls = ' cal-today' if dt == date.today() else ''

            chips_html = ''
            for ev in sorted(day_events, key=lambda e: e['session_idx']):
                bg, fg = SESSION_COLORS.get(ev['session_idx'], ('#888', '#fff'))
                sname  = SESSION_NAMES[ev['session_idx']][0]
                est    = ev['estado']
                opacity = '1' if est in ('Completada', 'Agendada') else '0.35'
                border  = '2px solid rgba(0,0,0,0.25)' if est == 'Completada' else 'none'
                check   = ' ✓' if est == 'Completada' else ''
                colegio_short = ev['colegio'][:20] + '…' if len(ev['colegio']) > 20 else ev['colegio']
                tooltip = f"{ev['dupla']} · {ev['colegio']} · Aula {ev['aula']} · {sname} · {est}"
                chips_html += (
                    f'<div class="ev-chip" '
                    f'style="background:{bg};color:{fg};opacity:{opacity};border:{border};" '
                    f'title="{tooltip}">'
                    f'<div class="ev-chip-top">'
                    f'<span class="ev-sess">{sname}</span>'
                    f'<span class="ev-dupla">{ev["dupla"]}{check}</span>'
                    f'</div>'
                    f'<div class="ev-chip-school">{colegio_short} · A{ev["aula"]}</div>'
                    f'</div>'
                )

            n_ev = len(day_events)
            n_badge = f'<span class="day-n-badge">{n_ev}</span>' if n_ev > 0 else ''

            weeks_html += f"""
            <div class="cal-cell{today_cls}">
              <div class="cal-cell-top">
                <span class="cal-day-num">{d}</span>
                {n_badge}
              </div>
              <div class="cal-chips">{chips_html}</div>
            </div>"""
        weeks_html += '</div>'

    return f"""
    <div class="cal-month-wrap">
      <div class="cal-month-header">
        <div class="cal-month-title">{month_label} {year}</div>
      </div>
      <div class="cal-grid">
        <div class="cal-week cal-week-hdr">{day_headers}</div>
        {weeks_html}
      </div>
    </div>"""


# ---------------------------------------------------------------------------
# School card renderer
# ---------------------------------------------------------------------------
def render_school_card(s):
    sessions_html = ''
    for i, ses in enumerate(s['sessions']):
        bg, fg = STATUS_CFG.get(ses['estado'], ('#e5e7eb', '#9ca3af'))
        icon   = '✓' if ses['estado'] == 'Completada' else ('📅' if ses['estado'] == 'Agendada' else '○')
        sname, stheme = SESSION_NAMES[i]
        fecha_display = ses['fecha'] if ses['fecha'] else '—'
        sessions_html += f"""
        <div class="track-step">
          <div class="track-dot" style="background:{bg};color:{fg};" title="{ses['estado']}">
            <span class="track-icon">{icon}</span>
            <span class="track-slabel">{sname}</span>
          </div>
          <div class="track-info">
            <div class="track-theme">{stheme}</div>
            <div class="track-date">{fecha_display}</div>
          </div>
        </div>"""

    comp    = sum(1 for ses in s['sessions'] if ses['estado'] == 'Completada')
    sched   = sum(1 for ses in s['sessions'] if ses['estado'] == 'Agendada')
    pending = sum(1 for ses in s['sessions'] if ses['estado'] == 'Por agendar')
    pct     = round(100 * comp / 5)

    # Left accent color
    if comp == 5:
        accent = '#4BAD4E'
    elif comp > 0 or sched > 0:
        accent = '#3AABE3'
    else:
        accent = '#d1d5db'

    # Dupla badge
    dbg, dfg = dupla_style(s['gestor'])
    dupla_badge = (
        f'<span class="dupla-badge" style="background:{dbg};color:{dfg};">'
        f'{s["gestor"] or "Sin asignar"}</span>'
    )

    celular_html = (
        f'<a href="tel:{s["celular"]}">{s["celular"]}</a>'
        if s['celular'] else '—'
    )

    return f"""
  <div class="school-card" id="school-{s['n']}" style="border-left:5px solid {accent};">
    <div class="card-rainbow-bar"></div>
    <div class="card-body">

      <!-- Card header -->
      <div class="card-header-row">
        <div class="card-title-area">
          <div class="card-top-meta">
            <span class="card-num">#{s['n']}</span>
            <span class="card-codigo">{s['codigo']}</span>
            {dupla_badge}
          </div>
          <h2 class="card-title">{s['colegio']}</h2>
          <div class="card-submeta">
            <span>📍 {s['localidad']}</span>
            <span>⏰ {s['jornada']}</span>
            <span>🏫 Aula {s['aula']}</span>
            <span>👥 {s['estudiantes']} est.</span>
          </div>
        </div>
        <div class="card-progress-block">
          <div class="prog-ring">
            <span class="prog-num">{comp}</span><span class="prog-den">/5</span>
          </div>
          <div class="prog-sub">sesiones</div>
          <div class="prog-bar-track">
            <div class="prog-bar-fill" style="width:{pct}%;"></div>
          </div>
          <div class="prog-mini-stats">
            <span style="color:#4BAD4E;">✓{comp}</span>
            <span style="color:#3AABE3;">📅{sched}</span>
            <span style="color:#9ca3af;">○{pending}</span>
          </div>
        </div>
      </div>

      <!-- Session tracker -->
      <div class="session-track">
        {sessions_html}
      </div>

      <!-- Footer info -->
      <div class="card-info-row">
        <div class="info-item"><span class="info-lbl">Director/a:</span> {s['director']}</div>
        <div class="info-item"><span class="info-lbl">Contacto:</span> {s['contacto']}
          {f'<span class="role-chip">{s["rol"]}</span>' if s['rol'] else ''}
        </div>
        <div class="info-item"><span class="info-lbl">Teléfono:</span> {celular_html}</div>
      </div>

    </div>
  </div>"""


# ---------------------------------------------------------------------------
# Main: load + compute stats
# ---------------------------------------------------------------------------
schools   = load_seleccionados()
total_cls = len(schools)
generated = datetime.now().strftime('%d/%m/%Y %H:%M')

# Session-level aggregates
session_stats = []
for i in range(5):
    c = sum(1 for s in schools if s['sessions'][i]['estado'] == 'Completada')
    a = sum(1 for s in schools if s['sessions'][i]['estado'] == 'Agendada')
    p = sum(1 for s in schools if s['sessions'][i]['estado'] == 'Por agendar')
    session_stats.append({'completadas': c, 'agendadas': a, 'por_agendar': p})

total_sessions    = total_cls * 5
total_completadas = sum(st['completadas'] for st in session_stats)
total_agendadas   = sum(st['agendadas']   for st in session_stats)
total_pending     = sum(st['por_agendar'] for st in session_stats)
overall_pct       = round(100 * total_completadas / total_sessions) if total_sessions else 0
pct_agendadas     = round(100 * total_agendadas   / total_sessions) if total_sessions else 0

full_done = sum(1 for s in schools if all(ses['estado'] == 'Completada' for ses in s['sessions']))
started   = sum(1 for s in schools if any(ses['estado'] == 'Completada' for ses in s['sessions']))

# Facilitator aggregates
gestor_data = defaultdict(lambda: {'aulas': 0, 'c': 0, 'a': 0, 'p': 0})
for s in schools:
    g = s['gestor'] or 'Sin asignar'
    gestor_data[g]['aulas'] += 1
    for ses in s['sessions']:
        if ses['estado'] == 'Completada':  gestor_data[g]['c'] += 1
        elif ses['estado'] == 'Agendada': gestor_data[g]['a'] += 1
        else:                              gestor_data[g]['p'] += 1

# Calendar events
cal_events = build_calendar_events(schools)

# Sort school cards: in-progress first, then not started, then all-done
def sort_key(s):
    c = sum(1 for ses in s['sessions'] if ses['estado'] == 'Completada')
    a = sum(1 for ses in s['sessions'] if ses['estado'] == 'Agendada')
    if c == 5:     return (2, -c)
    if c > 0 or a > 0: return (0, -c)
    return (1, 0)

schools_sorted = sorted(schools, key=sort_key)

# ---------------------------------------------------------------------------
# Build HTML sections
# ---------------------------------------------------------------------------

# --- Summary stats bar ---
summary_bar_html = f"""
  <div class="sum-stat sum-dark">
    <div class="sum-number">{total_cls}</div>
    <div class="sum-label">Aulas seleccionadas</div>
  </div>
  <div class="sum-stat sum-verde">
    <div class="sum-number">{total_completadas}</div>
    <div class="sum-label">Sesiones completadas</div>
  </div>
  <div class="sum-stat sum-azul">
    <div class="sum-number">{total_agendadas}</div>
    <div class="sum-label">Sesiones agendadas</div>
  </div>
  <div class="sum-stat">
    <div class="sum-number" style="color:var(--muted);">{total_pending}</div>
    <div class="sum-label">Por agendar</div>
  </div>
  <div class="sum-stat sum-verde">
    <div class="sum-number">{started}</div>
    <div class="sum-label">Aulas iniciadas</div>
  </div>
  <div class="sum-stat sum-verde">
    <div class="sum-number">{full_done}</div>
    <div class="sum-label">Aulas finalizadas</div>
  </div>"""

# --- Session color legend (for calendar) ---
session_legend_html = ''
for i, (snum, stheme) in enumerate(SESSION_NAMES):
    bg, fg = SESSION_COLORS[i]
    session_legend_html += (
        f'<div class="legend-item">'
        f'<span class="legend-dot" style="background:{bg};color:{fg};font-size:11px;">{snum}</span>'
        f'<span class="legend-name">{stheme}</span>'
        f'</div>'
    )
# Status legend
session_legend_html += (
    '<div class="legend-item" style="margin-left:auto;">'
    '<span style="font-size:11px;color:var(--muted);">'
    '<span style="opacity:1;display:inline-block;width:28px;height:14px;border-radius:4px;background:#8B4EA6;vertical-align:middle;margin-right:4px;"></span>Agendada · '
    '<span style="opacity:1;display:inline-block;width:28px;height:14px;border-radius:4px;background:#8B4EA6;border:2px solid rgba(0,0,0,0.25);vertical-align:middle;margin-right:4px;margin-left:6px;"></span>Completada · '
    '<span style="opacity:0.35;display:inline-block;width:28px;height:14px;border-radius:4px;background:#8B4EA6;vertical-align:middle;margin-right:4px;margin-left:6px;"></span>Por agendar'
    '</span></div>'
)

# --- Dupla legend (separate, below calendar header) ---
dupla_legend_html = ''
for name, (bg, fg, short) in DUPLA_COLORS.items():
    d = gestor_data.get(name, {'aulas': 0, 'c': 0, 'a': 0, 'p': 0})
    dupla_legend_html += (
        f'<div class="legend-item">'
        f'<span class="legend-dot" style="background:{bg};color:{fg};">{short}</span>'
        f'<span class="legend-name">{name}</span>'
        f'<span class="legend-n">{d["aulas"]} aulas</span>'
        f'</div>'
    )

# --- Calendar months ---
cal_html = ''.join(render_calendar_month(2026, m, cal_events) for m in [4, 5, 6])

# --- Session panels ---
session_panels_html = ''
for i, st in enumerate(session_stats):
    snum, stheme = SESSION_NAMES[i]
    pct_c = round(100 * st['completadas'] / total_cls) if total_cls else 0
    pct_a = round(100 * st['agendadas']   / total_cls) if total_cls else 0
    session_panels_html += f"""
    <div class="session-panel">
      <div class="sp-top">
        <div class="sp-num">{snum}</div>
        <div>
          <div class="sp-title">Sesión {i}</div>
          <div class="sp-theme">{stheme}</div>
        </div>
      </div>
      <div class="sp-counts">
        <div class="sp-count" style="color:#4BAD4E;"><span class="sp-n">{st['completadas']}</span><br>Comp.</div>
        <div class="sp-count" style="color:#3AABE3;"><span class="sp-n">{st['agendadas']}</span><br>Agend.</div>
        <div class="sp-count" style="color:#9ca3af;"><span class="sp-n">{st['por_agendar']}</span><br>Pend.</div>
      </div>
      <div class="sp-bar">
        <div style="width:{pct_c}%;background:#4BAD4E;height:100%;"></div>
        <div style="width:{pct_a}%;background:#3AABE3;height:100%;opacity:0.6;"></div>
      </div>
      <div class="sp-pct">{pct_c}% completado</div>
    </div>"""

# --- Facilitator table ---
gestor_table_rows = ''
for g, d in sorted(gestor_data.items()):
    bg, fg = dupla_style(g)
    t      = d['aulas'] * 5
    pct    = round(100 * d['c'] / t) if t else 0
    gestor_table_rows += f"""
      <tr>
        <td>
          <span class="dupla-badge" style="background:{bg};color:{fg};">{g}</span>
        </td>
        <td class="tc">{d['aulas']}</td>
        <td class="tc" style="color:#4BAD4E;font-weight:700;">{d['c']}</td>
        <td class="tc" style="color:#3AABE3;font-weight:700;">{d['a']}</td>
        <td class="tc" style="color:#9ca3af;">{d['p']}</td>
        <td>
          <div class="pbar-wrap">
            <div class="pbar-track">
              <div style="width:{pct}%;background:#4BAD4E;height:100%;border-radius:4px;"></div>
            </div>
            <span class="pbar-pct" style="color:#4BAD4E;">{pct}%</span>
          </div>
        </td>
      </tr>"""

# --- Summary table ---
summary_table_rows = ''
for s in schools_sorted:
    comp = sum(1 for ses in s['sessions'] if ses['estado'] == 'Completada')
    dots = ''
    for ses in s['sessions']:
        bg, fg = STATUS_CFG.get(ses['estado'], ('#ddd', '#666'))
        icon         = '✓' if ses['estado'] == 'Completada' else ('•' if ses['estado'] == 'Agendada' else '○')
        estado_label = ses['estado']
        dots        += f'<span class="tbl-dot" style="background:{bg};color:{fg};" title="{estado_label}">{icon}</span>'
    dbg, dfg = dupla_style(s['gestor'])
    prog_color = '#4BAD4E' if comp == 5 else ('#3AABE3' if comp > 0 else '#9ca3af')
    summary_table_rows += f"""
      <tr>
        <td class="tc">{s['n']}</td>
        <td><a href="#school-{s['n']}">{s['colegio']}</a></td>
        <td>{s['localidad']}</td>
        <td class="tc">{s['aula']}</td>
        <td><span class="dupla-badge sm" style="background:{dbg};color:{dfg};">{s['gestor']}</span></td>
        <td style="white-space:nowrap;">{dots}</td>
        <td class="tc" style="font-weight:800;color:{prog_color};">{comp}/5</td>
      </tr>"""

# --- School cards ---
all_cards_html = '\n'.join(render_school_card(s) for s in schools_sorted)

# ---------------------------------------------------------------------------
# Assemble full HTML  (design matches aulasenreconexion.com)
# ---------------------------------------------------------------------------
HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Monitoreo Ronda 3 – Aulas en Re-Conexión</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    /* ===== DESIGN TOKENS (match aulasenreconexion.com) ===== */
    :root {{
      --rojo:    #E8302A;
      --naranja: #F47920;
      --amarillo:#F9C200;
      --verde:   #4BAD4E;
      --azul:    #3AABE3;
      --morado:  #8B4EA6;
      --dark:    #2D2D2D;
      --text:    #4A4A4A;
      --muted:   #888888;
      --line:    #E8E8E8;
      --bg:      #F8F9FA;
      --card:    #ffffff;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; overflow-x: hidden; }}
    body {{
      font-family: 'Nunito Sans', sans-serif;
      background: #ffffff;
      color: var(--text);
      font-size: 14px;
      line-height: 1.6;
    }}

    /* ===== NAVBAR (identical to site) ===== */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #ffffff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      border-top: 6px solid;
      border-image: linear-gradient(to right,
        var(--rojo)     0%,    var(--rojo)     16.66%,
        var(--naranja)  16.66%, var(--naranja)  33.32%,
        var(--amarillo) 33.32%, var(--amarillo) 49.98%,
        var(--verde)    49.98%, var(--verde)    66.64%,
        var(--azul)     66.64%, var(--azul)     83.3%,
        var(--morado)   83.3%,  var(--morado)   100%) 1;
    }}
    .navbar-content {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 70px;
    }}
    .navbar-logo {{
      font-family: 'Nunito', sans-serif;
      font-size: 14px;
      font-weight: 900;
      letter-spacing: 0.5px;
      text-decoration: none;
    }}
    .nl-a {{ color: var(--rojo); }}
    .nl-u {{ color: var(--naranja); }}
    .nl-l {{ color: var(--amarillo); }}
    .nl-s {{ color: var(--verde); }}
    .nl-r {{ color: var(--azul); }}
    .nl-c {{ color: var(--morado); }}
    .nl-gray {{ color: #999; }}
    .navbar-nav {{
      display: flex;
      gap: 2rem;
      align-items: center;
      list-style: none;
    }}
    .navbar-nav a {{
      text-decoration: none;
      color: #333;
      font-size: 14px;
      font-weight: 600;
      transition: color 0.3s ease;
      position: relative;
    }}
    .navbar-nav a:hover {{ color: var(--rojo); }}
    .navbar-nav a.active {{
      color: var(--rojo);
      font-weight: 700;
    }}
    .navbar-nav a.active::after {{
      content: '';
      position: absolute;
      bottom: -8px;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--rojo);
      border-radius: 2px;
    }}

    /* ===== PAGE HERO ===== */
    .page-hero {{
      background: #ffffff;
      padding: 3rem 2rem 2.5rem;
      text-align: center;
      border-bottom: 1px solid var(--line);
    }}
    .page-hero-label {{
      font-family: 'Nunito', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: #AAAAAA;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 0.75rem;
    }}
    .page-hero-title {{
      font-family: 'Nunito', sans-serif;
      font-size: clamp(28px, 5vw, 42px);
      font-weight: 900;
      color: var(--dark);
      letter-spacing: -0.5px;
      line-height: 1.2;
      margin-bottom: 0.5rem;
    }}
    .page-hero-sub {{
      font-family: 'Nunito Sans', sans-serif;
      font-size: 15px;
      color: var(--muted);
      margin-bottom: 1.5rem;
    }}
    .rainbow-divider {{
      width: 60px;
      height: 4px;
      margin: 1rem auto 0;
      border-radius: 2px;
      background: linear-gradient(to right,
        var(--rojo)     0%,    var(--rojo)     16.66%,
        var(--naranja)  16.66%, var(--naranja)  33.32%,
        var(--amarillo) 33.32%, var(--amarillo) 49.98%,
        var(--verde)    49.98%, var(--verde)    66.64%,
        var(--azul)     66.64%, var(--azul)     83.3%,
        var(--morado)   83.3%,  var(--morado)   100%);
    }}

    /* ===== STATS ROW ===== */
    .stats-row {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      align-items: stretch;
    }}
    .stat-box {{
      flex: 1;
      min-width: 110px;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      padding: 18px 16px 14px;
      text-align: center;
    }}
    .stat-box.s-dark  {{ background: #1a1a2e; border-color: #1a1a2e; }}
    .stat-box.s-verde {{ background: #f0faf0; border-color: var(--verde); }}
    .stat-box.s-azul  {{ background: #f0f8ff; border-color: var(--azul); }}
    .stat-num {{
      font-family: 'Nunito', sans-serif;
      font-size: 32px;
      font-weight: 900;
      line-height: 1;
      color: var(--dark);
    }}
    .s-dark  .stat-num {{ color: #fff; }}
    .s-verde .stat-num {{ color: var(--verde); }}
    .s-azul  .stat-num {{ color: var(--azul); }}
    .stat-lbl {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
    .s-dark .stat-lbl {{ color: rgba(255,255,255,0.5); }}
    .updated-tag {{
      margin-left: auto;
      font-size: 11px;
      color: var(--muted);
      align-self: flex-end;
      padding-bottom: 2px;
      white-space: nowrap;
    }}

    /* ===== OVERALL PROGRESS ===== */
    .progress-block {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .pb-label {{
      font-family: 'Nunito', sans-serif;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--muted);
      white-space: nowrap;
    }}
    .pb-track {{
      flex: 1;
      min-width: 120px;
      background: #e5e7eb;
      border-radius: 6px;
      height: 10px;
      overflow: hidden;
      display: flex;
    }}
    .pb-fill-c {{ background: var(--verde); height: 100%; }}
    .pb-fill-a {{ background: var(--azul); height: 100%; opacity: 0.55; }}
    .pb-pct {{
      font-family: 'Nunito', sans-serif;
      font-size: 16px;
      font-weight: 900;
      color: var(--verde);
      white-space: nowrap;
    }}
    .pb-legend {{
      display: flex;
      gap: 14px;
      font-size: 12px;
      color: var(--muted);
    }}
    .pb-dot {{
      display: inline-block;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      margin-right: 4px;
      vertical-align: middle;
    }}

    /* ===== MAIN LAYOUT ===== */
    .wrap {{
      max-width: 1400px;
      margin: 2rem auto;
      padding: 0 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
    }}

    /* ===== SECTION CARD ===== */
    .section-card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      overflow: hidden;
    }}
    .sc-body {{ padding: 24px 28px; }}
    .sc-title {{
      font-family: 'Nunito', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: var(--dark);
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
    }}

    /* ===== LEGEND ===== */
    .legend-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
    }}
    .legend-dot {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 34px;
      height: 20px;
      border-radius: 10px;
      font-family: 'Nunito', sans-serif;
      font-size: 9px;
      font-weight: 800;
      letter-spacing: 0.3px;
      flex-shrink: 0;
    }}
    .legend-name {{ font-weight: 600; color: var(--text); }}
    .legend-n    {{ color: var(--muted); font-size: 11px; }}

    /* ===== CALENDAR ===== */
    .cal-months {{ display: flex; flex-direction: column; gap: 24px; }}
    .cal-month-wrap {{
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    .cal-month-header {{
      background: #1a1a2e;
      color: #fff;
      padding: 10px 18px;
      font-family: 'Nunito', sans-serif;
      font-size: 14px;
      font-weight: 800;
    }}
    .cal-grid {{ background: var(--card); }}
    .cal-week {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      border-bottom: 1px solid var(--line);
    }}
    .cal-week:last-child {{ border-bottom: none; }}
    .cal-week-hdr {{ background: var(--bg); }}
    .cal-day-hdr {{
      font-family: 'Nunito', sans-serif;
      font-size: 11px;
      font-weight: 700;
      color: var(--muted);
      text-align: center;
      padding: 8px 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .cal-cell {{
      min-height: 110px;
      padding: 6px 7px;
      border-right: 1px solid var(--line);
      position: relative;
    }}
    .cal-cell:last-child {{ border-right: none; }}
    .cal-cell-empty {{
      min-height: 110px;
      background: var(--bg);
      border-right: 1px solid var(--line);
    }}
    .cal-cell-empty:last-child {{ border-right: none; }}
    .cal-today {{ background: #fffbf0; }}
    .cal-today .cal-day-num {{ color: var(--naranja); font-weight: 900; }}
    .cal-cell-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }}
    .cal-day-num {{
      font-family: 'Nunito', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--dark);
    }}
    .day-n-badge {{
      background: #1a1a2e;
      color: #fff;
      font-family: 'Nunito', sans-serif;
      font-size: 9px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 8px;
    }}
    .cal-chips {{ display: flex; flex-direction: column; gap: 3px; }}
    .ev-chip {{
      display: flex;
      flex-direction: column;
      gap: 1px;
      border-radius: 5px;
      padding: 3px 5px;
      font-family: 'Nunito', sans-serif;
      font-size: 10px;
      font-weight: 700;
      cursor: default;
    }}
    .ev-chip-top {{ display: flex; align-items: baseline; gap: 4px; flex-wrap: wrap; }}
    .ev-chip-school {{
      font-size: 8.5px;
      font-weight: 600;
      opacity: 0.88;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }}
    .ev-dupla {{
      font-size: 9px;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      flex: 1;
      min-width: 0;
    }}
    .ev-sess {{
      font-size: 9px;
      opacity: 0.85;
      flex-shrink: 0;
      background: rgba(0,0,0,0.18);
      border-radius: 3px;
      padding: 0 3px;
    }}

    /* ===== SESSION PANELS ===== */
    .session-panels {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
    }}
    .session-panel {{
      background: var(--bg);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px 14px 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .sp-top {{ display: flex; align-items: center; gap: 10px; }}
    .sp-num {{
      font-family: 'Nunito', sans-serif;
      font-size: 24px;
      font-weight: 900;
      color: var(--dark);
      line-height: 1;
    }}
    .sp-title {{
      font-family: 'Nunito', sans-serif;
      font-size: 11px;
      font-weight: 700;
      color: var(--dark);
    }}
    .sp-theme {{ font-size: 10px; color: var(--muted); }}
    .sp-counts {{ display: flex; gap: 8px; }}
    .sp-count {{ flex: 1; text-align: center; font-size: 10px; font-weight: 600; }}
    .sp-n {{
      font-family: 'Nunito', sans-serif;
      font-size: 20px;
      font-weight: 800;
      line-height: 1;
      display: block;
    }}
    .sp-bar {{
      height: 7px;
      background: #e5e7eb;
      border-radius: 4px;
      overflow: hidden;
      display: flex;
    }}
    .sp-pct {{ font-size: 10px; font-weight: 700; color: var(--verde); text-align: right; }}

    /* ===== TABLES ===== */
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    .data-table thead th {{
      background: #1a1a2e;
      color: #fff;
      font-family: 'Nunito', sans-serif;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 10px 12px;
      text-align: left;
    }}
    .data-table tbody td {{
      padding: 9px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: middle;
    }}
    .tc {{ text-align: center; }}
    .data-table tbody tr:hover {{ background: #f5f8ff; }}
    .data-table a {{ color: var(--azul); text-decoration: none; font-weight: 600; }}
    .data-table a:hover {{ text-decoration: underline; }}
    .pbar-wrap {{ display: flex; align-items: center; gap: 8px; }}
    .pbar-track {{ flex: 1; background: #e5e7eb; border-radius: 4px; height: 8px; overflow: hidden; }}
    .pbar-pct {{ font-size: 12px; font-weight: 700; min-width: 34px; }}
    .tbl-dot {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      font-size: 10px;
      font-weight: 700;
      margin: 1px;
    }}

    /* ===== BADGES ===== */
    .dupla-badge {{
      display: inline-block;
      font-family: 'Nunito', sans-serif;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 20px;
    }}
    .dupla-badge.sm {{ font-size: 10px; padding: 2px 8px; }}
    .role-chip {{
      display: inline-block;
      background: #e8edf7;
      color: var(--dark);
      font-size: 10px;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: 20px;
      margin-left: 4px;
      font-family: 'Nunito', sans-serif;
    }}

    /* ===== SCHOOL CARDS ===== */
    .school-card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      overflow: hidden;
    }}
    .card-rainbow-bar {{
      height: 4px;
      background: linear-gradient(to right,
        var(--rojo)     0%,    var(--rojo)     16.66%,
        var(--naranja)  16.66%, var(--naranja)  33.32%,
        var(--amarillo) 33.32%, var(--amarillo) 49.98%,
        var(--verde)    49.98%, var(--verde)    66.64%,
        var(--azul)     66.64%, var(--azul)     83.3%,
        var(--morado)   83.3%,  var(--morado)   100%);
    }}
    .card-body {{ padding: 20px 24px; }}
    .card-header-row {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .card-title-area {{ flex: 1; min-width: 200px; }}
    .card-top-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      flex-wrap: wrap;
    }}
    .card-num {{ font-size: 11px; color: var(--muted); font-weight: 700; }}
    .card-codigo {{
      font-family: 'Nunito', sans-serif;
      font-size: 12px;
      font-weight: 800;
      background: #1a1a2e;
      color: #fff;
      padding: 2px 8px;
      border-radius: 4px;
    }}
    .card-title {{
      font-family: 'Nunito', sans-serif;
      font-size: 15px;
      font-weight: 800;
      color: var(--dark);
      margin-bottom: 5px;
      line-height: 1.3;
    }}
    .card-submeta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 12px;
      color: var(--muted);
    }}
    .card-progress-block {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
    }}
    .prog-ring {{ font-family: 'Nunito', sans-serif; font-weight: 900; line-height: 1; }}
    .prog-num {{ font-size: 30px; color: var(--dark); }}
    .prog-den {{ font-size: 14px; color: var(--muted); }}
    .prog-sub {{ font-size: 10px; color: var(--muted); }}
    .prog-bar-track {{
      width: 70px; height: 6px;
      background: #e5e7eb; border-radius: 3px; overflow: hidden;
    }}
    .prog-bar-fill {{ height: 100%; background: var(--verde); border-radius: 3px; }}
    .prog-mini-stats {{
      display: flex; gap: 8px;
      font-size: 11px; font-weight: 700;
      font-family: 'Nunito', sans-serif;
    }}
    .session-track {{
      display: flex;
      background: var(--bg);
      border-radius: 8px;
      padding: 14px 16px;
      margin-bottom: 14px;
      overflow-x: auto;
    }}
    .track-step {{
      flex: 1; min-width: 90px;
      display: flex; flex-direction: column;
      align-items: center; position: relative; gap: 6px;
    }}
    .track-step:not(:last-child)::after {{
      content: '';
      position: absolute;
      top: 21px;
      left: calc(50% + 22px);
      width: calc(100% - 44px);
      height: 2px;
      background: var(--line);
    }}
    .track-dot {{
      width: 44px; height: 44px; border-radius: 50%;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
      z-index: 1; position: relative;
    }}
    .track-icon  {{ font-size: 14px; line-height: 1; }}
    .track-slabel {{
      font-family: 'Nunito', sans-serif;
      font-size: 9px; font-weight: 700; line-height: 1;
    }}
    .track-info {{ text-align: center; }}
    .track-theme {{ font-size: 10px; font-weight: 600; color: var(--dark); }}
    .track-date  {{ font-size: 10px; color: var(--muted); line-height: 1.3; max-width: 80px; }}
    .card-info-row {{
      display: flex; flex-wrap: wrap; gap: 16px;
      font-size: 12px; color: var(--text);
      border-top: 1px solid var(--line); padding-top: 12px;
    }}
    .info-item {{ display: flex; align-items: center; gap: 5px; flex-wrap: wrap; }}
    .info-lbl {{ color: var(--muted); font-size: 11px; }}
    .info-item a {{ color: var(--azul); text-decoration: none; }}
    .info-item a:hover {{ text-decoration: underline; }}

    /* ===== FOOTER (identical to site) ===== */
    footer {{
      background: #1a1a2e;
      color: white;
      padding: 2rem;
      text-align: center;
      border-top: 6px solid;
      border-image: linear-gradient(to right,
        var(--rojo)     0%,    var(--rojo)     16.66%,
        var(--naranja)  16.66%, var(--naranja)  33.32%,
        var(--amarillo) 33.32%, var(--amarillo) 49.98%,
        var(--verde)    49.98%, var(--verde)    66.64%,
        var(--azul)     66.64%, var(--azul)     83.3%,
        var(--morado)   83.3%,  var(--morado)   100%) 1;
    }}
    .footer-content {{ max-width: 1200px; margin: 0 auto; }}
    .footer-logo {{
      font-family: 'Nunito', sans-serif;
      font-size: 16px; font-weight: 900;
      margin-bottom: 1rem; letter-spacing: 0.5px;
    }}
    .fl-a {{ color: var(--rojo); }}
    .fl-u {{ color: var(--naranja); }}
    .fl-l {{ color: var(--amarillo); }}
    .fl-s {{ color: var(--verde); }}
    .fl-r {{ color: var(--azul); }}
    .fl-c {{ color: var(--morado); }}
    .fl-gray {{ color: #999; }}
    .footer-tagline {{
      font-family: 'Nunito Sans', sans-serif;
      font-size: 14px; color: #aaa;
      font-weight: 600; font-style: italic;
    }}
    .footer-meta {{
      margin-top: 1.5rem; font-size: 13px; color: #888;
      border-top: 1px solid rgba(255,255,255,0.1);
      padding-top: 1.5rem;
    }}

    /* ===== RESPONSIVE ===== */
    @media (max-width: 900px) {{
      .session-panels {{ grid-template-columns: repeat(3, 1fr); }}
    }}
    @media (max-width: 768px) {{
      .navbar-content {{ padding: 0 1rem; height: 60px; }}
      .navbar-logo {{ font-size: 12px; }}
      .navbar-nav {{ gap: 1rem; }}
      .navbar-nav a {{ font-size: 12px; }}
      .wrap {{ padding: 0 1rem; margin: 1.5rem auto; gap: 1.5rem; }}
      .sc-body {{ padding: 18px 16px; }}
    }}
    @media (max-width: 480px) {{
      .navbar-nav {{ display: none; }}
      .session-panels {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    /* ===== REFRESH BUTTON ===== */
    .refresh-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 1.25rem;
      padding: 10px 24px;
      background: var(--rojo);
      color: #fff;
      font-family: 'Nunito', sans-serif;
      font-size: 13px;
      font-weight: 700;
      border: none;
      border-radius: 20px;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      box-shadow: 0 2px 8px rgba(232,48,42,0.3);
    }}
    .refresh-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(232,48,42,0.4);
    }}
    .refresh-btn:disabled {{
      background: #ccc;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }}
    .refresh-btn .spin {{
      display: inline-block;
      animation: spin 1s linear infinite;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .refresh-status {{
      display: block;
      margin-top: 0.6rem;
      font-size: 12px;
      color: var(--muted);
      min-height: 1.2em;
    }}
    .refresh-status.ok   {{ color: var(--verde); font-weight: 600; }}
    .refresh-status.err  {{ color: var(--rojo);  font-weight: 600; }}
  </style>
</head>
<body>

<!-- ── NAVBAR ── -->
<nav class="navbar">
  <div class="navbar-content">
    <a href="index.html" class="navbar-logo">
      <span class="nl-a">A</span><span class="nl-u">u</span><span class="nl-l">l</span><span class="nl-a">a</span><span class="nl-s">s</span>
      <span class="nl-gray"> en </span>
      <span class="nl-r">R</span><span class="nl-c">e</span><span class="nl-gray">-</span><span class="nl-a">C</span><span class="nl-u">o</span><span class="nl-l">n</span><span class="nl-s">e</span><span class="nl-r">x</span><span class="nl-c">i</span><span class="nl-a">ó</span><span class="nl-u">n</span>
    </a>
    <ul class="navbar-nav">
      <li><a href="index.html">Inicio</a></li>
      <li><a href="resumen.html">Resumen</a></li>
      <li><a href="timeline.html">Línea de Tiempo</a></li>
      <li><a href="sesion1.html">Sesión 1</a></li>
      <li><a href="sesion2.html">Sesión 2</a></li>
      <li><a href="sesion3.html">Sesión 3</a></li>
      <li><a href="sesion4.html">Sesión 4</a></li>
      <li><a href="monitoreo.html" class="active">Monitoreo</a></li>
    </ul>
  </div>
</nav>

<!-- ── PAGE HERO ── -->
<section class="page-hero">
  <p class="page-hero-label">Proyecto Violencia en Escuelas · PSE · SED Bogotá</p>
  <h1 class="page-hero-title">Progreso de Implementación — Ronda 3</h1>
  <p class="page-hero-sub">Monitoreo de sesiones por aula · Equipo facilitador · Abril–Junio 2026</p>
  <button class="refresh-btn" id="refreshBtn" onclick="triggerUpdate()">
    <span id="refreshIcon">↻</span> Actualizar datos
  </button>
  <span class="refresh-status" id="refreshStatus"></span>
  <div class="rainbow-divider"></div>
</section>

<!-- ── MAIN CONTENT ── -->
<div class="wrap">

  <!-- STATS ROW -->
  <div class="stats-row">
    <div class="stat-box s-dark">
      <div class="stat-num">{total_cls}</div>
      <div class="stat-lbl">Aulas seleccionadas</div>
    </div>
    <div class="stat-box s-verde">
      <div class="stat-num">{total_completadas}</div>
      <div class="stat-lbl">Sesiones completadas</div>
    </div>
    <div class="stat-box s-azul">
      <div class="stat-num">{total_agendadas}</div>
      <div class="stat-lbl">Sesiones agendadas</div>
    </div>
    <div class="stat-box">
      <div class="stat-num" style="color:var(--muted);">{total_pending}</div>
      <div class="stat-lbl">Por agendar</div>
    </div>
    <div class="stat-box s-verde">
      <div class="stat-num">{started}</div>
      <div class="stat-lbl">Aulas iniciadas</div>
    </div>
    <div class="stat-box s-verde">
      <div class="stat-num">{full_done}</div>
      <div class="stat-lbl">Aulas finalizadas</div>
    </div>
    <div class="updated-tag">Actualizado: {generated}</div>
  </div>

  <!-- OVERALL PROGRESS -->
  <div class="progress-block">
    <span class="pb-label">Progreso global</span>
    <div class="pb-track">
      <div class="pb-fill-c" style="width:{overall_pct}%;"></div>
      <div class="pb-fill-a" style="width:{pct_agendadas}%;"></div>
    </div>
    <span class="pb-pct">{overall_pct}% completado</span>
    <div class="pb-legend">
      <span><span class="pb-dot" style="background:var(--verde);"></span>Completada</span>
      <span><span class="pb-dot" style="background:var(--azul);opacity:0.7;"></span>Agendada</span>
      <span><span class="pb-dot" style="background:#e5e7eb;"></span>Por agendar</span>
    </div>
  </div>

  <!-- SESSION PANELS -->
  <div class="section-card">
    <div class="sc-body">
      <h3 class="sc-title">Avance por sesión</h3>
      <div class="session-panels">
        {session_panels_html}
      </div>
    </div>
  </div>

  <!-- CALENDAR -->
  <div class="section-card">
    <div class="sc-body">
      <h3 class="sc-title">Calendario del equipo — Abril · Mayo · Junio 2026</h3>
      <div class="legend-row" style="margin-bottom:10px;">
        {session_legend_html}
      </div>
      <div class="legend-row" style="padding-top:10px;border-top:1px solid var(--line);margin-bottom:20px;">
        <span style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:1px;align-self:center;white-space:nowrap;margin-right:4px;">Dupla:</span>
        {dupla_legend_html}
      </div>
      <div class="cal-months">
        {cal_html}
      </div>
    </div>
  </div>

  <!-- FACILITATOR TABLE -->
  <div class="section-card">
    <div class="sc-body">
      <h3 class="sc-title">Avance por gestor/a o dupla</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>Gestor(a) / Dupla</th>
            <th class="tc">Aulas</th>
            <th class="tc">✓ Comp.</th>
            <th class="tc">📅 Agend.</th>
            <th class="tc">○ Pend.</th>
            <th style="min-width:160px;">% completado</th>
          </tr>
        </thead>
        <tbody>{gestor_table_rows}</tbody>
      </table>
    </div>
  </div>

  <!-- SUMMARY TABLE -->
  <div class="section-card">
    <div class="sc-body">
      <h3 class="sc-title">Resumen por aula</h3>
      <div style="overflow-x:auto;">
        <table class="data-table">
          <thead>
            <tr>
              <th class="tc">#</th>
              <th>Colegio</th>
              <th>Localidad</th>
              <th class="tc">Aula</th>
              <th>Dupla</th>
              <th>S0 · S1 · S2 · S3 · S4</th>
              <th class="tc">Prog.</th>
            </tr>
          </thead>
          <tbody>{summary_table_rows}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- SCHOOL CARDS -->
  <div>
    <h3 style="font-family:'Nunito',sans-serif;font-weight:800;font-size:18px;color:var(--dark);margin-bottom:16px;">
      Detalle por aula
    </h3>
    <div style="display:flex;flex-direction:column;gap:16px;">
      {all_cards_html}
    </div>
  </div>

</div><!-- /.wrap -->

<!-- ── FOOTER (identical to site) ── -->
<footer>
  <div class="footer-content">
    <div class="footer-logo">
      <span class="fl-a">A</span><span class="fl-u">u</span><span class="fl-l">l</span><span class="fl-a">a</span><span class="fl-s">s</span>
      <span class="fl-gray"> en </span>
      <span class="fl-r">R</span><span class="fl-c">e</span><span class="fl-gray">-</span><span class="fl-a">C</span><span class="fl-u">o</span><span class="fl-l">n</span><span class="fl-s">e</span><span class="fl-r">x</span><span class="fl-c">i</span><span class="fl-a">ó</span><span class="fl-u">n</span>
    </div>
    <p class="footer-tagline">"Cada día es una oportunidad de ser el ambiente que queremos."</p>
    <div class="footer-meta">
      <p>Programa de Prácticas Restaurativas para Escuelas en Bogotá, Colombia</p>
      <p>En asociación con la Secretaría de Educación de Bogotá</p>
      <p>Paris School of Economics · 2026</p>
    </div>
  </div>
</footer>

<script>
  const REPO  = 'oscarmdiazb/aulasenreconexion';
  const WF    = 'update-dashboard.yml';
  const BRANCH = 'main';

  function getToken() {{
    let token = localStorage.getItem('gh_pat');
    if (!token) {{
      token = prompt(
        'Ingresa tu GitHub Personal Access Token (scope: workflow).\n' +
        'Se guardará en este navegador y no se enviará a ningún servidor externo.'
      );
      if (token) localStorage.setItem('gh_pat', token.trim());
    }}
    return token ? token.trim() : null;
  }}

  async function triggerUpdate() {{
    const btn    = document.getElementById('refreshBtn');
    const icon   = document.getElementById('refreshIcon');
    const status = document.getElementById('refreshStatus');

    const token = getToken();
    if (!token) {{
      status.textContent = 'Se necesita un token para actualizar.';
      status.className = 'refresh-status err';
      return;
    }}

    btn.disabled = true;
    icon.textContent = '↻';
    icon.className = 'spin';
    status.textContent = 'Disparando actualización…';
    status.className = 'refresh-status';

    try {{
      const res = await fetch(
        `https://api.github.com/repos/${{REPO}}/actions/workflows/${{WF}}/dispatches`,
        {{
          method: 'POST',
          headers: {{
            'Authorization': `Bearer ${{token}}`,
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json',
          }},
          body: JSON.stringify({{ ref: BRANCH }}),
        }}
      );

      if (res.status === 204) {{
        icon.className = '';
        icon.textContent = '✓';
        status.textContent = 'Actualización iniciada. La página se recargará en ~45 segundos.';
        status.className = 'refresh-status ok';
        setTimeout(() => location.reload(), 47000);
      }} else if (res.status === 401) {{
        localStorage.removeItem('gh_pat');
        icon.className = '';
        icon.textContent = '↻';
        status.textContent = 'Token inválido o expirado. Haz clic para intentar de nuevo.';
        status.className = 'refresh-status err';
        btn.disabled = false;
      }} else {{
        const body = await res.json().catch(() => ({{}}));
        icon.className = '';
        icon.textContent = '↻';
        status.textContent = `Error ${{res.status}}: ${{body.message || 'intenta de nuevo'}}`;
        status.className = 'refresh-status err';
        btn.disabled = false;
      }}
    }} catch (e) {{
      icon.className = '';
      icon.textContent = '↻';
      status.textContent = 'No se pudo conectar. Verifica tu conexión.';
      status.className = 'refresh-status err';
      btn.disabled = false;
    }}
  }}
</script>
</body>
</html>"""

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------
with open(SITE_OUTPUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Dashboard generado: {SITE_OUTPUT}")
print(f"  Aulas:                {total_cls}")
print(f"  Sesiones completadas: {total_completadas}/{total_sessions} ({overall_pct}%)")
print(f"  Sesiones agendadas:   {total_agendadas}")
print(f"  Por agendar:          {total_pending}")
print(f"  Aulas iniciadas:      {started}")
print(f"  Aulas finalizadas:    {full_done}")

# webbrowser.open disabled in CI
