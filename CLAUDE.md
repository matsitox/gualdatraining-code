# CLAUDE.md — Gualda Training Ads Dashboard

> Este archivo es leído automáticamente por Claude Code al abrir el proyecto.
> Contiene TODO el contexto necesario para trabajar sin preguntas previas.

---

## Regla de Git — SIEMPRE hacer push después de cada cambio

**Cada vez que se realice cualquier cambio en este repositorio, hacer commit y push a GitHub de forma automática.**

- Repo: `https://github.com/matsitox/gualdatraining-code`
- Rama: `main`
- Nunca afectar otros repositorios de la cuenta `matsitox`
- Si se aprende algo nuevo en la sesión (decisión de negocio, dato nuevo, configuración), anotarlo en la sección "Aprendizajes y Notas de Sesiones" del `README.md` y hacer push también.

---

## ¿Qué es este proyecto?

Dashboard de análisis de campañas **Meta Ads** de **Gualda Training** (empresa de cursos fitness online, Argentina). El output es un **sitio web estático de 3 páginas HTML** hosteado en Netlify: https://gualdatraining-ads.netlify.app

El objetivo del análisis es decidir la **estrategia de push de WhatsApp** para cada mes. Junio 2026 = mes de baja conversión, foco en campañas de cadencia corta (≤ 15 días) y recontacto vía plantillas de WhatsApp a leads con interés previo.

---

## Estructura del repo

```
github/
├── CLAUDE.md              ← este archivo
├── README.md
├── .gitignore
├── web/                   ← los 3 HTML listos para Netlify
│   ├── index.html                  (Push de Campañas)
│   ├── push_plantillas.html        (Rendimiento de Plantillas)
│   └── proyeccion_presupuesto.html (Calculadora de Presupuesto)
├── scripts/
│   └── gen_push_plantillas.py     ← regenera push_plantillas.html desde CSVs
├── data/                  ← gitignoreado (datos privados, copiar manualmente)
│   ├── plantillas_analytics_2026.csv
│   └── leads/
│       ├── enero.csv … mayo.csv
│       └── leads_preparados.json
└── docs/
    ├── CONTEXTO_PROYECTO_GT_traspaso.md   ← contexto histórico completo
    └── Gualda Training INFO.md            ← info de la empresa
```

**Deploy:** subir `web/` a Netlify (drag & drop o via CLI). Los 3 HTMLs son autocontenidos (imágenes embebidas en base64, sin dependencias externas).

---

## Las 3 páginas del sitio

### 1. `web/index.html` — Push de Campañas
Análisis de las 10 campañas de Meta Ads activas. Muestra por campaña:
- ROAS, Revenue, Inversión c/IVA, Ventas, Cadencia (% mismo mes + días promedio)
- Road touchpoint: de qué mes vino cada venta
- Cursos top vendidos
- Recomendación: PUSH / CON CUIDADO / NO ESCALAR / REACTIVAR
- Tabla comparativa clickeable con desglose mensual

### 2. `web/push_plantillas.html` — Rendimiento de Plantillas
Dos tabs:
- **Tab 1 — Rendimiento**: Revenue total de plantillas Mar–May 2026 ($110.9M ARS, 621 ventas, 211 plantillas), gráfico mensual, top 10 plantillas con revenue/ventas/países/productos/meses
- **Tab 2 — Campañas Recomendadas**: funnel de leads por campaña (Baja→Malos→Neutros→Buenos→Mostró Interés con porcentajes), tarjetas por campaña, cuadro de cruce campaña×plantilla

**Regenerar esta página:** `python3 scripts/gen_push_plantillas.py`  
(requiere `data/plantillas_analytics_2026.csv` y `data/leads/*.csv`)

### 3. `web/proyeccion_presupuesto.html` — Calculadora de Presupuesto
Calculadora interactiva: dado un presupuesto P y tiempo T días, proyecta Revenue/Ventas/Consultas por campaña usando modelo de maduración exponencial (`1 - e^(-T/cadencia_media)`). Entrada en ARS. FX 1.200 ARS/USD por defecto para presets en USD.

---

## Las 10 campañas (datos hardcodeados en el HTML)

| Campaña | Slug | Revenue | Inv c/IVA | ROAS | Ventas | Cad.días | Reco |
|---------|------|---------|-----------|------|--------|----------|------|
| APIWPP ArgLatam | mt_prospec_apiwpp_arglatam_wpp | $15.540.796 | $10.859.854 | 1.43x | 150 | ~10 | PUSH |
| Carrousel Exitoso ARG | mt_prospec_carrouselexitoso_arg_wpp | $10.512.239 | $5.028.750 | 2.09x | 89 | ~31 | CON CUIDADO |
| Oferta Flash ARG | mt_prospec_ofertaflash_arg_wpp | $4.777.416 | $2.438.690 | 1.96x | 47 | ~59 | NO ESCALAR |
| Mensajes ARG | mt_prospec_mensajes_arg_wpp | $3.289.375 | $3.028.918 | 1.09x | 24 | ~7 | PUSH |
| Oferta Flash MEX | mt_prospec_ofertaflash_mex_wpp | $2.637.797 | $1.800.000 | 1.47x | 16 | ~19 | REACTIVAR |
| Buyers ARG | mt_prospec_buyers_arg_venta | $2.359.916 | $3.925.980 | 0.60x | 14 | ~19 | NO ESCALAR |
| APIWPP LATAM Venta | mt_prospec_apiwpp_latam_venta | $1.899.921 | $1.522.400 | 1.25x | 10 | ~15 | NO ESCALAR |
| Mensajes URU | mt_prospec_mensajes_uru_wpp | $497.039 | $948.012 | 0.52x | 3 | ~0 | NO ESCALAR |
| Remark ArgLatam | mt_remark_mensajes_arglatam_wpp | $42.554 | $687.305 | 0.06x | 2 | ~0 | NO ESCALAR |
| Remark MEX | mt_remark_mensajes_mex_wpp | $0 | $386.100 | 0.00x | 0 | N/D | NO ESCALAR |

**GLOBAL:** Revenue $41.557.053 · Inversión $30.626.009 · ROAS 1.36x · 355 ventas  
**Ventana:** Mar–May 2026 para todas. Excepción: Oferta Flash MEX = Ene–Mar 2026 (apagada desde abril).  
Todo en **ARS**. ROAS = Revenue ÷ Inversión **con IVA**.

---

## Funnel de leads por campaña

Clasificación post-baja. **Prioridad exclusiva (de peor a mejor):**
`Baja > Malos > Neutros > Buenos > Mostró Interés`

Un lead solo puede estar en UNA categoría. Si tiene etiqueta "mostro interes" → sale de buenos/neutros/malos y va a Mostró Interés.

### Leads con "baja" (excluidos del conteo activo)
Tags que marcan baja: `presencial`, `lead mala calidad`, `seña/cuota`, `venta crm ok`

### Counts actuales (Mar–May 2026; MEX Ene–Mar)

| Campaña | Total | Baja | Malos | Neutros | Buenos | Mostró Interés |
|---------|-------|------|-------|---------|--------|----------------|
| Carrousel Exitoso ARG | 3.710 | 200 | 1 | 1.622 | 1.103 | 784 |
| Oferta Flash ARG | 3.643 | 245 | 3 | 2.124 | 801 | 470 |
| Mensajes ARG | 2.498 | 160 | 7 | 1.502 | 426 | 403 |
| APIWPP ArgLatam | 1.254 | 124 | 2 | 463 | 293 | 372 |
| Oferta Flash MEX | 1.043 | 54 | 3 | 653 | 219 | 114 |
| Mensajes URU | 272 | 20 | 1 | 146 | 52 | 53 |
| Remark ArgLatam | 255 | 19 | 0 | 146 | 48 | 42 |
| Buyers ARG | 170 | 15 | 0 | 105 | 25 | 25 |
| APIWPP LATAM Venta | 285 | 18 | 0 | 125 | 68 | 74 |
| Remark MEX | 113 | 3 | 0 | 77 | 16 | 17 |

**Totales del sistema (todos los leads, 5 meses):**
- Mostró Interés: 14.857
- Buenos: 20.344
- Neutros: 29.976
- Malos: 65
- Baja: 5.979

---

## Plantillas analytics — datos de `data/plantillas_analytics_2026.csv`

- Cada fila = 1 touchpoint de una venta (atribución multi-touch lineal)
- Filtro plantillas: `source_category` ∈ `["Templates", "Fuente para identificar conversaciones iniciadas con mensaje de plantilla de Meta"]`
- **Usar columna `revenue_linear`** (NO `Revenue` — está inflada para ventas USD)
- **Conversión de moneda:** ARS → directo; USD con `total_amount < 5.000` → × 1.200; USD con `total_amount ≥ 5.000` → tratar como ARS (outlier mal etiquetado)
- Ventana: Mar–May 2026 → 2.915 filas → 621 ventas únicas → $110.877.285 ARS

### Top 10 plantillas por revenue (Mar–May 2026)

| Plantilla | Revenue | Ventas |
|-----------|---------|--------|
| 2dainsist_oct | $16.847.296 | 298 |
| cc_template_20250804010523 | $15.609.865 | 249 |
| param_holainfo | $10.041.466 | 112 |
| clientenoseinscribe_may_2025 | $7.465.017 | 210 |
| manotazo_d | $6.225.687 | 173 |
| lead_magnet | $3.598.164 | 116 |
| instr_febars | $2.632.130 | 77 |
| ulths_packweek26 | $1.887.030 | 48 |
| seg_esp_agente | $1.803.223 | 41 |
| ptim_febars | $1.793.038 | 20 |

---

## Diseño visual del sitio

- **Fondo:** gradiente horizontal `#111624` (izq ~58%) → `#29021b` (der)
- **Barra top:** gradiente `#6001e2 → #ea0849` (4px, fixed)
- **Acento rosa:** `#fe006b` · Acento violeta: `#712fd1`
- **Cards:** `#111827` / `#0f172a` con bordes `#1f2937`
- **Loader:** logo GT latiendo con CSS puro (~0.95s) sobre overlay; luego fade-in
- **Imágenes:** todas embebidas en base64 dentro del HTML (sin archivos externos)
- **Clase `.grad-text`:** `background: linear-gradient(90deg, #fe006b, #712fd1); -webkit-background-clip: text`
- **Clase `.container`:** `max-width: 1200px; margin: 0 auto; padding: 0 20px`

---

## Flujo de trabajo estándar

1. **Editar datos** → modificar las constantes en `scripts/gen_push_plantillas.py`
2. **Regenerar página** → `python3 scripts/gen_push_plantillas.py`  
   (el script lee el HTML existente para extraer `<head>` + loader + logo base64, y reemplaza el body con contenido nuevo)
3. **Verificar** → abrir `web/push_plantillas.html` en el browser
4. **Deploy** → subir carpeta `web/` a Netlify (drag & drop en app.netlify.com)

Para `index.html` y `proyeccion_presupuesto.html` no hay script de generación — se editan directamente.

---

## Notas de negocio importantes

- **Junio = mes de baja conversión** → priorizar campañas con cadencia ≤ 15 días
- **ROAS incluye IVA** en la inversión (columna Budget del CSV de presupuestos = Monthly + Tax)
- **Buyers ARG** es venta web, no WhatsApp — su funnel de leads es casi inexistente (2 leads en el CSV)
- **Oferta Flash MEX** está apagada desde abril → si se reactiva hay que actualizar la ventana
- **WhatsApp default** (~$54.8M, 348 ventas sin atribución) no está incluido en los números — los ROAS reales son 1.5–2x mayores. Solución pendiente: configurar `ctwa_clid` en Chatty
- **Oferta Flash ARG mayo:** gasto estimado $819.950 (bug Días=0 en CSV de presupuestos)
- **Buyers ARG:** +$865.787 de 3 ventas CRM no atribuidas por Meta (ya incluido en los $2.359.916)
