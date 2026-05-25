# 📐 Academia CAS — Ley de Senos

Aplicación interactiva desarrollada con **Streamlit** para practicar la **Ley de Senos** en trigonometría. Genera ejercicios aleatorios con visualización geométrica y seguimiento del rendimiento del estudiante.

---

## 🖼️ Vista previa

```
┌─────────────────────────────────────┐
│  [Logo]  Academia CAS               │
│          Módulo de Trigonometría     │
├─────────────────────────────────────┤
│  Respondidas │ Correctas │ % Aciertos│
├─────────────────────────────────────┤
│         Triángulo SVG               │
│    A(45°)  ────────  B(60°)         │
│       \    a = 18   /               │
│        \           /                │
│    b=? · \         / c = 20         │
│            C(75°)                   │
├─────────────────────────────────────┤
│  ¿Cuánto mide el lado b?            │
│  [ Ingresa tu respuesta ] [Validar] │
└─────────────────────────────────────┘
```

---

## ✨ Características

- **Ejercicios aleatorios** — 6 variantes de pregunta con distintos ángulos y lados como incógnita
- **Visualización del triángulo** — arcos de ángulo dentro del triángulo, datos conocidos en color y desconocidos en gris con `?`
- **Solución paso a paso** en LaTeX — proporción, despeje y sustitución de valores
- **Control de rendimiento** — contador en tiempo real de respuestas correctas, incorrectas y porcentaje de aciertos
- **Resumen final** — badge de desempeño, detalle por pregunta y gráfico de dona
- **Logo personalizable** — coloca `Logo.png` en la carpeta del proyecto
- **Tolerancia de ±0.5** en las respuestas para aceptar redondeos

---

## 🗂️ Estructura del proyecto

```
LeyDeSenos/
├── leydesenos.py   # Aplicación principal
├── Logo.png        # Logo de Academia CAS (opcional)
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Streamlit 1.40 o superior

### Dependencias

```txt
streamlit
numpy
matplotlib
```

Instálalas con:

```bash
pip install streamlit numpy matplotlib
```

---

## 🚀 Ejecución

```bash
# Clona el repositorio
git clone https://github.com/tu-usuario/ley-de-senos.git
cd ley-de-senos

# Instala dependencias
pip install streamlit numpy matplotlib

# Ejecuta la app
streamlit run leydesenos.py
```

Abre tu navegador en `http://localhost:8501`.

---

## 🎮 Cómo usar la app

| Fase | Descripción |
|---|---|
| **Inicio** | Pantalla de bienvenida con la fórmula de referencia y botón para comenzar |
| **Actividad** | Triángulo aleatorio, ingresa tu respuesta y valida; avanza o finaliza cuando quieras |
| **Resumen** | Badge de desempeño, detalle de cada pregunta y gráfico de resultados |

### Variantes de ejercicio

La app genera aleatoriamente uno de estos 6 tipos de pregunta:

| Datos conocidos | Incógnita |
|---|---|
| Ángulo A, Ángulo B, lado a | lado b |
| Ángulo A, Ángulo B, lado b | lado a |
| Ángulo A, Ángulo C, lado a | lado c |
| Ángulo A, Ángulo C, lado c | lado a |
| Ángulo B, Ángulo C, lado b | lado c |
| Ángulo B, Ángulo C, lado c | lado b |

### Escala de rendimiento

| Porcentaje | Badge |
|---|---|
| ≥ 80% | 🏆 Excelente |
| 60–79% | 🥈 Bien |
| 40–59% | 🥉 Regular |
| < 40% | 📚 A repasar |

---

## 🧮 Fundamento matemático

La **Ley de Senos** establece que en cualquier triángulo:

$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}$$

donde $a$, $b$, $c$ son los lados opuestos a los ángulos $A$, $B$, $C$ respectivamente.

Para encontrar un lado desconocido, por ejemplo $b$:

$$b = \frac{a \cdot \sin B}{\sin A}$$

---

## 🖼️ Logo personalizado

Coloca un archivo llamado `Logo.png` en la misma carpeta que `leydesenos.py`. La app lo detecta automáticamente. Si no existe, muestra las siglas **CAS** como respaldo.

---

## 📄 Licencia

MIT © Academia CAS
