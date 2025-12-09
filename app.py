# -*- coding: utf-8 -*-
"""
🏥 DASHBOARD DE ERRORES API - PROA/CHOPO
=========================================
Versión 9.0 - Mejoras de visualización

Autor: Lizbeth Ramírez | PROA - Ecommerce
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="Monitor API - PROA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🔗 TU GOOGLE SHEET
# ============================================
GOOGLE_SHEET_ID = "1ycVV-aBUBhlPdJk9s3wSvaZflyMbSpmG1OpmB9rZof8"
GOOGLE_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"

# ============================================
# COLORES PROA
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
}

# Nombres de meses en español
MESES_ES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# ============================================
# CSS
# ============================================
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_dark']} 0%, #061220 100%);
    }}
    
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
    
    .kpi-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-top: 3px solid {COLORS['blue']};
    }}
    
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['white']};
    }}
    
    .kpi-label {{
        color: {COLORS['gray']};
        font-size: 0.8rem;
        text-transform: uppercase;
    }}
    
    .critical-banner {{
        background: linear-gradient(135deg, {COLORS['red']} 0%, #DC2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }}
    
    .info-box {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-left: 4px solid {COLORS['cyan']};
        padding: 1rem;
        border-radius: 8px;
        color: {COLORS['white']};
        margin-bottom: 1rem;
    }}
    
    section[data-testid="stSidebar"] {{
        background: {COLORS['bg_card']};
    }}
    
    .sidebar-logo {{
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, {COLORS['blue']} 0%, {COLORS['blue_light']} 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}
    
    .sidebar-logo h2 {{
        color: white;
        margin: 0;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ============================================
# CARGAR DATOS DESDE GOOGLE SHEETS
# ============================================
@st.cache_data(ttl=300)
def cargar_google_sheet():
    """Carga datos desde Google Sheets"""
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        df = df.dropna(how='all')
        
        return df, None
    except Exception as e:
        return None, str(e)

# ============================================
# COMPONENTES UI
# ============================================
def render_header(errores_mes):
    st.markdown(f"""
    <div class="main-header">
        <div>
            <div class="logo">✦ PROA</div>
            <div class="subtitle">Grupo Diagnóstico | Monitor de API</div>
        </div>
        <div style="text-align: right;">
            <div style="color: {COLORS['gray']}; font-size: 0.8rem;">ERRORES ESTE MES</div>
            <div style="color: {COLORS['cyan']}; font-size: 2rem; font-weight: 700;">{errores_mes:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(df):
    total = len(df)
    criticos = len(df[df['severidad'] == 'CRITICA']) if 'severidad' in df.columns else 0
    altos = len(df[df['severidad'] == 'ALTA']) if 'severidad' in df.columns else 0
    medios = len(df[df['severidad'] == 'MEDIA']) if 'severidad' in df.columns else 0
    bajos = len(df[df['severidad'] == 'BAJA']) if 'severidad' in df.columns else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {COLORS['cyan']};">📧 {total:,}</div>
            <div class="kpi-label">Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {COLORS['red']};">🔴 {criticos}</div>
            <div class="kpi-label">Críticos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {COLORS['yellow']};">🟠 {altos}</div>
            <div class="kpi-label">Altos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {COLORS['blue_light']};">🟡 {medios}</div>
            <div class="kpi-label">Medios</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {COLORS['green']};">🟢 {bajos}</div>
            <div class="kpi-label">Bajos</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# GRÁFICOS
# ============================================
def grafico_tendencia_diaria(df):
    """Tendencia diaria del mes seleccionado"""
    if 'fecha' not in df.columns or df['fecha'].isna().all():
        return None
    
    df_temp = df.dropna(subset=['fecha']).copy()
    df_temp['dia'] = df_temp['fecha'].dt.day
    por_dia = df_temp.groupby('dia').size().reset_index(name='Errores')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=por_dia['dia'],
        y=por_dia['Errores'],
        mode='lines+markers',
        line=dict(color=COLORS['cyan'], width=2),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(0, 180, 216, 0.1)'
    ))
    
    fig.update_layout(
        title='📅 Errores por Día del Mes',
        xaxis=dict(title='Día', gridcolor=COLORS['border'], tickmode='linear', dtick=1),
        yaxis=dict(title='', gridcolor=COLORS['border']),
        height=350,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

def grafico_por_tipo(df):
    if 'tipo_error' not in df.columns:
        return None
    
    conteo = df['tipo_error'].value_counts().head(10).reset_index()
    conteo.columns = ['Tipo', 'Cantidad']
    
    fig = go.Figure(go.Bar(
        x=conteo['Cantidad'],
        y=conteo['Tipo'],
        orientation='h',
        marker=dict(color=conteo['Cantidad'], colorscale=[[0, COLORS['blue']], [1, COLORS['cyan']]]),
        text=conteo['Cantidad'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='📊 Top 10 Tipos de Error',
        xaxis=dict(title='', gridcolor=COLORS['border']),
        yaxis=dict(title='', categoryorder='total ascending'),
        height=400,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

def grafico_severidad(df):
    if 'severidad' not in df.columns:
        return None
    
    conteo = df['severidad'].value_counts().reset_index()
    conteo.columns = ['Severidad', 'Cantidad']
    
    colores_map = {'CRITICA': COLORS['red'], 'ALTA': COLORS['yellow'], 
                   'MEDIA': COLORS['blue_light'], 'BAJA': COLORS['green']}
    colores = [colores_map.get(s, COLORS['gray']) for s in conteo['Severidad']]
    
    fig = go.Figure(go.Pie(
        labels=conteo['Severidad'],
        values=conteo['Cantidad'],
        hole=0.6,
        marker=dict(colors=colores)
    ))
    
    fig.update_layout(
        title='🎯 Distribución por Severidad',
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

def grafico_mensajes_error(df):
    """Gráfico de los mensajes de error más frecuentes"""
    if 'error_message' not in df.columns:
        return None
    
    msgs = df['error_message'].dropna()
    msgs = msgs[msgs != '']
    
    if len(msgs) == 0:
        return None
    
    conteo = msgs.value_counts().head(10).reset_index()
    conteo.columns = ['Mensaje', 'Cantidad']
    
    # Truncar mensajes largos
    conteo['Mensaje_corto'] = conteo['Mensaje'].apply(lambda x: x[:50] + '...' if len(str(x)) > 50 else x)
    
    fig = go.Figure(go.Bar(
        x=conteo['Cantidad'],
        y=conteo['Mensaje_corto'],
        orientation='h',
        marker=dict(color=conteo['Cantidad'], colorscale=[[0, COLORS['red']], [1, COLORS['yellow']]]),
        text=conteo['Cantidad'],
        textposition='auto',
        hovertext=conteo['Mensaje'],  # Mensaje completo en hover
        hoverinfo='text+x'
    ))
    
    fig.update_layout(
        title='💬 Top 10 Mensajes de Error',
        xaxis=dict(title='', gridcolor=COLORS['border']),
        yaxis=dict(title='', categoryorder='total ascending'),
        height=400,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

def grafico_por_hora(df):
    if 'fecha' not in df.columns or df['fecha'].isna().all():
        return None
    
    df_temp = df.dropna(subset=['fecha']).copy()
    df_temp['hora'] = df_temp['fecha'].dt.hour
    por_hora = df_temp.groupby('hora').size().reset_index(name='Errores')
    
    fig = go.Figure(go.Bar(
        x=por_hora['hora'],
        y=por_hora['Errores'],
        marker=dict(color=por_hora['Errores'], colorscale=[[0, COLORS['blue']], [1, COLORS['cyan']]]),
        text=por_hora['Errores'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='🕐 Errores por Hora del Día',
        xaxis=dict(title='Hora', gridcolor=COLORS['border'], tickmode='linear', dtick=2),
        yaxis=dict(title='', gridcolor=COLORS['border']),
        height=300,
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

# ============================================
# MAIN
# ============================================
def main():
    # ========== CARGAR DATOS PRIMERO ==========
    df_completo, error_carga = cargar_google_sheet()
    
    # Obtener meses disponibles
    meses_disponibles = []
    if df_completo is not None and 'fecha' in df_completo.columns and not df_completo['fecha'].isna().all():
        df_completo['año_mes'] = df_completo['fecha'].dt.to_period('M')
        meses_unicos = df_completo['año_mes'].dropna().unique()
        meses_ordenados = sorted(meses_unicos, reverse=True)
        
        for m in meses_ordenados:
            año = m.year
            mes = m.month
            nombre = f"{MESES_ES[mes]} {año}"
            meses_disponibles.append((nombre, año, mes))
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>✦ PROA</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.8rem;">Grupo Diagnóstico</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📅 Período")
        
        # Selector de mes (por defecto el actual)
        if meses_disponibles:
            opciones_mes = [m[0] for m in meses_disponibles]
            mes_seleccionado_idx = st.selectbox(
                "Selecciona mes:",
                range(len(opciones_mes)),
                format_func=lambda x: opciones_mes[x],
                index=0  # El primero es el más reciente
            )
            
            _, año_sel, mes_sel = meses_disponibles[mes_seleccionado_idx]
        else:
            año_sel = datetime.now().year
            mes_sel = datetime.now().month
        
        # Opción para ver histórico completo
        ver_historico = st.checkbox("📊 Ver histórico completo", value=False)
        
        st.markdown("---")
        
        # Filtros
        st.markdown("### ⚙️ Filtros")
        
        filtro_severidad = st.multiselect(
            "Severidad:",
            ['CRITICA', 'ALTA', 'MEDIA', 'BAJA'],
            default=['CRITICA', 'ALTA', 'MEDIA', 'BAJA']
        )
        
        st.markdown("---")
        
        # Botón refrescar
        if st.button("🔄 Actualizar datos"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: {COLORS['blue_light']}; font-weight: 600;">👩‍💻 Lizbeth Ramírez</p>
            <p style="color: {COLORS['gray']}; font-size: 0.8rem;">PROA - Ecommerce</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== FILTRAR POR MES ==========
    df = df_completo.copy() if df_completo is not None else None
    
    if df is not None and not ver_historico and 'fecha' in df.columns:
        df = df[(df['fecha'].dt.year == año_sel) & (df['fecha'].dt.month == mes_sel)]
    
    # ========== HEADER ==========
    errores_mes = len(df) if df is not None else 0
    render_header(errores_mes)
    
    # ========== SIN DATOS ==========
    if df is None or len(df) == 0:
        st.warning("⚠️ No hay datos disponibles para el período seleccionado.")
        return
    
    # ========== APLICAR FILTRO DE SEVERIDAD ==========
    if 'severidad' in df.columns and filtro_severidad:
        df = df[df['severidad'].isin(filtro_severidad)]
    
    if df is None or len(df) == 0:
        st.warning("⚠️ No hay datos con los filtros seleccionados.")
        return
    
    # ========== ALERTA CRÍTICOS ==========
    criticos = len(df[df['severidad'] == 'CRITICA']) if 'severidad' in df.columns else 0
    if criticos > 0:
        st.markdown(f"""
        <div class="critical-banner">
            ⚠️ ¡ALERTA! {criticos} errores críticos requieren atención
        </div>
        """, unsafe_allow_html=True)
    
    # ========== KPIs ==========
    render_kpis(df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== INFO DEL PERÍODO ==========
    if 'fecha' in df.columns and not df['fecha'].isna().all():
        fecha_min = df['fecha'].min()
        fecha_max = df['fecha'].max()
        periodo_texto = f"{MESES_ES[mes_sel]} {año_sel}" if not ver_historico else "Histórico completo"
        st.markdown(f"""
        <div class="info-box">
            📅 <strong>Período:</strong> {periodo_texto} | 
            <strong>Desde:</strong> {fecha_min.strftime('%d/%m/%Y')} <strong>hasta:</strong> {fecha_max.strftime('%d/%m/%Y')} | 
            📊 <strong>Total:</strong> {len(df):,} registros
        </div>
        """, unsafe_allow_html=True)
    
    # ========== GRÁFICOS FILA 1 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        fig = grafico_tendencia_diaria(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = grafico_severidad(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    
    # ========== GRÁFICOS FILA 2 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        fig = grafico_por_tipo(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = grafico_mensajes_error(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    
    # ========== POR HORA ==========
    fig = grafico_por_hora(df)
    if fig: st.plotly_chart(fig, use_container_width=True)
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📋 Detalle Mensajes", "🔍 Explorar Datos", "📊 Resumen"])
    
    with tab1:
        if 'error_message' in df.columns:
            msgs = df['error_message'].dropna()
            msgs = msgs[msgs != '']
            if len(msgs) > 0:
                top = msgs.value_counts().head(20).reset_index()
                top.columns = ['Mensaje de Error', 'Repeticiones']
                st.dataframe(top, use_container_width=True, hide_index=True)
            else:
                st.info("No hay mensajes de error registrados")
        else:
            st.info("La columna 'error_message' no existe en los datos")
    
    with tab2:
        if 'tipo_error' in df.columns:
            tipo_sel = st.selectbox("Filtrar por tipo:", ["Todos"] + list(df['tipo_error'].dropna().unique()))
            df_show = df if tipo_sel == "Todos" else df[df['tipo_error'] == tipo_sel]
            st.dataframe(df_show, use_container_width=True, height=400)
        else:
            st.dataframe(df, use_container_width=True, height=400)
    
    with tab3:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Errores", f"{len(df):,}")
        with col2:
            if 'tipo_error' in df.columns:
                st.metric("Tipos Únicos", df['tipo_error'].nunique())
        with col3:
            if 'fecha' in df.columns and not df['fecha'].isna().all():
                dias = df['fecha'].dt.day.nunique()
                st.metric("Días con Errores", dias)
        with col4:
            if 'fecha' in df.columns and not df['fecha'].isna().all():
                dias = max(df['fecha'].dt.day.nunique(), 1)
                st.metric("Promedio/día", f"{len(df)//dias:,}")
    
    # ========== DESCARGAR ==========
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV del período",
            csv,
            f"errores_proa_{MESES_ES[mes_sel]}_{año_sel}.csv",
            "text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
