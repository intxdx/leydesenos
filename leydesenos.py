import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import io
import math
import os
import base64

st.set_page_config(page_title="Academia CAS — Ley de Senos", layout="centered")

# ══════════════════════════════════════════════════════════════════
# CSS global
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  /* ── Forzar modo claro completo (evita texto blanco en móvil) ── */
  .stApp, .stApp * { color-scheme: light !important; }
  .stApp {
    background: #f0f4ff !important;
  }

  /* Texto base siempre oscuro */
  .stApp p, .stApp span, .stApp div,
  .stApp label, .stApp li, .stApp h1,
  .stApp h2, .stApp h3, .stApp h4 {
    color: #1e293b !important;
  }

  /* Markdown nativo de Streamlit */
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] strong {
    color: #1e293b !important;
  }

  /* Títulos / subheaders */
  [data-testid="stHeadingWithActionElements"] h2,
  [data-testid="stHeadingWithActionElements"] h3 {
    color: #1e3a8a !important;
  }

  /* Captions */
  [data-testid="stCaptionContainer"] p { color: #64748b !important; }

  /* Info / success / error boxes */
  [data-testid="stAlert"] p { color: inherit !important; }

  /* Number input label */
  [data-testid="stNumberInput"] label { color: #1e293b !important; }

  /* Expander título */
  [data-testid="stExpander"] summary p { color: #1e293b !important; }

  /* header/logo */
  .cas-header {
    display: flex; align-items: center; gap: 18px;
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    border-radius: 16px; padding: 22px 28px; margin-bottom: 24px;
  }
  .cas-logo-circle {
    width: 64px; height: 64px; border-radius: 50%;
    background: white; display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
    font-size: 26px; font-weight: 900; color: #1e3a8a !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.25);
    font-family: Georgia, serif; letter-spacing: -1px;
  }
  .cas-header-text h1 {
    margin: 0; color: white !important; font-size: 22px; font-weight: 700;
  }
  .cas-header-text p {
    margin: 4px 0 0; color: #bfdbfe !important; font-size: 13px;
  }

  /* tarjeta de métricas */
  .metric-bar {
    display: flex; gap: 12px; margin-bottom: 18px; flex-wrap: wrap;
  }
  .metric-card {
    flex: 1; min-width: 100px; border-radius: 12px;
    padding: 14px 18px; text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,.08);
  }
  .metric-card .val {
    font-size: 30px; font-weight: 800; line-height: 1;
  }
  .metric-card .lbl {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .06em; margin-top: 4px;
  }
  .mc-total  { background:#eff6ff; }
  .mc-total .val  { color:#1d4ed8 !important; }
  .mc-total .lbl  { color:#3b82f6 !important; }
  .mc-ok    { background:#f0fdf4; }
  .mc-ok .val    { color:#16a34a !important; }
  .mc-ok .lbl    { color:#22c55e !important; }
  .mc-fail  { background:#fff1f2; }
  .mc-fail .val  { color:#dc2626 !important; }
  .mc-fail .lbl  { color:#f87171 !important; }
  .mc-pct   { background:#fdf4ff; }
  .mc-pct .val   { color:#7c3aed !important; }
  .mc-pct .lbl   { color:#a855f7 !important; }

  /* resumen final */
  .resumen-card {
    background: white; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,.1); margin-top: 8px;
  }
  .resumen-title {
    font-size: 22px; font-weight: 800; color: #1e3a8a !important;
    margin-bottom: 6px;
  }
  .resumen-sub {
    font-size: 14px; color: #64748b !important; margin-bottom: 20px;
  }
  .badge {
    display:inline-block; padding: 6px 16px; border-radius: 999px;
    font-size: 13px; font-weight: 700; letter-spacing:.03em;
  }
  .badge-gold   { background:#fef3c7; color:#92400e !important; }
  .badge-silver { background:#f1f5f9; color:#475569 !important; }
  .badge-bronze { background:#fdf4ff; color:#6d28d9 !important; }
  .badge-retry  { background:#fff1f2; color:#be123c !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# HEADER / LOGO
# ══════════════════════════════════════════════════════════════════
# Coloca logo.png en la misma carpeta que este archivo para mostrarlo.
_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")

if os.path.exists(_logo_path):
    with open(_logo_path, "rb") as _f:
        _logo_b64 = base64.b64encode(_f.read()).decode()
    _logo_html = f'<img src="data:image/png;base64,{_logo_b64}" style="width:64px;height:64px;object-fit:contain;border-radius:12px;" />'
else:
    _logo_html = '<div class="cas-logo-circle">CAS</div>'

st.markdown(f"""
<div class="cas-header">
  {_logo_html}
  <div class="cas-header-text">
    <h1>Academia CAS</h1>
    <p>Módulo de Trigonometría · Ley de Senos</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ESTADO DE LA APP
# ══════════════════════════════════════════════════════════════════
if 'fase' not in st.session_state:
    st.session_state.fase       = 'inicio'   # inicio | actividad | resumen
    st.session_state.correctas  = 0
    st.session_state.erroneas   = 0
    st.session_state.historial  = []          # lista de dicts por pregunta
    st.session_state.triangulo  = None
    st.session_state.respondido = False
    st.session_state.resp_user  = None

# ══════════════════════════════════════════════════════════════════
# TIPOS DE PREGUNTA
# ══════════════════════════════════════════════════════════════════
TIPOS = [
    {"pregunta": "Conoces **A**, **B** y el lado **a**. Calcula el lado **b**.",
     "incognita": "b", "conocidos_fig": ["A","B","a"], },
    {"pregunta": "Conoces **A**, **B** y el lado **b**. Calcula el lado **a**.",
     "incognita": "a", "conocidos_fig": ["A","B","b"], },
    {"pregunta": "Conoces **A**, **C** y el lado **a**. Calcula el lado **c**.",
     "incognita": "c", "conocidos_fig": ["A","C","a"], },
    {"pregunta": "Conoces **A**, **C** y el lado **c**. Calcula el lado **a**.",
     "incognita": "a", "conocidos_fig": ["A","C","c"], },
    {"pregunta": "Conoces **B**, **C** y el lado **b**. Calcula el lado **c**.",
     "incognita": "c", "conocidos_fig": ["B","C","b"], },
    {"pregunta": "Conoces **B**, **C** y el lado **c**. Calcula el lado **b**.",
     "incognita": "b", "conocidos_fig": ["B","C","c"], },
]

def nuevo_triangulo():
    A = random.randint(35, 75)
    B = random.randint(40, 75)
    C = 180 - A - B
    a = round(random.uniform(10.0, 25.0), 1)
    b = round((a * np.sin(np.radians(B))) / np.sin(np.radians(A)), 1)
    c = round((a * np.sin(np.radians(C))) / np.sin(np.radians(A)), 1)
    tipo = random.choice(TIPOS)
    return dict(A=A, B=B, C=C, a=a, b=b, c=c, tipo=tipo)

# ══════════════════════════════════════════════════════════════════
# HELPER: dibujar triángulo
# ══════════════════════════════════════════════════════════════════
def draw_triangle(t):
    conocidos = t['tipo']['conocidos_fig']
    vals = {k: t[k] for k in ['A','B','C','a','b','c']}

    xA, yA = 0, 0
    xB, yB = t['c'], 0
    xC = t['b'] * np.cos(np.radians(t['A']))
    yC = t['b'] * np.sin(np.radians(t['A']))

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#f8faff')
    ax.set_facecolor('#f8faff')
    ax.fill([xA,xB,xC],[yA,yB,yC], color='#dbeafe', alpha=.6, zorder=0)
    ax.plot([xA,xB,xC,xA],[yA,yB,yC,yA], color='#2563eb', linewidth=2.2)
    for px,py in [(xA,yA),(xB,yB),(xC,yC)]:
        ax.plot(px, py, 'o', color='#2563eb', markersize=5, zorder=5)

    S   = max(t['a'], t['b'], t['c'])
    r   = S * 0.09    # radio del arco de ángulo
    m   = S * 0.13    # distancia etiqueta ángulo hacia interior
    ms  = S * 0.07    # margen etiqueta lados

    # centroide — punto interior de referencia
    cx = (xA + xB + xC) / 3
    cy = (yA + yB + yC) / 3

    def lc(key): return {'a':'#1d4ed8','b':'#7c3aed','c':'#059669'}[key] if key in conocidos else '#adb5bd'
    def lv(key, unit):
        return (f"{key} = {vals[key]}{unit}" if key in conocidos else f"{key} = ?")

    # ── Ángulos: arco + etiqueta dentro del triángulo ──────────────
    ang_data = [
        ('A', t['A'], (xA,yA), (xB,yB), (xC,yC)),
        ('B', t['B'], (xB,yB), (xA,yA), (xC,yC)),
        ('C', t['C'], (xC,yC), (xA,yA), (xB,yB)),
    ]
    for name, deg, (px,py), (v1x,v1y), (v2x,v2y) in ang_data:
        a1 = math.degrees(math.atan2(v1y-py, v1x-px))
        a2 = math.degrees(math.atan2(v2y-py, v2x-px))
        th1, th2 = sorted([a1, a2])
        # si el arco corto no pasa por el interior, usar el complementario
        mid_angle = math.radians((th1 + th2) / 2)
        test_x = px + r * math.cos(mid_angle)
        test_y = py + r * math.sin(mid_angle)
        # verificar si el punto del arco está dentro del triángulo (producto cruzado)
        def sign(ax_,ay_,bx,by,px_,py_):
            return (bx-ax_)*(py_-ay_) - (by-ay_)*(px_-ax_)
        d1=sign(xA,yA,xB,yB,test_x,test_y)
        d2=sign(xB,yB,xC,yC,test_x,test_y)
        d3=sign(xC,yC,xA,yA,test_x,test_y)
        inside = (d1>=0 and d2>=0 and d3>=0) or (d1<=0 and d2<=0 and d3<=0)
        if not inside:
            # usar el arco opuesto
            th1, th2 = th2, th1+360

        known = name in conocidos
        arc_color  = '#d97706' if known else '#adb5bd'
        text_color = '#92400e' if known else '#868e96'
        bg_color   = '#fffbeb' if known else '#f8f9fa'

        arc = mpatches.Arc((px,py), r*2, r*2, angle=0,
                            theta1=th1, theta2=th2,
                            color=arc_color, linewidth=1.5, zorder=4)
        ax.add_patch(arc)

        # etiqueta hacia el centroide
        dx = cx - px; dy = cy - py
        dist = math.sqrt(dx**2 + dy**2)
        lx = px + (dx/dist)*m
        ly = py + (dy/dist)*m
        label = f"{deg}°" if known else "?°"
        ax.text(lx, ly, label, fontsize=9, ha='center', va='center',
                color=text_color, fontweight='bold', zorder=6,
                bbox=dict(boxstyle='round,pad=0.18', fc=bg_color, ec='none', alpha=.9))

    # ── Letras de vértice (fuera, en la punta) ──────────────────────
    vx_offset = S * 0.06
    # A: abajo-izquierda
    ax.text(xA - vx_offset, yA - vx_offset*0.5, 'A',
            fontsize=12, fontweight='bold', ha='right', va='top', color='#1e3a8a')
    # B: abajo-derecha
    ax.text(xB + vx_offset, yB - vx_offset*0.5, 'B',
            fontsize=12, fontweight='bold', ha='left',  va='top', color='#1e3a8a')
    # C: arriba-centro
    ax.text(xC, yC + vx_offset*0.5, 'C',
            fontsize=12, fontweight='bold', ha='center', va='bottom', color='#1e3a8a')

    # ── Lados (punto medio, desplazado al exterior) ─────────────────
    ax.text((xB+xC)/2 + ms, (yB+yC)/2,       lv('a',''), fontsize=10, color=lc('a'), ha='left')
    ax.text((xA+xC)/2 - ms, (yA+yC)/2,       lv('b',''), fontsize=10, color=lc('b'), ha='right')
    ax.text((xA+xB)/2,      yA - ms*1.4,      lv('c',''), fontsize=10, color=lc('c'), ha='center')

    ax.set_aspect('equal'); ax.axis('off')
    plt.tight_layout(pad=1.5)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0); plt.close(fig)
    return buf

# ══════════════════════════════════════════════════════════════════
# HELPER: barra de métricas
# ══════════════════════════════════════════════════════════════════
def mostrar_metricas():
    total = st.session_state.correctas + st.session_state.erroneas
    pct   = int(st.session_state.correctas/total*100) if total else 0
    st.markdown(f"""
    <div class="metric-bar">
      <div class="metric-card mc-total">
        <div class="val">{total}</div><div class="lbl">Respondidas</div>
      </div>
      <div class="metric-card mc-ok">
        <div class="val">{st.session_state.correctas}</div><div class="lbl">Correctas</div>
      </div>
      <div class="metric-card mc-fail">
        <div class="val">{st.session_state.erroneas}</div><div class="lbl">Incorrectas</div>
      </div>
      <div class="metric-card mc-pct">
        <div class="val">{pct}%</div><div class="lbl">Aciertos</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# FASE 1: PANTALLA DE INICIO
# ══════════════════════════════════════════════════════════════════
if st.session_state.fase == 'inicio':
    st.markdown("### Bienvenido a la actividad")
    st.write(
        "Practicarás la **Ley de Senos** resolviendo triángulos con datos aleatorios. "
        "En cada ejercicio se te mostrarán **dos ángulos y un lado** — tu tarea es "
        "calcular el lado faltante."
    )
    st.latex(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}")
    st.info("Ingresa tu respuesta y valida. Cuando quieras terminar, presiona **Finalizar actividad**.")
    st.markdown("")
    if st.button("🚀 Iniciar actividad", type="primary", width='stretch'):
        st.session_state.fase      = 'actividad'
        st.session_state.triangulo = nuevo_triangulo()
        st.session_state.respondido = False
        st.session_state.resp_user  = None
        st.rerun()

# ══════════════════════════════════════════════════════════════════
# FASE 2: ACTIVIDAD
# ══════════════════════════════════════════════════════════════════
elif st.session_state.fase == 'actividad':

    mostrar_metricas()

    t    = st.session_state.triangulo
    tipo = t['tipo']
    inc  = tipo['incognita']
    lado_opuesto = {'a':'A','b':'B','c':'C'}
    vals = {k: t[k] for k in ['A','B','C','a','b','c']}

    # conocidos para mostrar en columnas
    conocidos_ang = [k for k in ['A','B','C'] if k in tipo['conocidos_fig']]
    conocidos_lad = [k for k in ['a','b','c'] if k in tipo['conocidos_fig']]

    st.markdown("---")
    st.subheader("📐 Triángulo")
    st.image(draw_triangle(t), width='stretch')

    st.markdown("---")
    st.subheader("📝 El Reto")
    st.write(tipo['pregunta'])

    cols = st.columns(3)
    datos = [(k, f"{k} = {vals[k]}^\\circ") for k in conocidos_ang] + \
            [(k, f"{k} = {vals[k]}")         for k in conocidos_lad]
    for i, (_, ltx) in enumerate(datos):
        with cols[i]:
            st.latex(ltx)

    st.markdown(f"**¿Cuánto mide el lado {inc}?**")

    # ── Respuesta del usuario ──
    if not st.session_state.respondido:
        with st.form("respuesta_form"):
            resp = st.number_input(
                f"Tu respuesta para **{inc}**:",
                min_value=0.0, step=0.1, format="%.1f"
            )
            enviado = st.form_submit_button("✅ Validar respuesta", width='stretch')

        if enviado:
            correcto = abs(resp - vals[inc]) <= 0.5   # tolerancia ±0.5
            st.session_state.respondido = True
            st.session_state.resp_user  = resp
            if correcto:
                st.session_state.correctas += 1
            else:
                st.session_state.erroneas  += 1
            st.session_state.historial.append({
                'pregunta': tipo['pregunta'],
                'incognita': inc,
                'valor_correcto': vals[inc],
                'respuesta_user': resp,
                'correcto': correcto,
            })
            st.rerun()

    # ── Feedback post-respuesta ──
    else:
        resp = st.session_state.resp_user
        correcto = abs(resp - vals[inc]) <= 0.5

        if correcto:
            st.success(f"✅ ¡Correcto! **{inc} = {vals[inc]}**")
        else:
            st.error(f"❌ Incorrecto. Tu respuesta: **{resp}** · Valor correcto: **{vals[inc]}**")

        # Solución paso a paso
        with st.expander("🔍 Ver solución paso a paso"):
            par_con  = next(k for k in conocidos_lad if k != inc)
            ang_inc  = lado_opuesto[inc]
            ang_con  = lado_opuesto[par_con]
            sinA_v   = round(np.sin(np.radians(vals[ang_con])), 4)
            sinB_v   = round(np.sin(np.radians(vals[ang_inc])), 4)

            st.markdown("#### Paso 1 — Proporción aplicable")
            st.latex(rf"\frac{{{par_con}}}{{\sin({ang_con})}} = \frac{{{inc}}}{{\sin({ang_inc})}}")

            st.markdown("#### Paso 2 — Despejar la incógnita")
            st.latex(rf"{inc} = \frac{{{par_con} \cdot \sin({ang_inc})}}{{\sin({ang_con})}}")

            st.markdown("#### Paso 3 — Sustituir")
            st.latex(
                rf"{inc} = \frac{{{vals[par_con]} \cdot \sin({vals[ang_inc]}^\circ)}}{{\sin({vals[ang_con]}^\circ)}}"
                rf"= \frac{{{vals[par_con]} \times {sinB_v}}}{{{sinA_v}}}"
            )
            st.latex(rf"{inc} \approx {vals[inc]}")

        # Botones de navegación
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("➡️ Siguiente pregunta", width='stretch', type="primary"):
                st.session_state.triangulo  = nuevo_triangulo()
                st.session_state.respondido = False
                st.session_state.resp_user  = None
                st.rerun()
        with col_b:
            if st.button("🏁 Finalizar actividad", width='stretch'):
                st.session_state.fase = 'resumen'
                st.rerun()

# ══════════════════════════════════════════════════════════════════
# FASE 3: RESUMEN FINAL
# ══════════════════════════════════════════════════════════════════
elif st.session_state.fase == 'resumen':

    total     = st.session_state.correctas + st.session_state.erroneas
    correctas = st.session_state.correctas
    pct       = int(correctas/total*100) if total else 0

    if pct >= 80:
        badge_cls, badge_txt, emoji = "badge-gold",   "Excelente", "🏆"
    elif pct >= 60:
        badge_cls, badge_txt, emoji = "badge-silver", "Bien",      "🥈"
    elif pct >= 40:
        badge_cls, badge_txt, emoji = "badge-bronze", "Regular",   "🥉"
    else:
        badge_cls, badge_txt, emoji = "badge-retry",  "A repasar", "📚"

    st.markdown(f"""
    <div class="resumen-card">
      <div class="resumen-title">{emoji} Resumen de la actividad</div>
      <div class="resumen-sub">Academia CAS · Ley de Senos</div>
      <span class="badge {badge_cls}">{badge_txt} — {pct}% de aciertos</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    mostrar_metricas()

    # Detalle por pregunta
    st.markdown("### 📋 Detalle de respuestas")
    for i, h in enumerate(st.session_state.historial, 1):
        icono = "✅" if h['correcto'] else "❌"
        with st.expander(f"{icono} Pregunta {i} — lado **{h['incognita']}**"):
            st.write(h['pregunta'])
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tu respuesta", h['respuesta_user'])
            with col2:
                st.metric("Valor correcto", h['valor_correcto'])
            if h['correcto']:
                st.success("Respuesta correcta ✅")
            else:
                st.error(f"Respuesta incorrecta — el valor era **{h['valor_correcto']}**")

    # Gráfico de rendimiento
    if total > 0:
        st.markdown("### 📊 Distribución de resultados")
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        fig2.patch.set_facecolor('#f0f4ff')
        ax2.set_facecolor('#f0f4ff')
        sizes  = [correctas, total - correctas]
        labels = [f"Correctas\n{correctas}", f"Incorrectas\n{total-correctas}"]
        colors = ['#22c55e', '#f87171']
        wedges, texts = ax2.pie(
            sizes, labels=labels, colors=colors,
            startangle=90, wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
            textprops=dict(fontsize=12)
        )
        ax2.text(0, 0, f"{pct}%", ha='center', va='center',
                 fontsize=22, fontweight='bold', color='#1e3a8a')
        ax2.set_title("Aciertos", fontsize=13, color='#1e3a8a', pad=12)
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format='png', dpi=130, bbox_inches='tight',
                     facecolor=fig2.get_facecolor())
        buf2.seek(0); plt.close(fig2)
        col_g, _ = st.columns([1, 1])
        with col_g:
            st.image(buf2)

    st.markdown("---")
    if st.button("🔄 Nueva actividad", type="primary", width='stretch'):
        for key in ['fase','correctas','erroneas','historial','triangulo','respondido','resp_user']:
            st.session_state.pop(key, None)
        st.rerun()
