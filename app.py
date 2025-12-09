# -*- coding: utf-8 -*-
"""
🏥 DASHBOARD DE ERRORES API - PROA/CHOPO
=========================================
Versión 8.0 - Conectado a Google Sheets

Autor: Lizbeth Ramírez | PROA - Ecommerce
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
    
    .success-box {{
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid {COLORS['green']};
        border-radius: 8px;
        padding: 1rem;
        color: {COLORS['green']};
        margin-bottom: 1rem;
    }}
    
    .warning-box {{
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid {COLORS['yellow']};
        border-radius: 8px;
        padding: 1rem;
        color: {COLORS['yellow']};
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
@st.cache_data(ttl=300)  # Cache por 5 minutos
def cargar_google_sheet():
    """Carga datos desde Google Sheets"""
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        
        # Procesar columna fecha
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        # Limpiar filas vacías
        df = df.dropna(how='all')
        
        return df, None
    except Exception as e:
        return None, str(e)

def cargar_excel(archivo):
    """Carga un archivo Excel"""
    try:
        xl = pd.ExcelFile(archivo)
        hojas = xl.sheet_names
        
        for hoja in ['Todos los Errores', 'Sheet1', 'Hoja1'] + hojas:
            if hoja in hojas:
                df = pd.read_excel(archivo, sheet_name=hoja)
                if len(df) > 0:
                    break
        else:
            df = pd.read_excel(archivo, sheet_name=0)
        
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

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
def grafico_tendencia(df):
    if 'fecha' not in df.columns or df['fecha'].isna().all():
        return None
    
    df_temp = df.dropna(subset=['fecha']).copy()
    df_temp['dia'] = df_temp['fecha'].dt.date
    por_dia = df_temp.groupby('dia').size().reset_index(name='Errores')
    por_dia['dia'] = pd.to_datetime(por_dia['dia'])
    
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
        title='📅 Tendencia Diaria',
        xaxis=dict(title='', gridcolor=COLORS['border']),
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
    
    conteo = df['tipo_error'].value_counts().reset_index()
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
        title='📊 Errores por Tipo',
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
        title='🎯 Por Severidad',
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['white'])
    )
    return fig

def grafico_mensual(df):
    if 'fecha' not in df.columns or df['fecha'].isna().all():
        return None
    
    df_temp = df.dropna(subset=['fecha']).copy()
    df_temp['mes'] = df_temp['fecha'].dt.to_period('M').astype(str)
    por_mes = df_temp.groupby('mes').size().reset_index(name='Errores')
    
    fig = go.Figure(go.Bar(
        x=por_mes['mes'],
        y=por_mes['Errores'],
        marker=dict(color=COLORS['blue_light']),
        text=por_mes['Errores'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='📆 Errores por Mes',
        xaxis=dict(title='', gridcolor=COLORS['border']),
        yaxis=dict(title='', gridcolor=COLORS['border']),
        height=300,
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
        title='🕐 Errores por Hora',
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
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>✦ PROA</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.8rem;">Grupo Diagnóstico</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📁 Fuente de Datos")
        
        fuente = st.radio(
            "Cargar desde:",
            ["☁️ Google Sheets (histórico)", "📤 Subir Excel"],
            index=0
        )
        
        # Subir Excel adicional
        archivo_excel = None
        if fuente == "📤 Subir Excel":
            archivo_excel = st.file_uploader(
                "Sube Excel",
                type=['xlsx', 'xls'],
                help="Para agregar datos nuevos"
            )
        
        st.markdown("---")
        
        # Filtros
        st.markdown("### ⚙️ Filtros")
        
        filtro_severidad = st.multiselect(
            "Severidad:",
            ['CRITICA', 'ALTA', 'MEDIA', 'BAJA'],
            default=['CRITICA', 'ALTA', 'MEDIA', 'BAJA']
        )
        
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
    
    # ========== CARGAR DATOS ==========
    df = None
    error_carga = None
    
    if fuente == "☁️ Google Sheets (histórico)":
        df, error_carga = cargar_google_sheet()
    elif archivo_excel:
        df = cargar_excel(archivo_excel)
    
    # ========== HEADER ==========
    errores_mes = 0
    if df is not None and 'fecha' in df.columns and not df['fecha'].isna().all():
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        errores_mes = len(df[(df['fecha'].dt.month == mes_actual) & (df['fecha'].dt.year == año_actual)])
    
    render_header(errores_mes)
    
    # ========== MOSTRAR ESTADO ==========
    if fuente == "☁️ Google Sheets (histórico)":
        if error_carga:
            st.markdown(f"""
            <div class="warning-box">
                ⚠️ <strong>No se pudo conectar a Google Sheets:</strong> {error_carga}<br>
                Verifica que el Sheet sea público.
            </div>
            """, unsafe_allow_html=True)
        elif df is not None and len(df) > 0:
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>Conectado a Google Sheets</strong> | {len(df):,} registros cargados
            </div>
            """, unsafe_allow_html=True)
    
    # ========== SIN DATOS ==========
    if df is None or len(df) == 0:
        st.markdown(f"""
        <div class="info-box">
            <h3>📤 No hay datos disponibles</h3>
            <p><strong>Opción 1:</strong> Verifica que Google Sheets tenga datos y sea público</p>
            <p><strong>Opción 2:</strong> Sube un archivo Excel</p>
            <br>
            <p>📋 <strong>Link del Sheet:</strong></p>
            <a href="https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}" target="_blank" style="color: {COLORS['cyan']};">Abrir Google Sheet</a>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ========== APLICAR FILTROS ==========
    if 'severidad' in df.columns and filtro_severidad:
        df = df[df['severidad'].isin(filtro_severidad)]
    
    if usar_rango and 'fecha' in df.columns and fecha_inicio and fecha_fin:
        df = df[(df['fecha'].dt.date >= fecha_inicio) & (df['fecha'].dt.date <= fecha_fin)]
    
    # ========== SIN DATOS DESPUÉS DE FILTRAR ==========
    if df is None or len(df) == 0:
        st.warning("⚠️ No hay datos en el rango seleccionado. Ajusta los filtros.")
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
    
    # ========== RANGO DE FECHAS INFO ==========
    if 'fecha' in df.columns and not df['fecha'].isna().all():
        fecha_min = df['fecha'].min()
        fecha_max = df['fecha'].max()
        st.markdown(f"""
        <div class="info-box">
            📅 <strong>Datos desde:</strong> {fecha_min.strftime('%d/%m/%Y')} <strong>hasta:</strong> {fecha_max.strftime('%d/%m/%Y')} | 
            📊 <strong>Total:</strong> {len(df):,} registros
        </div>
        """, unsafe_allow_html=True)
    
    # ========== GRÁFICOS FILA 1 ==========
    col1, col2 = st.columns(2)
    
    with col1:
        fig = grafico_tendencia(df)
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
        fig = grafico_mensual(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    
    # ========== POR HORA ==========
    fig = grafico_por_hora(df)
    if fig: st.plotly_chart(fig, use_container_width=True)
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📋 Top Mensajes", "🔍 Explorar", "📊 Resumen"])
    
    with tab1:
        if 'error_message' in df.columns:
            msgs = df['error_message'].dropna()
            msgs = msgs[msgs != '']
            if len(msgs) > 0:
                top = msgs.value_counts().head(10).reset_index()
                top.columns = ['Mensaje', 'Repeticiones']
                st.dataframe(top, use_container_width=True, hide_index=True)
            else:
                st.info("No hay mensajes de error registrados")
        else:
            st.info("La columna 'error_message' no existe en los datos")
    
    with tab2:
        if 'tipo_error' in df.columns:
            tipo_sel = st.selectbox("Filtrar:", ["Todos"] + list(df['tipo_error'].dropna().unique()))
            df_show = df if tipo_sel == "Todos" else df[df['tipo_error'] == tipo_sel]
            st.dataframe(df_show, use_container_width=True, height=400)
        else:
            st.dataframe(df, use_container_width=True, height=400)
    
    with tab3:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", f"{len(df):,}")
        with col2:
            if 'tipo_error' in df.columns:
                st.metric("Tipos", df['tipo_error'].nunique())
        with col3:
            if 'fecha' in df.columns and not df['fecha'].isna().all():
                dias = (df['fecha'].max() - df['fecha'].min()).days + 1
                st.metric("Días", dias)
        with col4:
            if 'fecha' in df.columns and not df['fecha'].isna().all():
                dias = max((df['fecha'].max() - df['fecha'].min()).days + 1, 1)
                st.metric("Promedio/día", f"{len(df)//dias}")
    
    # ========== DESCARGAR ==========
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV",
            csv,
            f"errores_proa_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
