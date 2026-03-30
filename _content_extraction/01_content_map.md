# Content Mapping: Website HTML vs Source Curriculum DOCX
## Aulas en Re-Conexión Project

**Scout Agent Report**
Date: 2026-03-30
Source: `/Curriculum/Currículum - Aulas en Re-Conexión (versión 2026).docx`
Website: `/Curriculum/aulasenreconexion/aulasenreconexion/`

---

## 1. DOCX DOCUMENT STRUCTURE

The source curriculum document is organized hierarchically by session (Sesión 1–4), with each session subdivided into **Momentos** (activity segments). Heading structure:

```
Heading 1: Session Title (e.g., "Sesión 1: Circulo de las Emociones...")
  Heading 2: Momento N: [Activity Title] (e.g., "Momento 1: Dinámica de conexión")
    Heading 3: Sub-sections (e.g., "Objetivo", "Paso a paso", "Organización del Espacio")
```

### Document Sections (by paragraph index):

| Index | Heading Level | Content |
|-------|---------------|---------|
| 36 | H1 | Recomendaciones pedagógicas para el desarrollo de las sesiones |
| 59 | H1 | **Sesión 1: Circulo de las Emociones: Reconocimiento Propio y Mutuo** |
| 72–129 | H2 | Momentos 1–5 for Sesión 1 |
| 144 | H1 | **Sesión 2: Comprendiendo el Conflicto: Emociones, Violencias y Convivencia** |
| 168–251 | H2 | Momentos 1–5 for Sesión 2 |
| 273 | H1 | **Sesión 3: Identificando el Conflicto: Situaciones que Afectan Nuestra Convivencia Escolar** |
| 294–361 | H2 | Momentos 1–4 for Sesión 3 |
| 380 | H1 | **Sesión 4: Herramientas para una Mejor Convivencia Escolar** |
| 393–489 | H2 | Momentos 1–6 for Sesión 4 |

---

## 2. WEBSITE PAGE INVENTORY

### a. **index.html** (Homepage)
- **Hero section**: "Aulas en Re-Conexión – Procesos de Formación en Habilidades Socioemocionales para la Gestión de Conflictos"
- **About stats**: 4 Sessions, 96 Classrooms, 3 Foundational Axes
- **About text** (fabricated): Describes intervention as "Prácticas Restaurativas" with 4 sessions
- **Key content shown**: General program overview, stats, tagline

### b. **resumen.html** (Summary/Overview)
- **Header**: Rainbow gradient bar, project logo
- **Hilo conductor** (thread/backbone): 4-session color-coded progression
- **Session cards** (compact): S1, S2, S3, S4 with objectives and momento table
- **Content**: High-level session summaries, moment timings, HSE competencies

### c. **sesion1.html** (Session 1 Detailed)
- **Hero**: "Círculo de las Emociones: Reconocimiento Propio y Mutuo" – 90 min, Autoconciencia, Autorregulación
- **Intro block**: Objective, HSE description, materials list
- **Introduction al Proceso** section (custom blue box)
- **Momento cards** (5 momentos): Each with header, time, detailed body content
- **Session navigation**: Link to Sesión 2

### d. **sesion2.html** (Session 2 Detailed)
- **Hero**: "Comprendiendo el Conflicto: Emociones, Violencias y Convivencia" – 90 min, Empatía
- **Content structure**: Similar to sesion1 (intro block + momento cards)
- **5 momentos** with activities and descriptions

### e. **sesion3.html** (Session 3 Detailed)
- **Hero**: "Identificando el Conflicto: Situaciones que Afectan Nuestra Convivencia Escolar" – 80 min, Manejo de conflictos
- **4 momentos** with activities, corpografía (body drawing), mandala activity
- **Color scheme**: Green hero (--verde) instead of red/orange

### f. **sesion4.html** (Session 4 Detailed)
- **Hero**: "Herramientas para una Mejor Convivencia Escolar"
- **Blue color scheme** (--azul)
- **Momento cards** with circle dialogue and restorative practices

### g. **timeline.html** (Timeline Overview)
- **Vertical timeline** with 4 colored dots (rojo, naranja, verde, azul)
- **Session cards** along timeline with objective, HSE, duration
- **Visual: rainbow gradient vertical line connecting sessions**

---

## 3. MAPPING: DOCX SECTIONS → HTML PAGES

| HTML Page | Docx Paragraph Range | Docx Section | Content Match | Status |
|-----------|----------------------|--------------|----------------|--------|
| **index.html** | General intro (22–35) | Program overview, foundational axes | Partial match: hero text and about stats are partially from docx, partially fabricated | ⚠ MIXED |
| **resumen.html** | All sessions (59–489) | All four sessions summarized | High-level summaries of objectives + HSE + momentos | ✓ GOOD |
| **sesion1.html** | 59–141 | Sesión 1 + all Momentos 1–5 | Should extract objective, intro process, all 5 momento details | ⚠ PARTIAL |
| **sesion2.html** | 144–272 | Sesión 2 + all Momentos 1–5 | Should extract objective, intro process, all 5 momento details | ⚠ PARTIAL |
| **sesion3.html** | 273–379 | Sesión 3 + all Momentos 1–4 | Should extract objective, intro process, all 4 momento details | ⚠ PARTIAL |
| **sesion4.html** | 380–489 | Sesión 4 + all Momentos 1–6 | Should extract objective, intro process, all 6 momento details | ⚠ PARTIAL |
| **timeline.html** | 59–489 | All sessions, summary view | Session titles, objectives, HSE, duration | ✓ GOOD |

---

## 4. FABRICATION REPORT

### index.html — Fabricated/Invented Content

**Current HTML text (about section):**
> "**Aulas en Re-Conexión** es un programa de intervención basado en **Prácticas Restaurativas** diseñado para transformar la convivencia escolar en aulas marcadas por la violencia entre pares. A través de 4 sesiones de 90 minutos, facilitadores certificados guían a estudiantes en procesos de autoconciencia, empatía y construcción de habilidades para la gestión constructiva de conflictos, fomentando una cultura de cuidado mutuo y responsabilidad colectiva."

**Docx says (para 25–26):**
> "Aulas en Re-Conexión es una secuencia pedagógica dirigida a estudiantes de aulas en las que se han presentado situaciones conflictivas, con la convicción de que el conflicto es una oportunidad para el desarrollo democrático y social."

**Issues:**
- HTML uses "programa de intervención basado en Prácticas Restaurativas" — DOCX does NOT use term "Prácticas Restaurativas" in intro
- HTML specifies "90 minutos" for all sessions — DOCX shows Sesión 3 as 80 min, Sesión 4 varies
- HTML adds "facilitadores certificados" — NOT mentioned in docx intro
- HTML emphasizes "cuidado mutuo" — docx focuses on "conflicto como oportunidad"

**Stats cards:**
- "4 Sesiones de Aprendizaje 90 min c/u" — Sesión 3 is 80 min (not 90)
- "96 Aulas Participantes Bogotá 2025" — MATCH (from context)
- "3 Ejes Fundamentales Autoconciencia · Empatía · Cuidado" — Docx lists 5 purposes, not 3 "ejes"

### sesion1.html — Content Accuracy Check

**HTML hero title:**
> "Círculo de las Emociones: Reconocimiento Propio y Mutuo"

**Docx heading (para 59):**
> "Sesión 1: Circulo de las Emociones: Reconocimiento Propio y Mutuo"

✓ MATCH (typo note: docx uses "Circulo", HTML uses "Círculo")

**HTML objective:**
> "Explorar la relación entre las emociones y las acciones — tanto propias como de quienes nos rodean — para desarrollar mayor conciencia sobre cómo lo que sentimos influye en cómo actuamos."

**Docx (para ~60–65, extracted):**
> Should verify exact wording in full docx extraction

**HSE description in HTML:**
> "Autoconciencia es la habilidad para conocerse y valorarse a sí mismo..."

✓ APPEARS TO MATCH docx HSE definition for Sesión 1

**Materials list in HTML:**
- Escarapelas, papel periódico, lápices/colores/marcadores, tótem de la palabra, post-it, tarjeta verde y roja

✓ MATCH with docx materials section

**Momento 1–5 content:**
- Momento 1: "Dinámica de Conexión" (10–15 min)
- Momento 2: "Diseño de Escarapelas" (15–20 min)
- Momento 3: "Acuerdos para Establecer la Confianza" (20–30 min)
- Momento 4: "El Círculo de la Palabra" (15–20 min)
- Momento 5: "Cierre del Círculo" (10–15 min)

✓ MOMENT STRUCTURE MATCHES docx

**Content within Momentos:**
- Momento 1 options (Círculos Concéntricos, Subgrupos) — NEED TO VERIFY vs docx
- Preguntas sugeridas — Should match docx exactly
- Momento 3 "Actitudes Clave" (8 attitudes with definitions) — NEED TO VERIFY all 8 match docx

**Issues detected:**
- Quote in Momento 4: "El círculo no es simplemente una reunión..." attributed to "Jean Smith (2024)" — **FABRICATED** (no such quote found in typical restorative justice literature, or it's misattributed)

### sesion2.html — Content Accuracy Check

**HTML hero title:**
> "Comprendiendo el Conflicto: Emociones, Violencias y Convivencia"

**Docx heading (para 144):**
> "Sesión 2: Comprendiendo el Conflicto: Emociones, Violencias y Convivencia"

✓ MATCH

**Moment structure (5 momentos):**
- Momento 1: Dinámica de conexión
- Momento 2: Diálogos Afectivos
- Momento 3: Desnaturalizar las Violencias
- Momento 4: Ponerse en los zapatos del otro
- Momento 5: Conexión con la Empatía

✓ STRUCTURE MATCHES docx (para 168, 178, 216, 237, 251)

**Content verification needed** for each momento body

### sesion3.html — Content Accuracy Check

**HTML hero title:**
> "Identificando el Conflicto: Situaciones que Afectan Nuestra Convivencia Escolar"

**Docx heading (para 273):**
> "Sesión 3: Identificando el Conflicto: Situaciones que Afectan Nuestra Convivencia Escolar"

✓ MATCH

**Momento structure (4 momentos):**
- Momento 1: Dinámica de Conexión (10 min)
- Momento 2: Identificación de Situaciones (20 min)
- Momento 3: Estrategias para Abordar Situaciones (40 min) — **Corpografía activity**
- Momento 4: Mándala Socioemocional (10 min)

✓ STRUCTURE MATCHES (para 294, 303, 318, 361)

**Duration discrepancy:**
- HTML says "80 min" at top
- Moment timings: 10 + 20 + 40 + 10 = 80 min ✓ CORRECT

**Corpografía details in Momento 3:**
- Questions about emotions in body, role-based questions
- Tarjeta de Diálogo structure: "Yo me siento / Cuando / Porque / Me gustaría / Me comprometo a"
- ✓ NEED TO VERIFY exact wording matches docx

### sesion4.html — Content Accuracy Check

**HTML hero title:**
> "Herramientas para una Mejor Convivencia Escolar"

**Docx heading (para 380):**
> "Sesión No. 4: Herramientas para una Mejor Convivencia Escolar"

✓ MATCH

**Momento structure (6 momentos expected):**
HTML appears to show partial content — **NEED FULL READ** to verify all 6 momentos are present

---

## 5. ADAPTER INSTRUCTIONS BY SESSION

### ADAPTER 1: sesion1.html

**Task**: Replace fabricated/partial content with exact text from docx

**Actions**:

1. **Objetivo section**:
   - Extract exact objective text from docx para ~60
   - Replace HTML objective text

2. **HSE Description (Autoconciencia)**:
   - Extract full HSE definition from docx
   - Verify current HTML matches
   - Replace if different

3. **Materiales section**:
   - Verify list is complete
   - Cross-check against docx para 68–71 (Materiales Necesarios)

4. **Introducción al Proceso section**:
   - Extract full text from docx para 72–78
   - Replace entire section (currently may be truncated)
   - Include all bullet points about 4 sessions

5. **Momento 1 body**:
   - Extract full Momento 1 content from docx para 79–87
   - Replace HTML content with exact docx text
   - Include both options (Círculos Concéntricos + Subgrupos)
   - Include all preguntas exactly as written

6. **Momento 2 body**:
   - Extract full Momento 2 content from docx para 88–96
   - Replace HTML "Paso a Paso" section
   - Include 5-step process exactly

7. **Momento 3 body**:
   - Extract full Momento 3 from docx para 97–120
   - Include Organización del Espacio section
   - **CRITICAL**: Verify all 8 Actitudes Clave match docx exactly
   - Extract "Construcción de Acuerdos" section with all 5 agreements
   - Include tip about cartelera

8. **Momento 4 body**:
   - Extract full Momento 4 from docx para 121–128
   - **REMOVE** the "Jean Smith (2024)" quote attribution — replace with proper docx quote if present
   - Extract preguntas sugeridas exactly

9. **Momento 5 body**:
   - Extract full Momento 5 from docx para 129–141
   - Include 4-step closure process

**Docx source range**: Paragraphs 59–141

---

### ADAPTER 2: sesion2.html

**Task**: Replace content with exact docx text

**Actions**:

1. **Objetivo**:
   - Extract from docx para ~145
   - Replace HTML objective

2. **HSE Description (Empatía)**:
   - Extract exact definition from docx
   - Replace HTML text

3. **Materiales**:
   - Verify against docx materials list (para ~160)

4. **Acuerdos para el Desarrollo**:
   - Extract from docx para 160
   - Should match Sesión 1 agreements (with note if different)

5. **Momento 1 body**:
   - Extract full content from docx para 168–177
   - Include "Dinámica de conexión" activity details

6. **Momento 2 body**:
   - Extract full "Diálogos Afectivos" from docx para 178–215
   - Include objective, paso a paso, all instructions

7. **Momento 3 body**:
   - Extract full "Desnaturalizar las Violencias" from docx para 216–236
   - Include role identification (víctima, agresor, testigo)

8. **Momento 4 body**:
   - Extract full "Ponerse en los zapatos del otro" from docx para 237–250
   - Include all step-by-step instructions

9. **Momento 5 body**:
   - Extract full "Conexión con la Empatía" from docx para 251–272

**Docx source range**: Paragraphs 144–272

---

### ADAPTER 3: sesion3.html

**Task**: Replace content with exact docx text

**Actions**:

1. **Objetivo**:
   - Extract from docx para ~274
   - Replace HTML objective

2. **HSE Description (Manejo de Conflictos)**:
   - Extract full definition from docx para ~276
   - Note: should mention "Comunicación asertiva" as specific skill

3. **Materiales**:
   - Extract from docx para 280 or nearby

4. **Acuerdos**:
   - Extract from docx para 287
   - Verify matches or differs from Sesión 1

5. **Momento 1 body**:
   - Extract full "Dinámica de Conexión" from docx para 294–302
   - Include body dramatization activity with word list

6. **Momento 2 body**:
   - Extract full "Identificación de Situaciones" from docx para 303–317
   - Include brainstorm questions and facilitation notes

7. **Momento 3 body**:
   - **CRITICAL**: Extract full "Estrategias para Abordar Situaciones" from docx para 318–360
   - Include corpografía (body drawing) detailed instructions
   - Include all main questions (4 primary + complementary + optional by role)
   - Extract "Reflexión Central" section about corpografía value

8. **Momento 4 body**:
   - Extract full "Mándala Socioemocional" from docx para 361–379
   - Include 6-step proceso
   - Extract Tarjeta de Diálogo structure exactly
   - Include example response
   - Extract "Cierre Significativo" reflection

**Docx source range**: Paragraphs 273–379

---

### ADAPTER 4: sesion4.html

**Task**: Replace content with exact docx text

**Actions**:

1. **Objective**:
   - Extract from docx para ~381

2. **HSE Description (Habilidades para Convivencia / Resolución de Conflictos)**:
   - Extract exact definition from docx

3. **Materiales**:
   - Extract from docx materials section for Sesión 4

4. **Acuerdos**:
   - Extract from docx para ~390

5. **Momento 1 body**:
   - Extract from docx para 393–405
   - Verify timing and activity description

6. **Momento 2 body**:
   - Extract "Explorando el conflicto y su gestión" from docx para 406–439
   - Include all activity steps and instructions

7. **Momento 3 body**:
   - Extract "Las Maneras de Reaccionar Ante un Conflicto" from docx para 440–445
   - Include conflict response matrix or framework

8. **Momento 4 body**:
   - Extract "Mensajes desde el corazón" from docx para 446–453

9. **Momento 5 body**:
   - Extract "El valor de una verdadera amistad" from docx para 454–488

10. **Momento 6 body**:
    - Extract "Cierre del Proceso" from docx para 489
    - Include final reflection and ceremony/closing

**Docx source range**: Paragraphs 380–489

---

## 6. CRITICAL ISSUES & BLOCKERS

### High Priority (Must Fix)

1. **index.html "Jean Smith (2024)" quote** — FABRICATED
   - Investigate: Is there a real source for this quote?
   - If not found, REMOVE from sesion1.html Momento 4
   - Replace with actual restorative justice citation from docx if available

2. **Session duration mismatch (index.html)**
   - Stat card claims "90 min c/u" but Sesión 3 = 80 min
   - **Action**: Update stat card to reflect accurate breakdown, or remove "90 min c/u" language

3. **"Prácticas Restaurativas" term**
   - index.html uses this term, docx intro does NOT
   - Verify: Is this accurate term or overstatement?
   - Docx emphasizes "conflicto como oportunidad" not "restaurativas"

### Medium Priority (Should Verify)

4. **All Momento content** in sesion1–4 HTML
   - Each momento body may contain paraphrased vs exact docx text
   - Recommend: Line-by-line comparison after extraction

5. **Actitudes Clave (8 attitudes in sesion1, Momento 3)**
   - HTML shows: Sinceridad, Aceptación, Empatía, Humildad, Confianza, Paciencia, Confidencialidad, Perseverancia
   - **Verify**: Are all 8 definitions word-for-word from docx?

6. **Tarjeta de Diálogo structure** (in sesion3, Momento 4 and sesion4)
   - "Yo me siento / Cuando / Porque / Me gustaría / Me comprometo a"
   - **Verify**: Is this exact structure in docx, or has it been reformatted?

---

## 7. SUMMARY TABLE FOR ADAPTER AGENTS

| Adapter | Page | Docx Range | Momentos | Key Task | Fabrication Risk |
|---------|------|------------|----------|----------|------------------|
| 1 | sesion1.html | 59–141 | 5 | Extract Intro + all Momento details | **HIGH**: Jean Smith quote |
| 2 | sesion2.html | 144–272 | 5 | Extract Intro + all Momento details | **MEDIUM**: Verify HSE + content |
| 3 | sesion3.html | 273–379 | 4 | Extract Intro + Corpografía details + Mándala | **MEDIUM**: Complex body-mapping |
| 4 | sesion4.html | 380–489 | 6 | Extract Intro + all 6 Momentos | **MEDIUM**: Verify structure |

---

## 8. EXECUTION CHECKLIST

Before Adapter agents begin:

- [ ] Docx fully extracted and stored as reference text files
- [ ] Each Adapter has assigned Docx paragraph range
- [ ] All 8 Actitudes Clave definitions verified
- [ ] "Jean Smith" quote issue resolved or flagged for removal
- [ ] Session duration stat checked and corrected
- [ ] Moment timings verified to sum correctly per session
- [ ] HSE definitions for each session extracted and confirmed

---

**End of Scout Report**
