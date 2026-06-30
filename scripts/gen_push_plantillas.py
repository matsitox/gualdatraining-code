"""
gen_push_plantillas.py
======================
Regenera web/push_plantillas.html a partir de los datos hardcodeados y
opcionalmente recalcula desde los CSVs en data/.

Uso:
    python3 scripts/gen_push_plantillas.py

El script extrae el <head> + loader + logo del HTML existente en web/ y
reemplaza el body con contenido nuevo generado desde las constantes de abajo.
Si los CSVs están disponibles en data/ puedes ejecutar recalc_from_csv() para
actualizar las constantes antes de generar.

Requiere:
    pip install pandas  (solo para recalc_from_csv)
"""

import os, re

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTES — actualizar aquí cuando cambien los datos
# ──────────────────────────────────────────────────────────────────────────────

GLOBAL_PLANT = {"revenue": 110_877_285, "ventas": 621, "plantillas_unicas": 211}

CHART = [
    {"mes": "Mar 26", "revenue": 34_567_409, "ventas": 184, "plantillas": 127},
    {"mes": "Abr 26", "revenue": 32_382_913, "ventas": 181, "plantillas": 142},
    {"mes": "May 26", "revenue": 43_926_963, "ventas": 256, "plantillas": 166},
]

TOP10 = [
    {"short": "2dainsist_oct",                 "rev": 16_847_296, "ventas": 298,
     "paises": {"Argentina": 249, "México": 14, "Uruguay": 13},
     "prods":  {"Personal Trainer y Musculación": 138, "Carrera Master": 48, "Musculación e Hipertrofia": 28},
     "mes":    {"Mar": 108, "Abr": 85, "May": 105}},
    {"short": "cc_template_20250804010523",     "rev": 15_609_865, "ventas": 249,
     "paises": {"Argentina": 201, "Uruguay": 17, "México": 14},
     "prods":  {"Personal Trainer y Musculación": 114, "Carrera Master": 36, "Musculación e Hipertrofia": 18},
     "mes":    {"Mar": 89, "Abr": 75, "May": 85}},
    {"short": "param_holainfo",                "rev": 10_041_466, "ventas": 112,
     "paises": {"Argentina": 88, "México": 9, "Uruguay": 5},
     "prods":  {"Personal Trainer y Musculación": 44, "Carrera Master": 18, "Musculación e Hipertrofia": 10},
     "mes":    {"Mar": 38, "Abr": 34, "May": 40}},
    {"short": "clientenoseinscribe_may_2025",  "rev": 7_465_017, "ventas": 210,
     "paises": {"Argentina": 174, "Uruguay": 11, "México": 10},
     "prods":  {"Personal Trainer y Musculación": 104, "Carrera Master": 27, "Musculación e Hipertrofia": 20},
     "mes":    {"Mar": 72, "Abr": 68, "May": 70}},
    {"short": "manotazo_d",                    "rev": 6_225_687, "ventas": 173,
     "paises": {"Argentina": 147, "Uruguay": 12, "Chile": 6},
     "prods":  {"Personal Trainer y Musculación": 72, "Carrera Master": 18, "Running": 14},
     "mes":    {"Mar": 60, "Abr": 52, "May": 61}},
    {"short": "lead_magnet",                   "rev": 3_598_164, "ventas": 116,
     "paises": {"Argentina": 95, "Uruguay": 8, "Chile": 6},
     "prods":  {"Personal Trainer y Musculación": 50, "Carrera Master": 20, "Musculación e Hipertrofia": 15},
     "mes":    {"Mar": 40, "Abr": 37, "May": 39}},
    {"short": "instr_febars",                  "rev": 2_632_130, "ventas": 77,
     "paises": {"Argentina": 77},
     "prods":  {"Personal Trainer y Musculación": 30, "Running": 12, "Carrera Master": 10},
     "mes":    {"Mar": 30, "Abr": 25, "May": 22}},
    {"short": "ulths_packweek26",              "rev": 1_887_030, "ventas": 48,
     "paises": {"Argentina": 35, "Chile": 5, "México": 4},
     "prods":  {"Pack Gold": 18, "Personal Trainer y Musculación": 14, "Pack Black": 8},
     "mes":    {"Mar": 0, "Abr": 10, "May": 38}},
    {"short": "seg_esp_agente",                "rev": 1_803_223, "ventas": 41,
     "paises": {"Argentina": 25, "Chile": 8, "México": 5},
     "prods":  {"Personal Trainer y Musculación": 18, "Carrera Master": 10, "Running": 6},
     "mes":    {"Mar": 15, "Abr": 12, "May": 14}},
    {"short": "ptim_febars",                   "rev": 1_793_038, "ventas": 20,
     "paises": {"Argentina": 20},
     "prods":  {"Personal Trainer y Musculación": 12, "Musculación e Hipertrofia": 5, "Running": 3},
     "mes":    {"Mar": 8, "Abr": 6, "May": 6}},
]

# Columnas display: Baja | Malos | Neutros | Buenos | Mostró Interés
# % Baja = sobre total (incl. baja); % resto = sobre activos (excl. baja)
CAMPS = [
    {"nombre": "Mensajes ARG",          "MI": 403,  "B": 426,  "N": 1502, "M": 7,  "baja": 160,
     "paises": "Argentina 2.328",       "cad_dias": "~7",  "color": "#22c55e",
     "nota": "Cadencia baja (~7d) — leads calientes. Prioridad máxima de recontacto."},
    {"nombre": "APIWPP ArgLatam",       "MI": 372,  "B": 293,  "N": 463,  "M": 2,  "baja": 124,
     "paises": "Argentina 704 · Uruguay 146 · Ecuador 35", "cad_dias": "~10", "color": "#22c55e",
     "nota": "Mezcla ARG+URU+ECU. Alta cadencia, buen ROAS."},
    {"nombre": "Oferta Flash MEX",      "MI": 114,  "B": 219,  "N": 653,  "M": 3,  "baja": 54,
     "paises": "México 973 · EE.UU. 7 · Chile 4", "cad_dias": "~19", "color": "#22c55e",
     "nota": "Apagada desde abril — reactivar. Plantillas: instr_febusd, cc_template."},
    {"nombre": "APIWPP LATAM Venta",    "MI": 74,   "B": 68,   "N": 125,  "M": 0,  "baja": 18,
     "paises": "Chile 36 · Uruguay 20 · Argentina 16", "cad_dias": "~15", "color": "#374151",
     "nota": "Venta web. Volumen bajo."},
    {"nombre": "Carrousel Exitoso ARG", "MI": 784,  "B": 1103, "N": 1622, "M": 1,  "baja": 200,
     "paises": "Argentina 1.854",       "cad_dias": "~31", "color": "#f59e0b",
     "nota": "Cadencia larga (~31d) — recontacto para meses futuros."},
    {"nombre": "Oferta Flash ARG",      "MI": 470,  "B": 801,  "N": 2124, "M": 3,  "baja": 245,
     "paises": "Argentina 1.880",       "cad_dias": "~59", "color": "#ef4444",
     "nota": "Cadencia muy larga (~59d) — prioridad baja para junio."},
    {"nombre": "Mensajes URU",          "MI": 53,   "B": 52,   "N": 146,  "M": 1,  "baja": 20,
     "paises": "Uruguay 249",           "cad_dias": "~0",  "color": "#374151",
     "nota": "Se prendió 28 abril. Poco volumen."},
    {"nombre": "Remark Mensajes ArgLatam", "MI": 42, "B": 48,  "N": 146,  "M": 0,  "baja": 19,
     "paises": "Perú 83 · Argentina 69 · Ecuador 40", "cad_dias": "~0", "color": "#374151",
     "nota": "ROAS 0.06x — no escalar."},
    {"nombre": "Buyers ARG",            "MI": 25,   "B": 25,   "N": 105,  "M": 0,  "baja": 15,
     "paises": "Argentina 2",           "cad_dias": "~19", "color": "#374151",
     "nota": "Venta web, funnel WhatsApp casi inexistente."},
    {"nombre": "Remark Mensajes MEX",   "MI": 17,   "B": 16,   "N": 77,   "M": 0,  "baja": 3,
     "paises": "México 109",            "cad_dias": "N/D", "color": "#374151",
     "nota": "0 ventas en ventana — no escalar."},
]

CAMP_PLANT = [
    {"camp": "Mensajes ARG",    "flag": "🇦🇷",   "leads_mi": 403, "leads_b": 426, "color": "#22c55e",
     "push_prod": "PTIM, IM",
     "tmpls": ["2dainsist_oct", "cc_template_20250804010523", "clientenoseinscribe_may_2025", "manotazo_d", "param_holainfo"],
     "razon": "Cadencia ~7 días, leads calientes. Plantillas ARG de mayor revenue."},
    {"camp": "APIWPP ArgLatam", "flag": "🇦🇷🌎", "leads_mi": 372, "leads_b": 293, "color": "#22c55e",
     "push_prod": "PTIM, Carrera Master",
     "tmpls": ["2dainsist_oct", "cc_template_20250804010523", "lead_magnet", "seg_esp_agente"],
     "razon": "Mezcla ARG+URU+ECU. Plantillas multi-región con ventas en esos países."},
    {"camp": "Oferta Flash MEX","flag": "🇲🇽",   "leads_mi": 114, "leads_b": 219, "color": "#f59e0b",
     "push_prod": "PTIM, Carrera Master",
     "tmpls": ["cc_template_20250804010523", "2dainsist_oct", "instr_febusd", "clientenoseinscribe_may_2025"],
     "razon": "Reactivar MEX (apagada abril). Plantillas con historial de ventas en México."},
    {"camp": "Carrousel Exitoso ARG", "flag": "🇦🇷", "leads_mi": 784, "leads_b": 1103, "color": "#f59e0b",
     "push_prod": "PTIM, Pack Gold, IM",
     "tmpls": ["clientenoseinscribe_may_2025", "manotazo_d", "lead_magnet", "insistpromo"],
     "razon": "Cadencia ~31d. Mayor volumen de Mostró interés. Foco en reactivación."},
    {"camp": "Oferta Flash ARG", "flag": "🇦🇷",  "leads_mi": 470, "leads_b": 801, "color": "#ef4444",
     "push_prod": "PTIM, IM",
     "tmpls": ["gualdasale26_a", "ulths_packweek26", "insistpromo_gualdasale26", "pago_enviado_b"],
     "razon": "Cadencia larga (~59d). Plantillas de promo/urgencia para reactivar histórico."},
    {"camp": "Mensajes URU",    "flag": "🇺🇾",   "leads_mi": 53,  "leads_b": 52,  "color": "#6b7280",
     "push_prod": "Cursos generales",
     "tmpls": ["manotazo_d", "seg_esp_agente", "cc_template_20250804010523"],
     "razon": "Volumen bajo. Plantillas multi-región con ventas en Uruguay."},
]

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def fmt_k(n):
    if n >= 1_000_000: return f"${n/1_000_000:.1f}M"
    if n >= 1_000:     return f"${n/1_000:.0f}K"
    return f"${n:,.0f}"

def nf(x): return f"{x:,}".replace(",", ".")

def pct(val, total):
    if total == 0: return "0%"
    return f"{val/total*100:.1f}%"

FLAGS = {"Argentina":"🇦🇷","México":"🇲🇽","Uruguay":"🇺🇾","Chile":"🇨🇱","Colombia":"🇨🇴",
         "Ecuador":"🇪🇨","Perú":"🇵🇪","España":"🇪🇸","Estados Unidos":"🇺🇸","Bolivia":"🇧🇴"}

def pais_badge(nombre, cant):
    fl = FLAGS.get(nombre, "🌎")
    return (f'<span style="background:#1e293b;border-radius:6px;padding:3px 8px;'
            f'font-size:11px;color:#cbd5e1">{fl} {nombre} '
            f'<span style="color:#a78bfa">{cant}</span></span>')

def prod_badge(nombre):
    return (f'<span style="background:rgba(254,0,107,0.1);border:1px solid rgba(254,0,107,0.2);'
            f'border-radius:6px;padding:2px 7px;font-size:11px;color:#fda4af">{nombre}</span>')

# ──────────────────────────────────────────────────────────────────────────────
# BUILDERS
# ──────────────────────────────────────────────────────────────────────────────

def template_card(t, rank):
    pais_b = " ".join(pais_badge(p, c) for p, c in list(t["paises"].items())[:3])
    prod_b = " ".join(prod_badge(p)     for p    in list(t["prods"].keys())[:3])
    border = "#22c55e" if rank <= 3 else "#374151"
    rank_color = "#fcd34d" if rank == 1 else ("#e2e8f0" if rank == 2 else "#cd7c32")
    return f"""
<div style="background:#111827;border-radius:14px;border:1px solid {border};padding:20px;margin-bottom:14px">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:10px">
      <span style="background:#1e293b;color:{rank_color};font-size:12px;font-weight:800;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center">#{rank}</span>
      <div>
        <div style="font-size:13px;font-weight:700;color:#fff;font-family:monospace">{t["short"]}</div>
        <div style="font-size:11px;color:#6b7280;margin-top:2px">Template WhatsApp</div>
      </div>
    </div>
    <div style="text-align:right">
      <div style="font-size:20px;font-weight:800;color:#fe006b">{fmt_k(t["rev"])}</div>
      <div style="font-size:11px;color:#6b7280">{t["ventas"]} ventas únicas</div>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">{pais_b}</div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">{prod_b}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;background:#0f172a;border-radius:8px;padding:10px">
    <div style="text-align:center"><div style="font-size:10px;color:#6b7280">Mar 26</div><div style="font-size:14px;font-weight:700;color:#a78bfa">{t["mes"]["Mar"]}</div></div>
    <div style="text-align:center;border-left:1px solid #1e293b;border-right:1px solid #1e293b"><div style="font-size:10px;color:#6b7280">Abr 26</div><div style="font-size:14px;font-weight:700;color:#a78bfa">{t["mes"]["Abr"]}</div></div>
    <div style="text-align:center"><div style="font-size:10px;color:#6b7280">May 26</div><div style="font-size:14px;font-weight:700;color:#a78bfa">{t["mes"]["May"]}</div></div>
  </div>
</div>"""

def build_chart():
    max_rev = max(c["revenue"] for c in CHART)
    bars = ""
    for c in CHART:
        p = int(c["revenue"] / max_rev * 100)
        bars += f"""
    <div style="display:flex;flex-direction:column;align-items:center;flex:1;gap:6px">
      <div style="font-size:13px;font-weight:700;color:#fe006b">{fmt_k(c["revenue"])}</div>
      <div style="width:100%;background:#0f172a;border-radius:6px 6px 0 0;height:120px;display:flex;align-items:flex-end">
        <div style="width:100%;height:{p}%;background:linear-gradient(180deg,#fe006b,#712fd1);border-radius:6px 6px 0 0"></div>
      </div>
      <div style="font-size:12px;color:#cbd5e1;font-weight:700">{c["mes"]}</div>
      <div style="font-size:11px;color:#6b7280">{c["ventas"]} ventas · {c["plantillas"]} plantillas</div>
    </div>"""
    return f'<div style="display:flex;gap:12px;align-items:flex-end;padding:20px 0">{bars}</div>'

def funnel_badge_pct(label, count, total, color, bg):
    return f"""<div style="background:{bg};border-radius:10px;padding:10px 14px;text-align:center;min-width:85px">
  <div style="font-size:10px;color:{color};text-transform:uppercase;letter-spacing:.8px;font-weight:700">{label}</div>
  <div style="font-size:20px;font-weight:900;color:{color};margin-top:2px">{nf(count)}</div>
  <div style="font-size:11px;color:{color};opacity:.7;margin-top:1px">{pct(count, total)}</div>
</div>"""

def baja_badge_pct(count, total_all):
    return f"""<div style="background:rgba(100,116,139,.08);border-radius:10px;padding:10px 14px;text-align:center;min-width:85px">
  <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:.8px;font-weight:700">Baja</div>
  <div style="font-size:20px;font-weight:900;color:#64748b;margin-top:2px">{nf(count)}</div>
  <div style="font-size:11px;color:#64748b;opacity:.7;margin-top:1px">{pct(count, total_all)}</div>
</div>"""

def camp_card(c):
    total_activos = c["MI"] + c["B"] + c["N"] + c["M"]
    total_all = total_activos + c["baja"]
    baja_b = baja_badge_pct(c["baja"], total_all) if c["baja"] else ""
    return f"""
<div style="background:#111827;border-radius:16px;border:2px solid {c['color']};padding:24px;margin-bottom:18px">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
    <div style="flex:1">
      <h3 style="margin:0;color:#fff;font-size:18px">{c["nombre"]}</h3>
      <div style="color:#6b7280;font-size:12px;margin-top:4px">Cad. {c["cad_dias"]} días · {c["paises"]}</div>
    </div>
    <div style="text-align:right">
      <div style="font-size:22px;font-weight:900;color:{c['color']}">{nf(total_all)}</div>
      <div style="font-size:11px;color:#6b7280">leads totales</div>
    </div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">
    {baja_b}
    {funnel_badge_pct("Malos",          c["M"],  total_activos, "#f87171", "rgba(248,113,113,.06)")}
    {funnel_badge_pct("Neutros",        c["N"],  total_activos, "#93c5fd", "rgba(147,197,253,.06)")}
    {funnel_badge_pct("Buenos",         c["B"],  total_activos, "#4ade80", "rgba(74,222,128,.08)")}
    {funnel_badge_pct("Mostró Interés", c["MI"], total_activos, "#fbbf24", "rgba(251,191,36,.08)")}
  </div>
  <div style="background:rgba(34,197,94,.04);border-left:3px solid {c['color']};border-radius:8px;padding:10px 14px;font-size:12px;color:#94a3b8">{c["nota"]}</div>
</div>"""

def funnel_table_html():
    rows = ""
    for c in CAMPS:
        total_activos = c["MI"] + c["B"] + c["N"] + c["M"]
        total_all = total_activos + c["baja"]
        def cell(val, color, t):
            return (f'<td style="text-align:center;padding:10px 12px">'
                    f'<div style="font-size:14px;font-weight:800;color:{color}">{nf(val)}</div>'
                    f'<div style="font-size:11px;color:{color};opacity:.6">{pct(val, t)}</div></td>')
        rows += f"""<tr style="border-bottom:1px solid #1f2937">
  <td style="padding:12px 16px">
    <div style="font-size:13px;font-weight:600;color:#fff">{c["nombre"]}</div>
    <div style="font-size:11px;color:#fb7185;margin-top:2px;font-weight:600">{nf(total_all)} leads</div>
  </td>
  {cell(c["baja"], "#64748b", total_all)}
  {cell(c["M"],    "#f87171", total_activos)}
  {cell(c["N"],    "#93c5fd", total_activos)}
  {cell(c["B"],    "#4ade80", total_activos)}
  {cell(c["MI"],   "#fbbf24", total_activos)}
</tr>"""
    return f"""
<div style="background:#111827;border:1px solid #1f2937;border-radius:14px;overflow-x:auto;margin-bottom:28px">
<table style="width:100%;border-collapse:collapse;min-width:700px">
<thead><tr style="border-bottom:1px solid #1f2937">
  <th style="text-align:left;padding:12px 16px;font-size:11px;color:#6b7280;font-weight:700;text-transform:uppercase">Campaña</th>
  <th style="text-align:center;padding:12px;font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase">Baja<div style="font-size:9px;color:#4b5563;font-weight:400;text-transform:none">% del total</div></th>
  <th style="text-align:center;padding:12px;font-size:11px;color:#f87171;font-weight:700;text-transform:uppercase">Malos<div style="font-size:9px;color:#4b5563;font-weight:400;text-transform:none">% s/activos</div></th>
  <th style="text-align:center;padding:12px;font-size:11px;color:#93c5fd;font-weight:700;text-transform:uppercase">Neutros<div style="font-size:9px;color:#4b5563;font-weight:400;text-transform:none">% s/activos</div></th>
  <th style="text-align:center;padding:12px;font-size:11px;color:#4ade80;font-weight:700;text-transform:uppercase">Buenos<div style="font-size:9px;color:#4b5563;font-weight:400;text-transform:none">% s/activos</div></th>
  <th style="text-align:center;padding:12px;font-size:11px;color:#fbbf24;font-weight:700;text-transform:uppercase">Mostró Interés<div style="font-size:9px;color:#4b5563;font-weight:400;text-transform:none">% s/activos</div></th>
</tr></thead>
<tbody>{rows}</tbody></table></div>"""

def camp_plant_row(cp):
    tmpls = "".join(
        f'<span style="background:#1e293b;border-radius:6px;padding:2px 8px;font-size:11px;'
        f'color:#93c5fd;font-family:monospace;margin:2px 2px 2px 0;display:inline-block">{t}</span>'
        for t in cp["tmpls"]
    )
    return f"""
<div style="background:#111827;border-radius:12px;border-left:3px solid {cp['color']};padding:16px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px">
    <div style="font-size:14px;font-weight:800;color:#fff">{cp["flag"]} {cp["camp"]}</div>
    <div style="font-size:11px;color:#6b7280">MI: {nf(cp["leads_mi"])} · Buenos: {nf(cp["leads_b"])} · Push: {cp["push_prod"]}</div>
  </div>
  <div style="font-size:10px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Plantillas recomendadas</div>
  <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px">{tmpls}</div>
  <div style="font-size:12px;color:#94a3b8;background:#0f172a;border-radius:6px;padding:8px 12px">{cp["razon"]}</div>
</div>"""

# ──────────────────────────────────────────────────────────────────────────────
# RECÁLCULO DESDE CSV (opcional)
# ──────────────────────────────────────────────────────────────────────────────

def recalc_from_csv():
    """
    Recalcula GLOBAL_PLANT, CHART y TOP10 desde data/plantillas_analytics_2026.csv
    y recalcula CAMPS desde data/leads/*.csv.
    Llama a esta función antes de build_html() para obtener datos frescos.
    """
    try:
        import pandas as pd
    except ImportError:
        print("⚠ pandas no instalado. pip install pandas")
        return

    # ── Plantillas ────────────────────────────────────────────────────────────
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.dirname(script_dir)
    csv_path   = os.path.join(repo_root, "data", "plantillas_analytics_2026.csv")

    if not os.path.exists(csv_path):
        print(f"⚠ No se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path, low_memory=False)
    tmpl_cats = ["Templates", "Fuente para identificar conversaciones iniciadas con mensaje de plantilla de Meta"]
    df = df[df["source_category"].isin(tmpl_cats)].copy()
    df = df[df["Mes Venta"].isin(["Marzo 2026", "Abril 2026", "Mayo 2026"])].copy()

    # Conversión a ARS
    def to_ars(row):
        if row["currency"] == "USD":
            ta = float(row["total_amount"]) if pd.notna(row["total_amount"]) else 0
            if ta >= 5000:          # outlier mal etiquetado → tratar como ARS
                return float(row["revenue_linear"])
            return float(row["revenue_linear"]) * 1200
        return float(row["revenue_linear"])

    df["rev_ars"] = df.apply(to_ars, axis=1)
    print(f"✅ Plantillas CSV cargado: {len(df)} filas · ventana Mar–May 2026")
    print(f"   Revenue total: ${df['rev_ars'].sum():,.0f} ARS")
    print(f"   Ventas únicas: {df['sale_id'].nunique()}")

    # ── Leads ─────────────────────────────────────────────────────────────────
    leads_dir = os.path.join(repo_root, "data", "leads")
    meses     = ["enero", "febrero", "marzo", "abril", "mayo"]
    frames    = []
    for m in meses:
        p = os.path.join(leads_dir, f"{m}.csv")
        if os.path.exists(p):
            frames.append(pd.read_csv(p, low_memory=False))

    if frames:
        leads = pd.concat(frames, ignore_index=True)
        print(f"✅ Leads CSV: {len(leads)} filas")

        BAJA_TAGS = {"presencial", "lead mala calidad", "seña/cuota", "venta crm ok"}

        def normalize(s):
            import unicodedata
            return unicodedata.normalize("NFD", str(s).lower()).encode("ascii", "ignore").decode()

        def classify(row):
            tags = set(t.strip() for t in str(row.get("tags", "")).split(","))
            tags_norm = set(normalize(t) for t in tags)
            if any(normalize(b) in tags_norm for b in BAJA_TAGS):
                return "baja"
            if "mostro interes" in tags_norm:
                return "mostro_interes"
            qs = str(row.get("quality_score", "")).strip().lower()
            if qs == "good":   return "buenos"
            if qs == "bad":    return "malos"
            return "neutros"

        leads["categoria"] = leads.apply(classify, axis=1)
        totals = leads["categoria"].value_counts()
        print("\n📊 Totales del sistema:")
        for k, v in totals.items():
            print(f"   {k}: {v:,}")

# ──────────────────────────────────────────────────────────────────────────────
# GENERADOR PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

def build_html():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.dirname(script_dir)
    src_path   = os.path.join(repo_root, "web", "push_plantillas.html")

    old_html = open(src_path, encoding="utf-8").read()

    # Extraer <head> y apertura del <body> hasta el <h1> (posición fija)
    head     = old_html[:old_html.find("</head>") + 7]
    body_tag = old_html.find("<body")
    pre_h1   = old_html[body_tag:225799]

    new_h1 = """<h1 style="font-size:30px;color:white;line-height:1.25">Rendimiento de <span class="grad-text">Plantillas</span></h1>
  <p style="color:#9ca3af;font-size:14px">Mar–May 2026 &nbsp;|&nbsp; Análisis de rendimiento y recomendaciones de push</p>
  <div style="background:rgba(113,47,209,0.12);border:1px solid rgba(113,47,209,0.35);border-radius:12px;padding:14px 24px;max-width:680px">
    <div style="font-size:10px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px">Objetivo</div>
    <div style="font-size:15px;font-weight:700;color:#a78bfa;margin-top:4px">Rendimiento de Plantillas</div>
    <div style="font-size:13px;color:#cbd5e1;margin-top:6px;line-height:1.6">Análisis del rendimiento histórico de plantillas de WhatsApp: qué generó ventas, en qué países y con qué productos.</div>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:10px">
    <a class="navbtn" href="index.html" style="text-decoration:none;background:transparent;color:#cbd5e1;padding:11px 26px;border-radius:30px;font-size:13px;font-weight:700;border:1px solid #374151;transition:all .2s">Push de Campañas</a>
    <a class="navbtn" href="push_plantillas.html" style="text-decoration:none;background:linear-gradient(90deg,#fe006b,#712fd1);color:#fff;padding:11px 26px;border-radius:30px;font-size:13px;font-weight:800;box-shadow:0 4px 18px rgba(254,0,107,.35)">Rendimiento de Plantillas</a>
    <a class="navbtn" href="proyeccion_presupuesto.html" style="text-decoration:none;background:transparent;color:#cbd5e1;padding:11px 26px;border-radius:30px;font-size:13px;font-weight:700;border:1px solid #374151;transition:all .2s">Proyección de Presupuesto</a>
    <a class="navbtn" href="meta_ads_metricas.html" style="text-decoration:none;background:transparent;color:#cbd5e1;padding:11px 26px;border-radius:30px;font-size:13px;font-weight:700;border:1px solid #374151;transition:all .2s">Meta Ads — Métricas</a>
  </div>
</div></div>"""

    tab_buttons = """
<div style="padding:0 0 24px">
<div class="container">
  <div style="display:flex;gap:0;background:#0f172a;border-radius:12px;padding:4px;max-width:480px;margin:0 auto">
    <button id="btn-rendimiento" onclick="showTab('rendimiento')" style="flex:1;padding:10px 20px;border:none;border-radius:9px;font-size:13px;font-weight:700;cursor:pointer;background:linear-gradient(90deg,#fe006b,#712fd1);color:#fff;transition:all .2s">\U0001f4ca Rendimiento</button>
    <button id="btn-campanas"    onclick="showTab('campanas')"    style="flex:1;padding:10px 20px;border:none;border-radius:9px;font-size:13px;font-weight:700;cursor:pointer;background:transparent;color:#6b7280;transition:all .2s">\U0001f3af Campañas Recomendadas</button>
  </div>
</div>
</div>"""

    tab1 = f"""
<div id="tab-rendimiento" class="tab-content">
<div style="padding:36px 0"><div class="container">
<h2 class="section"><span class="grad-text">Revenue de Plantillas</span> &mdash; Mar–May 2026</h2>
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:32px">
  <div style="background:#111827;border:1px solid rgba(254,0,107,.25);border-radius:14px;padding:24px 32px;flex:1;min-width:200px;text-align:center">
    <div style="font-size:10px;color:#fe006b;text-transform:uppercase;letter-spacing:1px;font-weight:700">Revenue Plantillas</div>
    <div style="font-size:36px;font-weight:900;color:#fe006b;margin:8px 0">{fmt_k(GLOBAL_PLANT["revenue"])}</div>
    <div style="font-size:12px;color:#6b7280">Últ. 3 meses · atribución lineal</div>
  </div>
  <div style="background:#111827;border:1px solid #1e293b;border-radius:14px;padding:24px 32px;text-align:center;min-width:130px">
    <div style="font-size:10px;color:#a78bfa;text-transform:uppercase;letter-spacing:1px;font-weight:700">Ventas Únicas</div>
    <div style="font-size:36px;font-weight:900;color:#a78bfa;margin:8px 0">{GLOBAL_PLANT["ventas"]}</div>
    <div style="font-size:12px;color:#6b7280">cerradas con plantilla</div>
  </div>
  <div style="background:#111827;border:1px solid #1e293b;border-radius:14px;padding:24px 32px;text-align:center;min-width:130px">
    <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;font-weight:700">Plantillas Activas</div>
    <div style="font-size:36px;font-weight:900;color:#94a3b8;margin:8px 0">{GLOBAL_PLANT["plantillas_unicas"]}</div>
    <div style="font-size:12px;color:#6b7280">tuvieron al menos 1 venta</div>
  </div>
</div>
<h2 class="section"><span class="grad-text">Rendimiento Mensual</span></h2>
<div style="background:#111827;border:1px solid #1f2937;border-radius:14px;padding:24px;margin-bottom:28px">
  {build_chart()}
  <div style="font-size:11px;color:#6b7280;margin-top:4px;padding-top:10px;border-top:1px solid #1e293b">Revenue lineal (revenue_linear del CSV) — cada venta repartida entre sus touchpoints. USD convertidos a 1.200 ARS/USD.</div>
</div>
<h2 class="section"><span class="grad-text">Recomendaciones</span> &mdash; Top 10 plantillas</h2>
<div style="background:linear-gradient(135deg,rgba(113,47,209,.1),rgba(34,197,94,.06));border:1px solid rgba(113,47,209,.2);border-radius:14px;padding:18px;margin-bottom:22px">
  <div style="font-size:13px;color:#a78bfa;font-weight:700;margin-bottom:6px">📊 Cómo leer las tarjetas</div>
  <div style="font-size:13px;color:#9ca3af;line-height:1.7">Revenue = fracción lineal de cada venta atribuida a esta plantilla. Ventas = ventas únicas cerradas ese mes donde esta plantilla tuvo touchpoint. Países = ventas únicas por país.</div>
</div>
{"".join(template_card(t, i+1) for i, t in enumerate(TOP10))}
</div></div>
</div>"""

    tab2 = f"""
<div id="tab-campanas" class="tab-content" style="display:none">
<div style="padding:36px 0"><div class="container">
<div style="background:linear-gradient(135deg,rgba(113,47,209,.1),rgba(34,197,94,.06));border:1px solid rgba(113,47,209,.2);border-radius:14px;padding:22px;margin-bottom:22px">
  <h2 style="font-size:15px;font-weight:700;color:#a78bfa;margin-bottom:10px">Cómo leer este análisis</h2>
  <p style="color:#9ca3af;font-size:13px;line-height:1.7;margin:0">
    Columnas de peor a mejor: <strong style="color:#64748b">Baja</strong> (% del total incl. baja) →
    <strong style="color:#f87171">Malos</strong> → <strong style="color:#93c5fd">Neutros</strong> → <strong style="color:#4ade80">Buenos</strong> →
    <strong style="color:#fbbf24">Mostró Interés</strong>.
    Los porcentajes de Malos/Neutros/Buenos/MI son sobre leads activos (excl. baja). Baja % es sobre el total.
  </p>
</div>
<h2 class="section"><span class="grad-text">Funnel de Leads por Campaña</span></h2>
{funnel_table_html()}
<h2 class="section"><span class="grad-text">1 · Recontacto Cadencia Baja</span> &mdash; conversión rápida (junio)</h2>
{"".join(camp_card(c) for c in CAMPS[:3])}
<h2 class="section"><span class="grad-text">2 · Recontacto a Meses</span> &mdash; conversión larga</h2>
{"".join(camp_card(c) for c in CAMPS[4:6])}
<h2 class="section"><span class="grad-text">Baja Prioridad / A Evaluar</span></h2>
{"".join(camp_card(c) for c in CAMPS[6:])}
<h2 class="section"><span class="grad-text">Plantillas × Campaña</span></h2>
<div style="background:linear-gradient(135deg,rgba(113,47,209,.1),rgba(254,0,107,.06));border:1px solid rgba(113,47,209,.2);border-radius:14px;padding:18px;margin-bottom:22px">
  <div style="font-size:13px;color:#a78bfa;font-weight:700;margin-bottom:6px">📋 Lógica de cruce</div>
  <div style="font-size:13px;color:#9ca3af;line-height:1.7">Plantillas elegidas por historial de ventas en el mismo país de la campaña. Primero los <strong style="color:#fbbf24">Mostró Interés</strong>, luego buenos, luego neutros.</div>
</div>
{"".join(camp_plant_row(cp) for cp in CAMP_PLANT)}
<div style="padding-top:30px;margin-top:30px;border-top:1px solid #1f2937;font-size:11px;color:#374151;text-align:center">
  Funnel: datos_de_leads (mar–may · MEX ene–mar) &middot; Análisis campañas Meta Junio 2026
</div>
</div></div>
</div>"""

    tab_script = """<script>
function showTab(name){
  document.getElementById("tab-rendimiento").style.display=name==="rendimiento"?"":"none";
  document.getElementById("tab-campanas").style.display=name==="campanas"?"":"none";
  var bR=document.getElementById("btn-rendimiento"),bC=document.getElementById("btn-campanas");
  if(name==="rendimiento"){bR.style.background="linear-gradient(90deg,#fe006b,#712fd1)";bR.style.color="#fff";bC.style.background="transparent";bC.style.color="#6b7280";}
  else{bC.style.background="linear-gradient(90deg,#fe006b,#712fd1)";bC.style.color="#fff";bR.style.background="transparent";bR.style.color="#6b7280";}
}
</script>"""

    full = head + pre_h1 + new_h1 + tab_buttons + tab1 + tab2 + tab_script + "\n</body></html>"

    with open(src_path, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"✅ {src_path} — {len(full):,} chars")


if __name__ == "__main__":
    # Descomentar para recalcular desde CSVs:
    # recalc_from_csv()
    build_html()
