# Contexto del proyecto — Análisis de Campañas Meta de Gualda Training (GT)

> Documento de traspaso para continuar el trabajo en otro chat de IA. Contiene el contexto completo, las fuentes de datos, las definiciones, las decisiones tomadas, las métricas finales y lo que quedó pendiente. Todo el dinero está en **pesos argentinos (ARS)** salvo que se indique lo contrario.

---

## 1. Objetivo del proyecto

Análisis de campañas de **Meta Ads** de Gualda Training para decidir la estrategia de **Push de Junio 2026**. Premisa del negocio: **junio es un mes de baja conversión**, así que el objetivo es meter presupuesto en campañas con **cadencia baja** (convierten rápido, mismo mes) y **ROAS positivo**. Las campañas de embudo largo se trabajan con el equipo de CS vía **plantillas de WhatsApp** (recontacto).

Se construyó un sitio web (3 páginas HTML estáticas, autocontenidas) hospedado en **https://gualdatraining-ads.netlify.app**.

---

## 2. Ventana de análisis y períodos

- **Ventana general: Marzo, Abril y Mayo 2026** para todas las campañas.
- **Excepción — Oferta Flash MEX: Enero, Febrero y Marzo 2026** (solo estuvo activa en ese tramo; apagada desde abril).
- Mapa de períodos del CSV de presupuestos: **36 = enero 2026, 37 = feb, 38 = mar, 39 = abr, 40 = may, 41 = jun**. El histórico baja hasta "Antes 7/7/2023".

---

## 3. Fuentes de datos (rutas dentro de la carpeta del proyecto "Gualda Training (1)")

- **`campañas/revenue_de_todas_las_campañas.csv`** — Revenue por campaña y fecha (export de Analytics GT). Tiene **36 campañas distintas**; solo se usan las **10 que tienen carpeta de capturas**. Columnas: Campaña, Fecha ("4 de marzo"), Revenue.
- **`campañas/periodos-y-presupuestos.csv`** — Presupuestos diarios. Columnas clave: Período, Rango Tiempo, Tipo, **Campaña**, Conj. de anuncios, **Daily**, **Días**, **Monthly (=Daily×Días, sin IVA)**, **Tax (IVA)**, **Budget (=Monthly+Tax, con IVA)**, Status.
  - **Nombres duplicados dentro de un período** = (a) adsets distintos de la misma campaña, o (b) el mismo adset repetido por cambios de presupuesto diario (cada fila es un tramo con sus Días). Para la inversión de una campaña/mes **hay que sumar TODAS sus filas** en ese período.
  - Ojo: los montos usan coma de miles dentro de comillas (parsear con csv respetando comillas).
- **`campañas/anuncios-click-to-whatsapp/<campaña>/<mes>/`** y **`campañas/venta-web/<campaña>/<mes>/`** — Capturas (3 PNG por campaña/mes):
  - `foto_grafico.png` → revenue del mes + **gráfico "Ventas" por curso** (ranking de cursos vendidos) + touchpoints.
  - `ventas_por_anuncio_y_cadencia_total.png` → países (embudo) + ventas por anuncio + **"Road touchpoint for Sale"** (cadencia).
  - `cadencia_por_anuncio.png` → cadencia por anuncio.
- **`campañas/datos_de_leads/{enero..mayo}.csv`** — Leads de WhatsApp (los genera Chatty). Columnas usadas: **fecha_primer_contacto**, **pais**, **fuente_origen** (trae la campaña), **quality_score** (good/neutral/bad), **tags** (etiquetas). 71.221 filas totales.
- **`campañas/mt_prospec_buyers_arg_venta en CRM - Hoja 1.csv`** — 3 ventas web extra de Buyers no atribuidas por Meta (CRM).
- **`plantillas_analytics_2026.csv`** — TODAS las ventas (pauta + plantillas + todo) a lo largo de muchos meses (jun 2025 – jun 2026). Cada fila es un touchpoint de una venta. Se usa solo para **plantillas** (ver sección 9).
- **`Análisis Campañas Meta - Junio 2026/`** — Las 3 páginas HTML + imágenes (logo GT, logo Meta, favicon embebidos en base64).
- **`web_para_hostear/`** — Copia lista para deploy (página principal renombrada a `index.html` y links internos corregidos). **Hay que re-sincronizar esta carpeta cada vez que se edita el sitio.**
- **`Metodologia_Proyeccion_Presupuesto_GT.docx`** — Documento de metodología de la calculadora de proyección (incluye anexo de "WhatsApp default").

---

## 4. Definiciones clave (importantes para no malinterpretar)

- **Cadencia**: % de ventas que convierten **el mismo mes** del touchpoint (cuándo entró el lead vs. cuándo compró). Objetivo ≥70%. Mide qué tan rápido convierte la campaña. También se expresa como **cadencia media en días** (meses × 30).
- **Road Touchpoint for Sale**: las ventas **siempre se cuentan en el mes en que se cerró la venta**; el desglose indica **de qué mes vino el lead** (su touchpoint). Ej. "abril: mismo mes 25 · marzo 9" = en abril hubo 34 ventas, 25 de leads que entraron en abril y 9 de leads que entraron en marzo. En la web se muestran con el nombre exacto del mes (y año si es de un año anterior).
- **ROAS** = Revenue ÷ Inversión (con IVA).
- **Intermitencias**: días reales que corrió cada campaña cada mes (afecta la inversión y la interpretación). El CSV de presupuestos ya las refleja en la columna Días.

---

## 5. Decisiones tomadas (acordadas con el usuario)

1. **Inversión y ROAS con IVA incluido** (columna Budget del CSV de presupuestos).
2. **Ventana Mar–May** para todas; **Oferta Flash MEX Ene–Mar**.
3. **Las notas del usuario mandan** cuando el CSV y las fechas verbales no coinciden.
4. **Oferta Flash ARG — mayo:** la fila de presupuesto de mayo tenía **Días=0 (bug de carga)**, así que el gasto figuraba en $0 y el ROAS estaba inflado (2.95x). Se **estimó** el gasto de mayo en **$819.950** (daily $21.160 × 31 días × IVA) → ROAS corregido a **1.96x**.
5. **Buyers ARG:** se sumaron **3 ventas de CRM web** (+$865.787) que Meta no atribuyó. Marzo se re-incluyó (el CRM confirma actividad). ROAS pasó de 0.38x a **0.60x**.
6. **Sistema de leads — bajas:** los leads cuya columna **tags** contiene alguna de **`presencial`, `lead mala calidad`, `seña/cuota`, `venta crm ok`** se **dan de baja**: NO suman al total ni a buenos/neutros/malos. Se cuentan aparte como "gente de baja". (Al excluir "lead mala calidad", los "malos" bajaron mucho: ahora casi todos los malos quedaron como baja.)
7. **La web muestra SOLO data real trackeada** (sin ponderación, sin uplift, sin contar "WhatsApp default"). Cualquier ajuste por pauta no trackeada quedó solo documentado, no aplicado.

---

## 6. Métricas finales por campaña (lo que muestra la web)

Revenue del CSV de Analytics GT; Inversión con IVA; ventana respetada por campaña.

| Campaña | slug | Revenue | Inv c/IVA | ROAS | Ventas | Cadencia | Cad. días | Reco |
|---|---|---|---|---|---|---|---|---|
| APIWPP ArgLatam | mt_prospec_apiwpp_arglatam_wpp | 15.540.796 | 10.859.854 | 1.43x | 150 | 76% | ~10 | PUSH |
| Carrousel Exitoso ARG | mt_prospec_carrouselexitoso_arg_wpp | 10.512.239 | 5.028.750 | 2.09x | 89 | 65% | ~31 | CON CUIDADO |
| Oferta Flash ARG | mt_prospec_ofertaflash_arg_wpp | 4.777.416 | 2.438.690* | 1.96x | 47 | 43% | ~59 | NO ESCALAR |
| Mensajes ARG | mt_prospec_mensajes_arg_wpp | 3.289.375 | 3.028.918 | 1.09x | 24 | 78% | ~7 | PUSH |
| Oferta Flash MEX | mt_prospec_ofertaflash_mex_wpp | 2.637.797 | 1.800.000 | 1.47x | 16 | 75% | ~19 | REACTIVAR |
| Buyers ARG (c/CRM) | mt_prospec_buyers_arg_venta | 2.359.916 | 3.925.980 | 0.60x | 14 | 50% | ~19 | NO ESCALAR |
| APIWPP LATAM Venta | mt_prospec_apiwpp_latam_venta | 1.899.921 | 1.522.400 | 1.25x | 10 | 60% | ~15 | NO ESCALAR |
| Mensajes URU | mt_prospec_mensajes_uru_wpp | 497.039 | 948.012 | 0.52x | 3 | 100% | ~0 | NO ESCALAR |
| Remark Mensajes ArgLatam | mt_remark_mensajes_arglatam_wpp | 42.554 | 687.305 | 0.06x | 2 | 100% | ~0 | NO ESCALAR |
| Remark Mensajes MEX | mt_remark_mensajes_mex_wpp | 0 | 386.100 | 0.00x | 0 | N/D | N/D | NO ESCALAR |

**GLOBAL:** Revenue **$41.557.053** · Inversión c/IVA **$30.626.009** · ROAS **1.36x** · **355 ventas**.

\*Oferta Flash ARG: incluye los $819.950 de mayo estimados (bug Días=0).

### Intermitencias por campaña
- APIWPP ArgLatam, Carrousel, Oferta Flash ARG: sin intermitencias (corrieron los 3 meses).
- Mensajes ARG: se prendió el **19 de marzo** (marzo ~12 días, 0 ventas ese mes).
- Oferta Flash MEX: medida ene–feb–mar; **apagada desde abril** (reactivar = prioridad).
- APIWPP LATAM Venta: marzo completo; abril apagada 16→24 (14 días); mayo apagada 1→4 y desde el 15 (apagada definitiva).
- Buyers ARG: se prendió el 6 de abril (pero marzo re-incluido por CRM). Es **venta web**, no WhatsApp.
- Mensajes URU: se prendió el 28 de abril. Remark ArgLatam: 1 de abril. Remark MEX: 15 de mayo (0 ventas en ventana, 1 en junio).

---

## 7. Cursos más vendidos por campaña (del gráfico "Ventas" de las capturas, ranking aprox.)

- **APIWPP ArgLatam:** Personal Trainer (~70), Carrera (~17), Running (~15), Musculación (~14).
- **Carrousel Exitoso ARG:** Personal Trainer (~44), Carrera (~13), Musculación (~11), Pack Gold (~4), Pack Black (~2).
- **Oferta Flash ARG:** Personal Trainer y Musculación (~31), Musculación e Hipertrofia (~9), Carrera Master.
- **Mensajes ARG:** Personal Trainer y Musculación (~15), Musculación Fuerza e Hipertrofia (~5), Carrera Master (~3).
- **Oferta Flash MEX:** Personal Trainer y Musculación (~10), Musculación e Hipertrofia (~3), Pack Gold / Carrera Master / Nutrición Deportiva.
- **APIWPP LATAM:** Personal Trainer y Musculación (~8), Nutrición Deportiva (~1), Musculación e Hipertrofia (~1).
- **Buyers ARG:** Personal Trainer y Musculación (~5), Carrera Master (~2), Musculación e Hipertrofia (~1).
- **Mensajes URU:** Pack Gold / Entrenamiento Funcional / Musculación e Hipertrofia (1 c/u).
- **Remark ArgLatam:** Personal Trainer y Musculación / Pack Gold (1 c/u).

---

## 8. Funnel de leads por campaña (post-baja, ventana mar–may; MEX ene–mar)

Total contado = buenos + neutros + malos (excluye baja). Ordenado por **buenos** (criterio de prioridad de recontacto).

| Campaña | Total | Buenos | Neutros | Malos | Baja | Países top |
|---|---|---|---|---|---|---|
| Carrousel Exitoso ARG | 1.863 | 931 | 931 | 1 | 112 | Argentina 1.854 |
| Mensajes ARG | 2.338 | 684 | 1.647 | 7 | 160 | Argentina 2.328 |
| Oferta Flash ARG | 1.890 | 647 | 1.242 | 1 | 145 | Argentina 1.880 |
| APIWPP ArgLatam | 912 | 449 | 461 | 2 | 102 | Argentina 704 · Uruguay 146 · Ecuador 35 |
| Oferta Flash MEX | 988 | 317 | 668 | 3 | 54 | México 973 · EE.UU. 7 · Chile 4 |
| Mensajes URU | 252 | 88 | 163 | 1 | 20 | Uruguay 249 |
| Remark Mensajes ArgLatam | 236 | 79 | 157 | 0 | 19 | Perú 83 · Argentina 69 · Ecuador 40 |
| APIWPP LATAM Venta | 76 | 46 | 30 | 0 | 6 | Chile 36 · Uruguay 20 · Argentina 16 |
| Remark Mensajes MEX | 110 | 30 | 80 | 0 | 3 | México 109 |
| Buyers ARG | 2 | 0 | 2 | 0 | 0 | Argentina 2 (es venta web, casi sin funnel WhatsApp) |

- **quality_score**: good/neutral/bad. Lead llega → neutro por defecto; CS lo califica. Bueno = interesado/responde; malo = no responde/no paga/no interesa.
- Matching campaña: por prefijo de `fuente_origen` (el ad name empieza con el nombre de la campaña). Solo las 10 campañas con carpeta; el resto del CSV se ignora.
- Archivos preparados generados: `campañas/datos_de_leads/leads_por_campana_mes.csv`, `leads_por_campana_pais.csv`, `leads_preparados.json` (con baja).

---

## 9. Plantillas (archivo `plantillas_analytics_2026.csv`) — TRABAJO EN CURSO

### Lo que pidió el usuario (rediseño del sitio)
- **Renombrar** la página actual "Push de Plantillas" a **"Rendimiento de Plantillas"**, con dos sub-secciones/botones internos:
  1. **"Rendimiento de Plantillas"** (NUEVO): métricas generales arriba (Leads buenos – neutros – malos[+baja] y **gasto en plantillas últ. 3 meses**), una sección de **Recomendaciones** (top de mejores plantillas: qué correr y por qué, en qué países, qué cursos vendieron), un **gráfico** del rendimiento de plantillas de los últimos 3 meses, e identificar **qué plantillas tuvieron ventas**.
  2. **"Push de Plantillas" / "Campañas recomendadas"** (la data ACTUAL de la página): panorama de leads buenos/neutros/malos por campaña + un **cuadro nuevo de qué campaña pushear con qué plantillas** (cruzando campañas con plantillas: algunas plantillas van mejor para México, otras para Argentina, para vender X producto, etc.).

### Estructura del archivo de plantillas
- Cada fila = un **touchpoint** de una venta (atribución multi-touch). 19.989 filas; columnas relevantes: `source_name` (nombre de la plantilla), `source_category`, `Fecha venta`, `Mes Venta`, `client_country`, `product_name`, `currency`, `total_amount`, **`Revenue`** (parte lineal = total ÷ touchpoints), `touchpoints_per_sale`, `sales_credit_linear` (fracción de venta), `sale_id`.
- **Plantillas** = `source_category` ∈ {`Templates`, `Fuente para identificar conversaciones iniciadas con mensaje de plantilla de Meta`}.
- **13.870 filas de plantilla** en total; **2.915 en mar–abr–may 2026 = 621 ventas únicas**.
- **OJO atribución multi-touch:** una misma venta suele estar tocada por varias plantillas. El archivo ya reparte cada venta entre sus touchpoints (Revenue = parte lineal, sales_credit_linear = fracción). **Sumar la venta entera a cada plantilla la duplicaría.** Recomendado: usar atribución **lineal** (sumar la columna `Revenue` y `sales_credit_linear` por plantilla).
- **Monedas:** en la ventana hay **2.362 filas ARS y 553 USD** (México, etc.). Para un total único hay que unificar a ARS con un tipo de cambio.
- **Costo de plantillas:** cada plantilla enviada cuesta **≈ USD 0,61**. El archivo de ventas NO trae la cantidad de plantillas enviadas (solo las ligadas a ventas), así que el "gasto en plantillas" total no se puede sacar solo de acá.

### DUDAS ABIERTAS (pendientes de responder por el usuario antes de construir)
1. **Atribución**: ¿lineal (recomendado, sin duplicar), última plantilla (last-touch), o completa a cada plantilla?
2. **Tipo de cambio USD→ARS** para unificar el revenue de plantillas (la calculadora de proyección usa 1.200 ARS/USD por defecto).
3. **Gasto en plantillas**: ¿de dónde sale la cantidad de plantillas enviadas? (¿contar conversaciones iniciadas por plantilla en los archivos de leads × 0,61, o el usuario pasa el número de mensajes enviados?).
4. **Métricas generales** (buenos/neutros/malos+baja del tope de la página): ¿son el total del funnel de las 10 campañas, todos los leads del sistema, o solo leads tocados por plantillas?
5. Confirmar **nombres/estructura** de los dos botones internos.

---

## 10. El sitio web (3 páginas)

Generadas por un script Python (`gen.py`) que arma el HTML embebiendo las imágenes en base64. Páginas:

1. **`analisis_campanas_meta_junio2026.html`** (= `index.html` en deploy) — **Push de Campañas**: stats globales, contexto, criterios de scoring, notas de metodología, tarjetas por campaña (ROAS, inversión, ventas, cadencia en %, cursos top, road touchpoint mensual con meses exactos), tabla comparativa con filas **clickeables** que despliegan el desglose mensual.
2. **`push_plantillas.html`** — **Push de Plantillas** (a renombrar "Rendimiento de Plantillas"): tabla de funnel ordenada por **leads buenos**, tarjetas por campaña con funnel (buenos arriba en grande, neutros debajo), métricas de contexto, "gente de baja" por campaña, y notas de por qué recontactar. Dos secciones: cadencia baja (rápido) y recontacto a meses (lento).
3. **`proyeccion_presupuesto.html`** — **Proyección de Presupuesto**: calculadora interactiva (ver sección 11).

**Navegación y estética (en las 3):**
- 3 botones de nav con efecto **hover** (se elevan, escalan, brillo #ea0849).
- **Barra superior** fina con gradiente **#6001e2 → #ea0849**.
- **Fondo** degradado horizontal **#111624 (izq, ~58%) → #29021b (der)**.
- **Loader al cargar**: logo de GT latiendo en el centro (~0,95s, CSS puro) sobre overlay semi-transparente; luego fade-in del contenido.
- Tarjetas/marcos en gris azulado (#111827 / #0f172a). Acentos rosa/violeta (#fe006b, #712fd1).

---

## 11. Metodología de la calculadora de Proyección de Presupuesto

(Detallado en `Metodologia_Proyeccion_Presupuesto_GT.docx`.)

Por cada campaña se precarga su **economía unitaria**: ROAS, **CPA** (=Inv÷Ventas), **CPL** (=Inv÷Leads), ticket, % buenos/neutros, **cadencia en días**.

Con un presupuesto **P** y un tiempo **T** (días):
- Revenue eventual = P × ROAS · Ventas eventuales = P ÷ CPA · Consultas = P ÷ CPL (regla de 3 / proporción).
- **Ponderación de la cadencia (modelo de maduración):** fracción que madura en T días = **1 − e^(−T ÷ cadencia_media)**. Revenue/ventas "en ventana" = eventual × esa fracción. (Calibrado: da muy cerca del % histórico "mismo mes".)
- **"Eventual"** = total final; **"en ventana"** = lo que cae dentro de los T días.
- **Ajuste de eficiencia** (slider, default 100%): multiplica ROAS/ventas para modelar rendimientos decrecientes al escalar.
- **Combinado multi-campaña:** suma inversión, consultas, ventas y revenue en ventana; ROAS combinado = revenue en ventana ÷ inversión total.
- Entrada en **ARS**; hay campo de tipo de cambio editable (default 1.200) solo para los presets en USD.

---

## 12. "WhatsApp default" — pauta no trackeada (solo documentado, NO aplicado a la web)

- Chatty marca muchas ventas como **"WhatsApp default"** (parecen orgánicas). En mar–may: **348 ventas / $54,8M** de revenue. Buena parte es **pauta no trackeada** (entraron por anuncio pero sin atribución), mezclada con orgánico.
- Como la **inversión ya está 100% contada**, este revenue no atribuido hace que los ROAS reales estén **subestimados** (podrían ser 2–3x mayores).
- No se pueden exportar los chats ni detectar las plantillas masivamente, y no identifican la campaña. Solo hay agregados (países, cursos, revenue).
- **Método propuesto (anexo §9 del docx):** repartir una fracción **S** del default **proporcional al revenue trackeado** de cada campaña → equivale a multiplicar el ROAS de todas por un **factor uniforme = 1 + S × (54,8M ÷ 41,5M) = 1 + S × 1,32**.
  - S=50% → ×1,66 · S=70% → ×1,92 · S=100% → ×2,32.
  - S se acota con el cotejo de países/cursos del default (casi idénticos a los de las campañas pagas → S alto, ~60–80%).
- **Decisión del usuario:** dejarlo solo documentado por ahora; NO modificar la web. Solución de fondo: configurar el ad referral (ctwa_clid) en Chatty.

---

## 13. Estado y próximos pasos

- ✅ Análisis de campañas, métricas, cursos, leads (con bajas), web (3 páginas), hosting, documento de metodología: COMPLETOS.
- 🔄 **En curso:** rediseño de la página de plantillas ("Rendimiento de Plantillas" + "Push/Campañas recomendadas") usando `plantillas_analytics_2026.csv`. **Bloqueado por las 5 dudas abiertas de la sección 9.**
- Recordatorio operativo: tras cada cambio en el sitio, **re-sincronizar `web_para_hostear/`** (copiar las 3 páginas y reemplazar el nombre de la principal por `index.html` en los links internos).
