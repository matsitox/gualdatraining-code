# Gualda Training — Ads Dashboard

Dashboard de análisis de campañas **Meta Ads** para decisiones de push mensual de WhatsApp y estrategia publicitaria de Gualda Training.

**Live:** https://gualdatraining-ads.netlify.app  
**Repo:** https://github.com/matsitox/gualdatraining-code

---

## Propósito del repositorio

Este repo existe para **analizar la pauta publicitaria de Gualda Training**: campañas activas en Meta Ads, revenue atribuido, gasto con IVA, ROAS por campaña, análisis de leads, plantillas de WhatsApp con mejor rendimiento, y proyecciones de presupuesto.

El output es un **sitio web estático de 3 páginas HTML** que se usa mensualmente para decidir la estrategia de push de WhatsApp y escalar o frenar campañas.

---

## Auto-push a GitHub

**Cada vez que Claude Code realiza un cambio en este repositorio, hace push automático a GitHub.**  
Esto garantiza que el historial de cambios quede registrado y el repo siempre esté actualizado.  
Rama: `main` · Usuario: `matsitox` · Repo: `gualdatraining-code`

---

## Las 3 páginas del sitio

| Página | Archivo | Descripción |
|--------|---------|-------------|
| **Push de Campañas** | `web/index.html` | ROAS, revenue, inversión, ventas y cadencia de las 10 campañas activas. Tabla comparativa con desglose mensual. Recomendación: PUSH / CON CUIDADO / NO ESCALAR / REACTIVAR |
| **Rendimiento de Plantillas** | `web/push_plantillas.html` | Revenue atribuido a plantillas de WhatsApp (Mar–May 2026). Top 10 plantillas. Funnel de leads por campaña con porcentajes. |
| **Proyección de Presupuesto** | `web/proyeccion_presupuesto.html` | Calculadora interactiva: dado un presupuesto y un horizonte de días, proyecta revenue/ventas/consultas por campaña usando modelo de maduración exponencial. |

---

## Stack técnico

- **HTML estático autocontenido** — imágenes embebidas en base64, sin dependencias externas, sin framework
- **Python** — `scripts/gen_push_plantillas.py` regenera `push_plantillas.html` desde CSVs
- **Deploy en Netlify** — drag & drop de la carpeta `web/` en app.netlify.com
- **Datos privados** — CSVs de leads y ventas en `data/` (gitignoreados, copiar manualmente)

---

## Estructura del repo

```
web/                        → deploy a Netlify (los 3 HTMLs)
scripts/
└── gen_push_plantillas.py  → regenera push_plantillas.html desde CSVs
data/                       → CSVs de fuente (gitignoreados — copiar manualmente)
├── plantillas_analytics_2026.csv
└── leads/
    └── enero.csv … mayo.csv
docs/
├── CONTEXTO_PROYECTO_GT_traspaso.md  → contexto histórico completo
└── Gualda Training INFO.md           → info completa de la empresa
CLAUDE.md                   → contexto completo para Claude Code (leer siempre)
```

---

## Setup

```bash
# Clonar
git clone https://github.com/matsitox/gualdatraining-code.git
cd gualdatraining-code

# Copiar datos privados (no están en el repo)
cp /ruta/local/plantillas_analytics_2026.csv data/
cp /ruta/local/leads/*.csv data/leads/

# Regenerar push_plantillas.html
python3 scripts/gen_push_plantillas.py

# Deploy — subir carpeta web/ a Netlify (drag & drop)
```

Para `index.html` y `proyeccion_presupuesto.html` no hay script — se editan directamente.

---

## Datos y privacidad

Los archivos CSV con datos de leads y ventas **no están en el repo** (`.gitignore`). Son datos privados de clientes. La carpeta `data/` contiene solo `.gitkeep` como placeholder.

---

## Contexto técnico completo

Ver [`CLAUDE.md`](CLAUDE.md) para toda la documentación técnica: métricas por campaña, lógica de clasificación de leads, atribución multi-touch, diseño visual y flujo de trabajo.

---

---

# Gualda Training — Información de la Empresa

> Esta sección es de referencia de negocio, no de desarrollo. Contiene todos los detalles de la academia necesarios para entender el contexto al analizar campañas, leads, copies y revenue.

---

## Descripción General

| Campo | Detalle |
|-------|---------|
| **Nombre** | Gualda Training |
| **Tipo** | Academia de cursos fitness online |
| **Fundador** | Axel Gualda (estudiante de Ingeniería Industrial, UTN Buenos Aires) |
| **Sede** | Argentina (alcance latinoamericano e hispanohablante) |
| **Sitio web** | https://gualdatraining.com |
| **Campus online** | https://campus.gualdatraining.com |
| **Instagram** | https://www.instagram.com/gualdatraining/ |
| **LinkedIn** | https://www.linkedin.com/school/gualdatraining/ |
| **YouTube** | https://www.youtube.com/c/GualdaTraining |
| **Facebook** | https://www.facebook.com/Gualda.training/ |

**Propuesta de valor principal:**
- Única academia con aval de **ALIFID** (Alianza Latinoamericana de Instructores de Fitness y Deporte)
- Única avalada por **ISLA** (Instituto Superior Latinoamericano), incorporada al **Ministerio de Educación CABA** (A-1548)
- Más de **20.000 alumnos** en toda Latinoamérica
- Más de **200 gimnasios** que confían en sus egresados y comparten oportunidades laborales

---

## Oferta Académica

| Código | Curso |
|--------|-------|
| **CMPT** | Carrera Master Personal Trainer (7 cursos, 9 certificados, 73hs) |
| **IFA** | Carrera Avanzada en Fitness y Actividad Física (5 cursos, 60hs) |
| **PTIM** | Instructorado de Personal Trainer y Musculación |
| **IM** | Instructorado de Musculación y Especialista en Hipertrofia |
| **ND** | Curso de Nutrición Deportiva |
| **NDA** | Curso de Nutrición Deportiva Avanzada |
| **CT** | Instructorado de Calistenia |
| **LD** | Curso de Lesiones Deportivas |
| **EEO** | Curso de Especialización en Entrenamiento Online |
| **IR** | Instructorado de Running |
| **PF** | Instructorado de Preparación Física para Deportes |
| **BIO** | Curso de Biomecánica |
| **EF** | Instructorado de Entrenamiento Funcional, HIIT y GAP |
| **ST** | Curso de Especialización de Stretching y Movilidad |
| **EMB** | Curso de Entrenamiento en el Embarazo |
| **PTS** | Curso de Especialización en Salud para Entrenadores |
| **MKT** | Curso de Marketing y Ventas para Entrenadores |
| **ADU** | Curso de Entrenamiento de Adultos Mayores |

### Packs

| Pack | Cursos incluidos |
|------|-----------------|
| **PACK BLACK INSTRUCTORES** | PTIM + IM + BIO + PF + EF |
| **PACK BLACK TRAINING** | PTIM + IM + ND + NDA + LD |
| **PACK GOLD** | PTIM + ND + BIO (3x1) |
| **Pack Personalizado** | El alumno elige 5 cursos |

---

## Promociones y Descuentos

| Promoción | Descuento | Condición |
|-----------|-----------|-----------|
| **#GUALDASALE** | 75% OFF | En todos los cursos, carreras y packs. Con fecha límite |
| **OFERTAFLASH** | 60% OFF | Cupón aplicable a todos los cursos. Válido 48hs |
| **GUALDA2026** | 60% OFF | Cupón general 2026 |
| **Pago único** | 45% OFF | Al abonar en un solo pago |
| **Comunidad Gualda** | 15% OFF adicional | Para alumnos con formación previa |
| **12 cuotas sin interés** | Hasta 40% + 2 cursos gratis | Con tarjeta |

> Verificar siempre antes de usar copies con descuento: https://www.gualdatraining.com/promociones-vigentes/

---

## Beneficios para Alumnos

- Carnet profesional digital como instructor
- Web personal como instructor
- Aparición en el buscador de instructores de ALIFID
- Plataforma **Top Trainers**: conecta egresados con gimnasios
- Bolsa laboral activa: +25 búsquedas laborales por semana por mail
- 15% a 50% de descuento en membresías y equipamiento de gimnasios asociados

---

## Programa de Afiliados

- Los afiliados reciben un código de referido con **15% de descuento exclusivo** para compartir
- Cobran comisión por cada inscripción con su código
- Contacto inicial por WhatsApp en 48 horas hábiles
- URL: https://www.gualdatraining.com/programa-afiliados

---

## Top Trainers — Segundo Proyecto

| Campo | Detalle |
|-------|---------|
| **Qué es** | Portal / buscador de entrenadores personales ("LinkedIn Fitness") |
| **Estado** | En desarrollo — exclusivo para certificados GT, próximamente abierto |
| **URL** | https://toptrainers.app |
| **Instagram** | https://www.instagram.com/toptrainers.app/ |
| **Color de marca** | #e91e8c |

Los entrenadores crean su perfil con certificaciones, especializaciones y tarifas. Los usuarios buscan filtrando por ubicación, modalidad, especialidad, precio, género y tipo de clase.

---

## Buyer Personas (para análisis de campañas)

### Buyer 1 — El apasionado del gym que quiere trabajar de lo que ama
Perfil principal. Va al gym todos los días, trabaja en algo que no le gusta. Siente que "algo está al revés". Puntos de dolor: no le gusta su trabajo, miedo a invertir mal, barrera económica, no sabe por dónde empezar.

### Buyer 2 — El PT o instructor que ya trabaja y quiere actualizarse
Perfil secundario. Ya trabaja en gimnasio o como PT freelance. Quiere diferenciarse, tiene conocimiento básico pero busca profundidad y aval internacional.

---

## Niveles de Consciencia del Funnel

| Nivel | Descripción |
|-------|-------------|
| **Inconscientes** | Aman el gym, no saben que quieren ser PT |
| **Conc. del Problema** | Saben que no quieren su trabajo, no saben qué hacer |
| **Conc. de la Solución** | Saben que pueden ser PT, no saben cómo formarse |
| **Conc. del Producto** | Conocen Gualda, evalúan si les sirve |
| **Muy conscientes (3%)** | Están a punto de comprar — remarketing |

---

## Datos Clave

- +20.000 alumnos certificados en Latinoamérica
- +200 gimnasios y centros deportivos que confían en los egresados
- 144K seguidores en Instagram
- Presencia en Argentina, Chile y todo el mundo hispanohablante
- Modalidad: 100% online y a tu ritmo

---

## URLs Importantes

| Recurso | URL |
|---------|-----|
| Sitio principal | https://gualdatraining.com |
| Campus online | https://campus.gualdatraining.com |
| Promociones vigentes | https://www.gualdatraining.com/promociones-vigentes/ |
| Packs de cursos | https://www.gualdatraining.com/packs-cursos-fitness |
| Beneficios | https://www.gualdatraining.com/beneficios-gualda-training |
| Programa de afiliados | https://www.gualdatraining.com/programa-afiliados |
| Recursos gratuitos | https://www.gualdatraining.com/recursos-gratuitos-fitness |
| Top Trainers | https://toptrainers.app |

---

---

# Aprendizajes y Notas de Sesiones

> Esta sección se actualiza cada vez que se aprende algo nuevo en una sesión de trabajo con Claude Code. Sirve como memoria de contexto para futuras sesiones.

| Fecha | Aprendizaje |
|-------|-------------|
| 2026-06-30 | Repositorio creado en GitHub (`matsitox/gualdatraining-code`). GitHub CLI instalado con `winget install GitHub.cli`. Claude Code tiene acceso vía `gh auth` con cuenta `matsitox`. |
| 2026-06-30 | Regla establecida: cada vez que Claude Code hace un cambio en este repo, hace push automático a GitHub en la rama `main`. |
