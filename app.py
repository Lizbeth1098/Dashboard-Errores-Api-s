# -*- coding: utf-8 -*-
"""
🏥 DASHBOARD DE ERRORES API - PROA/CHOPO
=========================================
Versión 6.0 PRO - Optimizado para Streamlit Cloud

Características:
- Diseño moderno y responsivo
- Navegación intuitiva
- Gráficos interactivos
- Filtros avanzados
- KPIs destacados

Autor: Lizbeth Ramírez | PROA - Ecommerce
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Monitor API - PROA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Dashboard de Monitoreo de Errores API - PROA/CHOPO v6.0"
    }
)

# ============================================
# PALETA DE COLORES PROA
# ============================================
COLORS = {
    'bg_dark': '#0A1628',
    'bg_card': '#0D1B2A',
    'border': '#1B3A5C',
    'blue': '#0066B3',
    'blue_light': '#3B9EE8',
    'cyan': '#00B4D8',
    'white': '#FFFFFF',
    'gray': '#8B9AAF',
    'green': '#10B981',
    'yellow': '#F59E0B',
    'red': '#EF4444',
    'purple': '#8B5CF6',
}

# ============================================
# CSS PROFESIONAL
# ============================================
st.markdown(f"""
<style>
    /* === TEMA OSCURO PROA === */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_dark']} 0%, #061220 100%);
    }}
    
    /* Header Principal */
    .main-header {{
        background: linear-gradient(90deg, {COLORS['bg_card']} 0%, {COLORS['bg_dark']} 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .logo-section {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .logo {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['cyan']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .subtitle {{
        color: {COLORS['gray']};
        font-size: 0.85rem;
    }}
    
    /* KPI Cards */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .kpi-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 102, 179, 0.2);
        border-color: {COLORS['blue_light']};
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {COLORS['blue']} 0%, {COLORS['cyan']} 100%);
    }}
    
    .kpi-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }}
    
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['white']};
        line-height: 1.2;
    }}
    
    .kpi-label {{
        color: {COLORS['gray']};
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .kpi-trend {{
        font-size: 0.75rem;
        margin-top: 0.3rem;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        display: inline-block;
    }}
    
    .trend-up {{ background: rgba(239, 68, 68, 0.2); color: {COLORS['red']}; }}
    .trend-down {{ background: rgba(16, 185, 129, 0.2); color: {COLORS['green']}; }}
    
    /* Alerta Crítica */
    .critical-banner {{
        background: linear-gradient(135deg, {COLORS['red']} 0%, #DC2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
        50% {{ box-shadow: 0 0 20px 10px rgba(239, 68, 68, 0); }}
    }}
    
    /* Section Cards */
    .section-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    .section-title {{
        color: {COLORS['white']};
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Top Messages */
    .message-item {{
        background: rgba(0, 102, 179, 0.1);
        border: 1px solid {COLORS['border']};
        border-left: 4px solid {COLORS['blue_light']};
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        color: {COLORS['white']};
        font-size: 0.85rem;
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
    }}
    
    .message-rank {{
        background: {COLORS['blue']};
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        flex-shrink: 0;
    }}
    
    .message-count {{
        background: {COLORS['cyan']};
        color: {COLORS['bg_dark']};
        padding: 0.15rem 0.5rem;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-left: auto;
        flex-shrink: 0;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {COLORS['bg_card']};
    }}
    
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['white']};
    }}
    
    /* Sidebar Logo */
    .sidebar-logo {{
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['blue_light']} 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}
    
    .sidebar-logo h2 {{
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }}
    
    .sidebar-logo p {{
        color: rgba(255,255,255,0.8);
        margin: 0;
        font-size: 0.75rem;
    }}
    
    /* Filter Section */
    .filter-section {{
        background: rgba(0, 102, 179, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    
    .filter-title {{
        color: {COLORS['cyan']};
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    /* Error Type Card */
    .error-type-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s;
    }}
    
    .error-type-card:hover {{
        border-color: {COLORS['blue_light']};
        background: rgba(0, 102, 179, 0.1);
    }}
    
    /* Data Status */
    .data-status {{
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid {COLORS['green']};
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: {COLORS['green']};
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }}
    
    /* Empty State */
    .empty-state {{
        text-align: center;
        padding: 3rem;
        color: {COLORS['gray']};
    }}
    
    .empty-state h3 {{
        color: {COLORS['white']};
        margin-bottom: 1rem;
    }}
    
    /* Tabs customization */
    .stTabs [data-baseweb="tab-list"] {{
        background: {COLORS['bg_card']};
        border-radius: 10px;
        padding: 0.3rem;
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {COLORS['gray']};
        border-radius: 8px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['blue']};
        color: white;
    }}
    
    /* Download Button */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['cyan']} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .kpi-container {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATOS DE EJEMPLO (para demo)
# ============================================
@st.cache_data
def generar_datos_demo():
    """Genera datos de ejemplo para demostración"""
    import random
    
    tipos = ['DOCUMENTO_NO_ENCONTRADO', 'ERROR_AUTENTICACION', 'TIMEOUT', 'ESTUDIO_NO_DISPONIBLE', 
             'PROMOCION_ERROR', 'PACIENTE_NO_ENCONTRADO', 'ERROR_SERVIDOR', 'NO_CLASIFICADO']
    severidades = ['CRITICA', 'ALTA', 'MEDIA', 'BAJA']
    mensajes = [
        "El estudio 15166 DETECCIÓN DE ANTÍGENO no se encuentra activo",
        "El código de promoción 203174 no se encuentra vigente",
        "No se encontraron resultados para el entidadId solicitado",
        "El código de promoción 203088 no está asociado a la sucursal",
        "Error de autenticación: Token expirado",
        "Timeout al conectar con el servidor",
        "Paciente no encontrado en el sistema",
        "Error interno del servidor 500"
    ]
    
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(500):
        fecha = base_date + timedelta(days=random.randint(0, 30), hours=random.randint(6, 22))
        tipo = random.choice(tipos)
        
        if tipo in ['ERROR_AUTENTICACION', 'ERROR_SERVIDOR']:
            severidad = 'CRITICA'
        elif tipo == 'TIMEOUT':
            severidad = 'ALTA'
        elif tipo in ['DOCUMENTO_NO_ENCONTRADO', 'ESTUDIO_NO_DISPONIBLE']:
            severidad = 'MEDIA'
        else:
            severidad = random.choice(severidades)
        
        data.append({
            'fecha': fecha,
            'tipo_error': tipo,
            'severidad': severidad,
            'error_message': random.choice(mensajes),
            'entidad_id': str(random.randint(100000, 999999)),
            'api_endpoint': random.choice(['GetDocument', 'CreateOrder', 'ValidatePromo', 'GetPatient'])
        })
    
    return pd.DataFrame(data)

# ============================================
# FUNCIONES DE CARGA
# ============================================
def cargar_excel(archivo):
    """Carga y procesa archivo Excel"""
    try:
        xl = pd.ExcelFile(archivo)
        hojas = xl.sheet_names
        
        # Buscar hoja con datos
        for hoja in ['Todos los Errores', 'Sheet1', 'Hoja1'] + hojas:
            if hoja in hojas:
                df = pd.read_excel(archivo, sheet_name=hoja)
                if len(df) > 0:
                    break
        else:
            df = pd.read_excel(archivo, sheet_name=0)
        
        # Procesar fechas
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar archivo: {e}")
        return None

# ============================================
# COMPONENTES UI
# ============================================
def render_header(total_errores, errores_mes):
    """Renderiza el header principal"""
    st.markdown(f"""
    <div class="main-header">
        <div class="logo-section">
            <div>
                <div class="logo">✦ PROA</div>
                <div class="subtitle">Grupo Diagnóstico | Monitor de API</div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: {COLORS['gray']}; font-size: 0.8rem;">ERRORES ESTE MES</div>
            <div style="color: {COLORS['cyan']}; font-size: 2rem; font-weight: 700;">{errores_mes:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(df):
    """Renderiza los KPIs principales"""
    total = len(df)
    criticos = len(df[df['severidad'] == 'CRITICA']) if 'severidad' in df.columns else 0
    altos = len(df[df['severidad'] == 'ALTA']) if 'severidad' in df.columns else 0
    medios = len(df[df['severidad'] == 'MEDIA']) if 'severidad' in df.columns else 0
    bajos = len(df[df['severidad'] == 'BAJA']) if 'severidad' in df.columns else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📧</div>
            <div class="kpi-value" style="color: {COLORS['cyan']};">{total:,}</div>
            <div class="kpi-label">Total Errores</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-value" style="color: {COLORS['red']};">{criticos}</div>
            <div class="kpi-label">Críticos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟠</div>
            <div class="kpi-value" style="color: {COLORS['yellow']};">{altos}</div>
            <div class="kpi-label">Altos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟡</div>
            <div class="kpi-value" style="color: {COLORS['blue_light']};">{medios}</div>
            <div class="kpi-label">Medios</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟢</div>
            <div class="kpi-value" style="color: {COLORS['green']};">{bajos}</div>
            <div class="kpi-label">Bajos</div>
        </div>
        """, unsafe_allow_html=True)

def render_alerta_criticos(cantidad):
    """Renderiza banner de alerta si hay críticos"""
    if cantidad > 0:
        st.markdown(f"""
        <div class="critical-banner">
            <span style="font-size: 1.5rem;">⚠️</span>
            <span>¡ALERTA! {cantidad} errores críticos requieren atención inmediata</span>
        </div>
        """, unsafe_allow_html=True)

def render_top_mensajes(df):
    """Renderiza el top 5 de mensajes más repetidos"""
    if 'error_message' not in df.columns:
        return
    
    mensajes = df['error_message'].dropna()
    mensajes = mensajes[mensajes != '']
    
    if len(mensajes) == 0:
        return
    
    top = mensajes.value_counts().head(5)
    
    st.markdown(f'<div class="section-title">🔝 Top 5 Mensajes Más Frecuentes</div>', unsafe_allow_html=True)
    
    for i, (msg, count) in enumerate(top.items(), 1):
        msg_corto = str(msg)[:100] + "..." if len(str(msg)) > 100 else str(msg)
        st.markdown(f"""
        <div class="message-item">
            <div class="message-rank">{i}</div>
            <div style="flex: 1;">{msg_corto}</div>
            <div class="message-count">{count}x</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# GRÁFICOS
# ============================================
def grafico_tendencia_diaria(df):
    """Gráfico de línea: errores por día"""
    if 'fecha' not in df.columns:
        return None
    
    df_temp = df.copy()
    df_temp['dia'] = df_temp['fecha'].dt.date
    por_dia = df_temp.groupby('dia').size().reset_index(name='Errores')
    por_dia['dia'] = pd.to_datetime(por_dia['dia'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=por_dia['dia'],
        y=por_dia['Errores'],
        mode='lines+markers',
        line=dict(color=COLORS['cyan'], width=3),
        marker=dict(size=8, color=COLORS['cyan']),
        fill='tozeroy',
        fillcolor='rgba(0, 180, 216, 0.1)',
        hovertemplate='<b>%{x|%d %b}</b><br>Errores: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📅 Tendencia Diaria', font=dict(color=COLORS['white'], size=16)),
        xaxis=dict(
            title='',
            color=COLORS['gray'],
            gridcolor=COLORS['border'],
            tickformat='%d %b'
        ),
        yaxis=dict(title='', color=COLORS['gray'], gridcolor=COLORS['border']),
        height=350,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=50, b=40),
        hovermode='x unified'
    )
    
    return fig

def grafico_por_tipo(df):
    """Gráfico de barras: errores por tipo"""
    if 'tipo_error' not in df.columns:
        return None
    
    conteo = df['tipo_error'].value_counts().reset_index()
    conteo.columns = ['Tipo', 'Cantidad']
    
    # Colores por tipo
    colores = [COLORS['blue_light']] * len(conteo)
    
    fig = go.Figure(go.Bar(
        x=conteo['Cantidad'],
        y=conteo['Tipo'],
        orientation='h',
        marker=dict(
            color=conteo['Cantidad'],
            colorscale=[[0, COLORS['blue']], [0.5, COLORS['blue_light']], [1, COLORS['cyan']]],
            line=dict(color=COLORS['border'], width=1)
        ),
        text=conteo['Cantidad'],
        textposition='auto',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='📊 Errores por Tipo', font=dict(color=COLORS['white'], size=16)),
        xaxis=dict(title='', color=COLORS['gray'], gridcolor=COLORS['border']),
        yaxis=dict(title='', color=COLORS['white'], categoryorder='total ascending'),
        height=400,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def grafico_severidad(df):
    """Gráfico de dona: distribución por severidad"""
    if 'severidad' not in df.columns:
        return None
    
    conteo = df['severidad'].value_counts().reset_index()
    conteo.columns = ['Severidad', 'Cantidad']
    
    colores_map = {
        'CRITICA': COLORS['red'],
        'ALTA': COLORS['yellow'],
        'MEDIA': COLORS['blue_light'],
        'BAJA': COLORS['green']
    }
    colores = [colores_map.get(s, COLORS['gray']) for s in conteo['Severidad']]
    
    fig = go.Figure(go.Pie(
        labels=conteo['Severidad'],
        values=conteo['Cantidad'],
        hole=0.6,
        marker=dict(colors=colores, line=dict(color=COLORS['bg_dark'], width=2)),
        textinfo='label+percent',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='🎯 Distribución por Severidad', font=dict(color=COLORS['white'], size=16)),
        height=350,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color=COLORS['white']), orientation='h', y=-0.1),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def grafico_por_hora(df):
    """Gráfico de barras: errores por hora"""
    if 'fecha' not in df.columns:
        return None
    
    df_temp = df.copy()
    df_temp['hora'] = df_temp['fecha'].dt.hour
    por_hora = df_temp.groupby('hora').size().reset_index(name='Errores')
    
    fig = go.Figure(go.Bar(
        x=por_hora['hora'],
        y=por_hora['Errores'],
        marker=dict(
            color=por_hora['Errores'],
            colorscale=[[0, COLORS['blue']], [1, COLORS['cyan']]]
        ),
        text=por_hora['Errores'],
        textposition='outside',
        textfont=dict(color=COLORS['white'], size=10),
        hovertemplate='<b>%{x}:00</b><br>Errores: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='🕐 Distribución por Hora', font=dict(color=COLORS['white'], size=16)),
        xaxis=dict(
            title='Hora',
            color=COLORS['gray'],
            gridcolor=COLORS['border'],
            tickmode='linear',
            dtick=2
        ),
        yaxis=dict(title='', color=COLORS['gray'], gridcolor=COLORS['border']),
        height=300,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=50, b=40)
    )
    
    return fig

def grafico_top_mensajes(df):
    """Gráfico de barras: top 5 mensajes"""
    if 'error_message' not in df.columns:
        return None
    
    mensajes = df['error_message'].dropna()
    mensajes = mensajes[mensajes != '']
    
    if len(mensajes) == 0:
        return None
    
    top = mensajes.value_counts().head(5)
    labels = [m[:40] + "..." if len(str(m)) > 40 else str(m) for m in top.index]
    
    fig = go.Figure(go.Bar(
        x=top.values,
        y=labels,
        orientation='h',
        marker=dict(
            color=top.values,
            colorscale=[[0, COLORS['blue']], [1, COLORS['cyan']]]
        ),
        text=top.values,
        textposition='auto',
        textfont=dict(color='white'),
        hovertemplate='<b>%{y}</b><br>Repeticiones: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='🔝 Top 5 Mensajes', font=dict(color=COLORS['white'], size=16)),
        xaxis=dict(title='', color=COLORS['gray'], gridcolor=COLORS['border']),
        yaxis=dict(title='', color=COLORS['white'], categoryorder='total ascending'),
        height=350,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

# ============================================
# MAIN APP
# ============================================
def main():
    # Estado de la sesión
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>✦ PROA</h2>
            <p>Grupo Diagnóstico</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div class='filter-title'>📁 Cargar Datos</div>", unsafe_allow_html=True)
        
        archivo = st.file_uploader(
            "Sube tu archivo Excel",
            type=['xlsx', 'xls'],
            help="Sube el Excel generado por el analizador"
        )
        
        usar_demo = st.checkbox("📊 Usar datos de demostración", value=st.session_state.df is None and archivo is None)
        
        st.markdown("---")
        
        # Filtros
        st.markdown(f"<div class='filter-title'>⚙️ Filtros</div>", unsafe_allow_html=True)
        
        filtro_severidad = st.multiselect(
            "Severidad:",
            ['CRITICA', 'ALTA', 'MEDIA', 'BAJA'],
            default=['CRITICA', 'ALTA', 'MEDIA', 'BAJA']
        )
        
        # Rango de fechas
        usar_rango = st.checkbox("📅 Filtrar por fecha")
        fecha_inicio = None
        fecha_fin = None
        
        if usar_rango:
            col1, col2 = st.columns(2)
            with col1:
                fecha_inicio = st.date_input("Desde", value=datetime.now() - timedelta(days=30))
            with col2:
                fecha_fin = st.date_input("Hasta", value=datetime.now())
        
        st.markdown("---")
        
        # Info
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <p style="color: {COLORS['blue_light']}; font-weight: 600;">👩‍💻 Lizbeth Ramírez</p>
            <p style="color: {COLORS['gray']}; font-size: 0.8rem;">PROA - Ecommerce</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== CARGAR DATOS ==========
    df = None
    
    if archivo:
        df = cargar_excel(archivo)
        st.session_state.df = df
    elif usar_demo:
        df = generar_datos_demo()
    elif st.session_state.df is not None:
        df = st.session_state.df
    
    # ========== HEADER ==========
    errores_mes = 0
    if df is not None and 'fecha' in df.columns:
        mes_actual = datetime.now().month
        errores_mes = len(df[df['fecha'].dt.month == mes_actual])
    
    render_header(len(df) if df is not None else 0, errores_mes)
    
    # ========== SIN DATOS ==========
    if df is None or len(df) == 0:
        st.markdown(f"""
        <div class="empty-state">
            <h3>📤 Carga un archivo para comenzar</h3>
            <p>Sube el Excel generado por el analizador de errores API<br>
            o activa "Usar datos de demostración" para explorar el dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ========== APLICAR FILTROS ==========
    if 'severidad' in df.columns and filtro_severidad:
        df = df[df['severidad'].isin(filtro_severidad)]
    
    if usar_rango and 'fecha' in df.columns and fecha_inicio and fecha_fin:
        df = df[(df['fecha'].dt.date >= fecha_inicio) & (df['fecha'].dt.date <= fecha_fin)]
    
    # ========== CONTENIDO PRINCIPAL ==========
    
    # Alerta de críticos
    criticos = len(df[df['severidad'] == 'CRITICA']) if 'severidad' in df.columns else 0
    render_alerta_criticos(criticos)
    
    # KPIs
    render_kpis(df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== GRÁFICOS FILA 1 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        fig = grafico_tendencia_diaria(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = grafico_severidad(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== GRÁFICOS FILA 2 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        fig = grafico_por_tipo(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = grafico_top_mensajes(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== POR HORA ==========
    fig = grafico_por_hora(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== TABS: DETALLES ==========
    tab1, tab2, tab3 = st.tabs(["📋 Top Mensajes", "🔍 Explorar Datos", "📊 Resumen"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            render_top_mensajes(df)
        with col2:
            # Tabla resumen por tipo
            if 'tipo_error' in df.columns:
                st.markdown(f'<div class="section-title">📊 Resumen por Tipo</div>', unsafe_allow_html=True)
                resumen = df['tipo_error'].value_counts().reset_index()
                resumen.columns = ['Tipo de Error', 'Cantidad']
                resumen['%'] = (resumen['Cantidad'] / len(df) * 100).round(1).astype(str) + '%'
                st.dataframe(resumen, use_container_width=True, hide_index=True)
    
    with tab2:
        # Filtro por tipo
        if 'tipo_error' in df.columns:
            tipo_sel = st.selectbox("Filtrar por tipo:", ["Todos"] + list(df['tipo_error'].unique()))
            
            if tipo_sel != "Todos":
                df_filtrado = df[df['tipo_error'] == tipo_sel]
            else:
                df_filtrado = df
            
            st.dataframe(df_filtrado, use_container_width=True, height=400)
    
    with tab3:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Errores", f"{len(df):,}")
            if 'fecha' in df.columns:
                st.metric("Fecha más antigua", df['fecha'].min().strftime('%d/%m/%Y'))
        
        with col2:
            if 'tipo_error' in df.columns:
                st.metric("Tipos únicos", df['tipo_error'].nunique())
            if 'fecha' in df.columns:
                st.metric("Fecha más reciente", df['fecha'].max().strftime('%d/%m/%Y'))
        
        with col3:
            if 'api_endpoint' in df.columns:
                st.metric("APIs afectadas", df['api_endpoint'].nunique())
            if 'fecha' in df.columns:
                dias = (df['fecha'].max() - df['fecha'].min()).days + 1
                st.metric("Promedio/día", f"{len(df)/max(dias,1):.0f}")
    
    # ========== DESCARGAR ==========
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV",
            csv,
            f"errores_proa_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    main()
