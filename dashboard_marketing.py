"""
Dashboard Corporativo de Marketing - BAP 2025
Sistema de Business Intelligence para análise de KPIs e campanhas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="BAP | Marketing Analytics",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Corporativo Profissional
st.markdown("""
<style>
    /* Importar fonte profissional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Header principal */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }

    .main-subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Sidebar corporativa */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #374151;
    }

    /* Métricas com estilo profissional */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 600;
        color: #111827;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Cards de métrica */
    .metric-card {
        background: linear-gradient(to bottom, #ffffff, #f9fafb);
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Títulos de seção */
    h2, h3 {
        color: #111827;
        font-weight: 600;
        letter-spacing: -0.3px;
    }

    /* Tabs corporativas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f3f4f6;
        padding: 4px;
        border-radius: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border-radius: 4px;
        color: #6b7280;
        font-weight: 500;
        font-size: 0.875rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #111827;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Divisores */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e5e7eb;
    }

    /* Botões */
    .stButton button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }

    /* DataFrames */
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid #e5e7eb;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 6px;
        border-left-width: 4px;
    }

    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Logo placeholder */
    .company-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2563eb;
        letter-spacing: -1px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    """Carrega todos os dados do Excel preparado"""
    file_path = Path('KPI_Marketing_Preparado.xlsx')

    if not file_path.exists():
        st.error("Erro: Arquivo 'KPI_Marketing_Preparado.xlsx' não encontrado!")
        st.info("Execute primeiro o script: python preparar_dados_marketing.py")
        st.stop()

    data = {
        'marketing_geral': pd.read_excel(file_path, sheet_name='Marketing_Geral'),
        'leads': pd.read_excel(file_path, sheet_name='Leads_Condominios'),
        'indices': pd.read_excel(file_path, sheet_name='Indices_Condominios'),
        'imoveis': pd.read_excel(file_path, sheet_name='Campanha_Imoveis'),
        'boleto': pd.read_excel(file_path, sheet_name='Campanha_Boleto_Digital'),
        'seguros': pd.read_excel(file_path, sheet_name='Campanha_Multiseguros'),
        'resumo': pd.read_excel(file_path, sheet_name='Resumo_Analitico'),
        'consolidado': pd.read_excel(file_path, sheet_name='Dados_Consolidados_Long')
    }

    return data

def get_month_columns(df):
    """Identifica as colunas de meses"""
    month_keywords = ['janeiro', 'fevereiro', 'março', 'marco', 'abril', 'maio', 'junho',
                     'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    return [col for col in df.columns if any(month.lower() in str(col).lower() for month in month_keywords)]

def get_metric_data(df, metric_name):
    """Extrai dados de uma métrica específica"""
    metric_col = df.columns[0]
    mask = df[metric_col].str.contains(metric_name, case=False, na=False)
    if mask.any():
        row = df[mask].iloc[0]
        month_cols = get_month_columns(df)
        return row[month_cols].values, month_cols
    return None, None

# Cores corporativas
CORPORATE_COLORS = {
    'primary': '#2563eb',
    'secondary': '#64748b',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'dark': '#1e293b',
    'light': '#f1f5f9'
}

# Carregar dados
data = load_data()

# ============================================================================
# SIDEBAR CORPORATIVA
# ============================================================================
with st.sidebar:
    st.markdown('<div class="company-logo">BAP</div>', unsafe_allow_html=True)

    st.markdown("### ANALYTICS DASHBOARD")
    st.markdown("Business Intelligence & Marketing Performance")

    st.markdown("---")

    # Seletor de módulo
    st.markdown("**MÓDULOS**")
    modulo = st.selectbox(
        "Selecione o módulo de análise:",
        ["Executive Summary", "Marketing Performance", "Lead Analytics",
         "Financial KPIs", "Campaign Management", "Comparative Analysis"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Informações do período
    st.markdown("**PERÍODO**")
    st.caption("Janeiro - Outubro 2025")

    st.markdown("---")

    # Métricas resumidas
    st.markdown("**OVERVIEW**")
    resumo = data['resumo']
    total_metricas = resumo['Num_Métricas'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Métricas", total_metricas, label_visibility="visible")
    with col2:
        st.metric("Tabelas", len(resumo), label_visibility="visible")

    avg_preenchimento = resumo['Pct_Preenchimento'].mean()
    st.metric("Completude", f"{avg_preenchimento:.1f}%", label_visibility="visible")

# ============================================================================
# HEADER PRINCIPAL
# ============================================================================
st.markdown('<h1 class="main-header">Marketing Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Análise de Performance e Indicadores Estratégicos | BAP 2025</p>', unsafe_allow_html=True)

# ============================================================================
# EXECUTIVE SUMMARY
# ============================================================================
if modulo == "Executive Summary":
    st.markdown("## Executive Summary")
    st.markdown("Visão consolidada dos principais indicadores de performance")

    st.markdown("---")

    # KPIs Principais
    df_indices = data['indices']
    df_marketing = data['marketing_geral']
    month_cols = get_month_columns(df_indices)

    # Row de métricas principais
    col1, col2, col3, col4 = st.columns(4)

    # CAC médio
    cac_data, _ = get_metric_data(df_indices, 'CAC')
    if cac_data is not None:
        cac_medio = np.nanmean(cac_data)
        with col1:
            st.metric("Customer Acquisition Cost", f"R$ {cac_medio:,.0f}",
                     delta=None, help="Custo médio de aquisição de cliente")

    # MRR médio
    mrr_data, _ = get_metric_data(df_indices, 'MRR')
    if mrr_data is not None:
        mrr_medio = np.nanmean(mrr_data)
        mrr_total = np.nansum(mrr_data)
        with col2:
            st.metric("Monthly Recurring Revenue", f"R$ {mrr_medio:,.0f}",
                     help="Receita recorrente mensal média")

    # Novos seguidores
    seg_data, _ = get_metric_data(df_marketing, 'Seguidores')
    if seg_data is not None:
        total_seg = np.nansum(seg_data)
        with col3:
            st.metric("New Followers", f"{total_seg:,.0f}",
                     help="Total de novos seguidores no período")

    # Investimento total
    ads_data, _ = get_metric_data(df_marketing, 'Custo geral de Ads')
    if ads_data is not None:
        total_ads = np.nansum(ads_data)
        with col4:
            st.metric("Ad Investment", f"R$ {total_ads:,.0f}",
                     help="Investimento total em publicidade")

    st.markdown("---")

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Data Completeness")
        fig = px.bar(
            resumo,
            x='Pct_Preenchimento',
            y='Tabela',
            orientation='h',
            text='Pct_Preenchimento',
            color='Pct_Preenchimento',
            color_continuous_scale=['#fee2e2', '#dcfce7'],
            range_color=[0, 100]
        )
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            marker_line_color='#e5e7eb',
            marker_line_width=1
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Completeness (%)",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Metrics Summary")
        resumo_display = resumo[['Tabela', 'Num_Métricas', 'Pct_Preenchimento']].copy()
        resumo_display.columns = ['Module', 'Metrics', 'Completeness (%)']
        resumo_display['Completeness (%)'] = resumo_display['Completeness (%)'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(
            resumo_display,
            hide_index=True,
            height=400,
            use_container_width=True
        )

# ============================================================================
# MARKETING PERFORMANCE
# ============================================================================
elif modulo == "Marketing Performance":
    st.markdown("## Marketing Performance")
    st.markdown("Análise de performance de canais digitais e investimento em mídia")

    df_marketing = data['marketing_geral']
    month_cols = get_month_columns(df_marketing)

    st.markdown("---")

    # Instagram Growth
    st.markdown("### Instagram Growth Analysis")
    seg_data, months = get_metric_data(df_marketing, 'Seguidores')

    if seg_data is not None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=seg_data,
            mode='lines+markers',
            name='New Followers',
            line=dict(color=CORPORATE_COLORS['primary'], width=3),
            marker=dict(size=8, line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.1)'
        ))

        # Adicionar linha de média
        media = np.nanmean(seg_data)
        fig.add_hline(
            y=media,
            line_dash="dash",
            line_color=CORPORATE_COLORS['secondary'],
            annotation_text=f"Average: {media:.0f}",
            annotation_position="right"
        )

        fig.update_layout(
            height=350,
            xaxis_title="Period",
            yaxis_title="New Followers",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average", f"{np.nanmean(seg_data):.0f}")
        col2.metric("Maximum", f"{np.nanmax(seg_data):.0f}")
        col3.metric("Minimum", f"{np.nanmin(seg_data):.0f}")
        col4.metric("Total", f"{np.nansum(seg_data):.0f}")

    st.markdown("---")

    # Investimento e Performance
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Advertising Investment")
        ads_data, months = get_metric_data(df_marketing, 'Custo geral de Ads')
        if ads_data is not None:
            fig = px.bar(
                x=months, y=ads_data,
                labels={'x': 'Period', 'y': 'Investment (R$)'},
                color=ads_data,
                color_continuous_scale=['#dbeafe', '#1e40af']
            )
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11, color='#374151'),
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb')
            )
            st.plotly_chart(fig, use_container_width=True)

            col_a, col_b = st.columns(2)
            col_a.metric("Total", f"R$ {np.nansum(ads_data):,.2f}")
            col_b.metric("Average", f"R$ {np.nanmean(ads_data):,.2f}")

    with col2:
        st.markdown("### Content Views")
        vis_data, months = get_metric_data(df_marketing, 'Visualizações')
        if vis_data is not None:
            fig = px.area(
                x=months, y=vis_data,
                labels={'x': 'Period', 'y': 'Views'},
                color_discrete_sequence=[CORPORATE_COLORS['success']]
            )
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11, color='#374151'),
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb')
            )
            st.plotly_chart(fig, use_container_width=True)

            col_a, col_b = st.columns(2)
            col_a.metric("Total", f"{np.nansum(vis_data):,.0f}")
            col_b.metric("Average", f"{np.nanmean(vis_data):,.0f}")

    st.markdown("---")

    # Reach Analysis
    st.markdown("### Reach Analysis: Organic vs Paid")
    org_data, months = get_metric_data(df_marketing, 'Alcance Orgânico')
    pago_data, _ = get_metric_data(df_marketing, 'Alcance Pago')

    if org_data is not None and pago_data is not None:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months, y=org_data,
            name='Organic',
            marker_color=CORPORATE_COLORS['success']
        ))
        fig.add_trace(go.Bar(
            x=months, y=pago_data,
            name='Paid',
            marker_color=CORPORATE_COLORS['warning']
        ))
        fig.update_layout(
            height=350,
            barmode='group',
            xaxis_title="Period",
            yaxis_title="Reach",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# LEAD ANALYTICS
# ============================================================================
elif modulo == "Lead Analytics":
    st.markdown("## Lead Analytics")
    st.markdown("Análise de geração e conversão de leads por canal")

    df_leads = data['leads']
    metric_col = df_leads.columns[0]
    month_cols = get_month_columns(df_leads)

    st.markdown("---")

    # Propostas por origem
    st.markdown("### Lead Source Distribution")
    propostas_mask = df_leads[metric_col].str.contains('proposta enviada', case=False, na=False)
    df_propostas = df_leads[propostas_mask].copy()
    df_propostas['Total'] = df_propostas[month_cols].sum(axis=1)
    df_propostas['Origem'] = df_propostas[metric_col].str.replace('Origem da proposta enviada', '').str.strip(' -')
    df_propostas_filtrado = df_propostas[df_propostas['Total'] > 0].copy()

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = px.pie(
            df_propostas_filtrado,
            values='Total',
            names='Origem',
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent',
            marker=dict(line=dict(color='white', width=2))
        )
        fig.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11, color='#374151')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_propostas_filtrado.sort_values('Total', ascending=True),
            x='Total',
            y='Origem',
            orientation='h',
            text='Total',
            color='Total',
            color_continuous_scale=['#dbeafe', '#1e3a8a']
        )
        fig.update_traces(textposition='outside', marker_line_color='#e5e7eb', marker_line_width=1)
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Total Proposals",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Conversion Rate
    st.markdown("### Conversion Rate by Source")

    convertidos_mask = df_leads[metric_col].str.contains('Lead Convertido', case=False, na=False)
    df_convertidos = df_leads[convertidos_mask].copy()
    df_convertidos['Total'] = df_convertidos[month_cols].sum(axis=1)

    origens_map = {
        'Indicação': 'Indica',
        'Capt. Ativa': 'Capt. Ativa',
        'Capt. Receptiva': 'Contato Receptivo',
        'Construtora': 'Construtora',
        'Reativação': 'Reativa',
        'Ads': 'Ads',
        'Mala Direta': 'Mala Direta'
    }

    conversao_data = []
    for origem_conv, origem_prop in origens_map.items():
        prop_row = df_propostas[df_propostas[metric_col].str.contains(origem_prop, case=False, na=False)]
        conv_row = df_convertidos[df_convertidos[metric_col].str.contains(origem_conv, case=False, na=False)]

        if len(prop_row) > 0 and len(conv_row) > 0:
            total_prop = prop_row['Total'].values[0]
            total_conv = conv_row['Total'].values[0]
            taxa = (total_conv / total_prop * 100) if total_prop > 0 else 0
            conversao_data.append({
                'Source': origem_conv,
                'Proposals': int(total_prop),
                'Conversions': int(total_conv),
                'Rate_%': round(taxa, 2)
            })

    df_conversao = pd.DataFrame(conversao_data).sort_values('Rate_%', ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            df_conversao,
            x='Source',
            y='Rate_%',
            text='Rate_%',
            color='Rate_%',
            color_continuous_scale=['#fecaca', '#166534'],
            range_color=[0, df_conversao['Rate_%'].max()]
        )
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            marker_line_color='#e5e7eb',
            marker_line_width=1
        )
        fig.update_layout(
            height=350,
            xaxis_title="Lead Source",
            yaxis_title="Conversion Rate (%)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Formatar a coluna de taxa
        df_conversao_display = df_conversao.copy()
        df_conversao_display['Rate_%'] = df_conversao_display['Rate_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(
            df_conversao_display,
            hide_index=True,
            height=350,
            use_container_width=True
        )

# ============================================================================
# FINANCIAL KPIs
# ============================================================================
elif modulo == "Financial KPIs":
    st.markdown("## Financial Key Performance Indicators")
    st.markdown("Análise de indicadores financeiros e rentabilidade")

    df_indices = data['indices']
    metric_col = df_indices.columns[0]
    month_cols = get_month_columns(df_indices)

    st.markdown("---")

    # Customer Acquisition Cost
    st.markdown("### Customer Acquisition Cost (CAC)")
    cac_data, months = get_metric_data(df_indices, 'CAC')

    if cac_data is not None:
        fig = go.Figure()
        media_cac = np.nanmean(cac_data)

        fig.add_trace(go.Scatter(
            x=months, y=cac_data,
            mode='lines+markers',
            name='CAC',
            line=dict(color=CORPORATE_COLORS['primary'], width=3),
            marker=dict(size=9, line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.08)'
        ))

        fig.add_hline(
            y=media_cac,
            line_dash="dash",
            line_color=CORPORATE_COLORS['danger'],
            annotation_text=f"Average: R$ {media_cac:,.0f}",
            annotation_position="right"
        )

        fig.update_layout(
            height=350,
            xaxis_title="Period",
            yaxis_title="CAC (R$)",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Average CAC", f"R$ {media_cac:,.2f}")
        col2.metric("Minimum", f"R$ {np.nanmin(cac_data):,.2f}")
        col3.metric("Maximum", f"R$ {np.nanmax(cac_data):,.2f}")

    st.markdown("---")

    # MRR e ROI
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Monthly Recurring Revenue")
        mrr_data, months = get_metric_data(df_indices, 'MRR')
        if mrr_data is not None:
            fig = px.bar(
                x=months, y=mrr_data,
                labels={'x': 'Period', 'y': 'MRR (R$)'},
                text=mrr_data,
                color=mrr_data,
                color_continuous_scale=['#d1fae5', '#065f46']
            )
            fig.update_traces(
                texttemplate='R$%{text:,.0f}',
                textposition='outside',
                marker_line_color='#e5e7eb',
                marker_line_width=1
            )
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11, color='#374151'),
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb')
            )
            st.plotly_chart(fig, use_container_width=True)

            col_a, col_b = st.columns(2)
            col_a.metric("Average", f"R$ {np.nanmean(mrr_data):,.2f}")
            col_b.metric("Total", f"R$ {np.nansum(mrr_data):,.2f}")

    with col2:
        st.markdown("### Return on Investment Ratio")
        roi_data, months = get_metric_data(df_indices, 'Recorrente mensal / Custo')
        if roi_data is not None:
            colors = [CORPORATE_COLORS['success'] if v > 1 else CORPORATE_COLORS['danger']
                     for v in roi_data if not np.isnan(v)]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=months, y=roi_data,
                marker_color=colors,
                text=roi_data,
                texttemplate='%{text:.2f}x',
                marker_line_color='#e5e7eb',
                marker_line_width=1
            ))
            fig.add_hline(
                y=1,
                line_dash="dash",
                line_color=CORPORATE_COLORS['dark'],
                annotation_text="Break-even",
                annotation_position="right"
            )
            fig.update_layout(
                height=300,
                yaxis_title="ROI Ratio",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11, color='#374151'),
                xaxis=dict(gridcolor='#e5e7eb'),
                yaxis=dict(gridcolor='#e5e7eb')
            )
            st.plotly_chart(fig, use_container_width=True)

            col_a, col_b = st.columns(2)
            col_a.metric("Average", f"{np.nanmean(roi_data):.2f}x")
            meses_positivos = np.sum(roi_data > 1)
            total_meses = len([x for x in roi_data if not np.isnan(x)])
            col_b.metric("Positive Months", f"{meses_positivos}/{total_meses}")

# ============================================================================
# CAMPAIGN MANAGEMENT
# ============================================================================
elif modulo == "Campaign Management":
    st.markdown("## Campaign Management")
    st.markdown("Análise detalhada de performance de campanhas")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Real Estate", "Digital Billing", "Insurance"])

    # TAB 1: Imóveis
    with tab1:
        st.markdown("### Real Estate Campaign")
        df_imoveis = data['imoveis']
        month_cols = get_month_columns(df_imoveis)

        col1, col2, col3 = st.columns(3)

        inv_data, _ = get_metric_data(df_imoveis, 'Investimento')
        leads_data, _ = get_metric_data(df_imoveis, 'Leads Gerados')
        roi_data, months = get_metric_data(df_imoveis, 'ROI')

        if inv_data is not None:
            col1.metric("Total Investment", f"R$ {np.nansum(inv_data):,.2f}")
        if leads_data is not None:
            col2.metric("Leads Generated", f"{np.nansum(leads_data):.0f}")
        if roi_data is not None:
            col3.metric("Average ROI", f"{np.nanmean(roi_data):.2f}%")

        col1, col2 = st.columns(2)

        with col1:
            if inv_data is not None:
                fig = px.line(
                    x=months, y=inv_data,
                    markers=True,
                    labels={'x': 'Period', 'y': 'Investment (R$)'}
                )
                fig.update_traces(
                    line_color=CORPORATE_COLORS['primary'],
                    line_width=3,
                    marker=dict(size=8, line=dict(width=2, color='white'))
                )
                fig.update_layout(
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if roi_data is not None:
                fig = px.bar(
                    x=months, y=roi_data,
                    labels={'x': 'Period', 'y': 'ROI (%)'},
                    color=roi_data,
                    color_continuous_scale=['#fee2e2', '#166534']
                )
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

    # TAB 2: Boleto Digital
    with tab2:
        st.markdown("### Digital Billing Campaign")
        df_boleto = data['boleto']
        month_cols = get_month_columns(df_boleto)

        unid_data, months = get_metric_data(df_boleto, 'Nº de Unidades')
        econ_data, _ = get_metric_data(df_boleto, 'Economia')
        pct_data, _ = get_metric_data(df_boleto, '% da base')

        col1, col2, col3 = st.columns(3)

        if unid_data is not None:
            col1.metric("Registered Units", f"{np.nanmax(unid_data):.0f}")
        if econ_data is not None:
            col2.metric("Total Savings", f"R$ {np.nansum(econ_data):,.2f}")
        if pct_data is not None:
            col3.metric("Current Base %", f"{np.nanmax(pct_data)*100:.2f}%")

        col1, col2 = st.columns(2)

        with col1:
            if unid_data is not None:
                fig = px.area(
                    x=months, y=unid_data,
                    labels={'x': 'Period', 'y': 'Units'},
                    color_discrete_sequence=[CORPORATE_COLORS['success']]
                )
                fig.update_layout(
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if econ_data is not None:
                fig = px.bar(
                    x=months, y=econ_data,
                    labels={'x': 'Period', 'y': 'Savings (R$)'},
                    color_discrete_sequence=[CORPORATE_COLORS['success']]
                )
                fig.update_layout(
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

    # TAB 3: Multiseguros
    with tab3:
        st.markdown("### Insurance Campaign")
        df_seguros = data['seguros']
        month_cols = get_month_columns(df_seguros)

        inv_seg_data, months = get_metric_data(df_seguros, 'Investimento')
        leads_seg_data, _ = get_metric_data(df_seguros, 'Leads Gerados')
        conv_seg_data, _ = get_metric_data(df_seguros, 'Clientes Convertidos')
        roi_seg_data, _ = get_metric_data(df_seguros, 'ROI')

        col1, col2, col3, col4 = st.columns(4)

        if inv_seg_data is not None:
            col1.metric("Investment", f"R$ {np.nansum(inv_seg_data):,.2f}")
        if leads_seg_data is not None:
            col2.metric("Leads", f"{np.nansum(leads_seg_data):.0f}")
        if conv_seg_data is not None:
            col3.metric("Conversions", f"{np.nansum(conv_seg_data):.0f}")
        if roi_seg_data is not None:
            col4.metric("Average ROI", f"{np.nanmean(roi_seg_data):.2f}%")

        col1, col2 = st.columns(2)

        with col1:
            if leads_seg_data is not None and conv_seg_data is not None:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=months, y=leads_seg_data,
                    name='Leads',
                    marker_color=CORPORATE_COLORS['primary']
                ))
                fig.add_trace(go.Bar(
                    x=months, y=conv_seg_data,
                    name='Conversions',
                    marker_color=CORPORATE_COLORS['success']
                ))
                fig.update_layout(
                    barmode='group',
                    height=300,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if roi_seg_data is not None:
                fig = px.line(
                    x=months, y=roi_seg_data,
                    markers=True,
                    labels={'x': 'Period', 'y': 'ROI (%)'}
                )
                fig.update_traces(
                    line_color=CORPORATE_COLORS['danger'],
                    line_width=3,
                    marker=dict(size=8, line=dict(width=2, color='white'))
                )
                fig.update_layout(
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11, color='#374151'),
                    xaxis=dict(gridcolor='#e5e7eb'),
                    yaxis=dict(gridcolor='#e5e7eb')
                )
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# COMPARATIVE ANALYSIS
# ============================================================================
elif modulo == "Comparative Analysis":
    st.markdown("## Comparative Analysis")
    st.markdown("Análise comparativa entre campanhas e métricas")

    df_imoveis = data['imoveis']
    df_seguros = data['seguros']
    month_cols = get_month_columns(df_imoveis)

    st.markdown("---")

    # Investment Comparison
    st.markdown("### Investment Comparison")

    inv_imoveis, months = get_metric_data(df_imoveis, 'Investimento')
    inv_seguros, _ = get_metric_data(df_seguros, 'Investimento')

    if inv_imoveis is not None and inv_seguros is not None:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months, y=inv_imoveis,
            name='Real Estate',
            marker_color=CORPORATE_COLORS['primary']
        ))
        fig.add_trace(go.Bar(
            x=months, y=inv_seguros,
            name='Insurance',
            marker_color=CORPORATE_COLORS['danger']
        ))
        fig.update_layout(
            height=350,
            barmode='group',
            xaxis_title="Period",
            yaxis_title="Investment (R$)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        col1.metric("Real Estate Total", f"R$ {np.nansum(inv_imoveis):,.2f}")
        col2.metric("Insurance Total", f"R$ {np.nansum(inv_seguros):,.2f}")

    st.markdown("---")

    # ROI Comparison
    st.markdown("### Return on Investment Comparison")

    roi_imoveis, months = get_metric_data(df_imoveis, 'ROI')
    roi_seguros, _ = get_metric_data(df_seguros, 'ROI')

    if roi_imoveis is not None and roi_seguros is not None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=roi_imoveis,
            mode='lines+markers',
            name='Real Estate',
            line=dict(color=CORPORATE_COLORS['primary'], width=3),
            marker=dict(size=8, line=dict(width=2, color='white'))
        ))
        fig.add_trace(go.Scatter(
            x=months, y=roi_seguros,
            mode='lines+markers',
            name='Insurance',
            line=dict(color=CORPORATE_COLORS['danger'], width=3),
            marker=dict(size=8, line=dict(width=2, color='white'))
        ))
        fig.update_layout(
            height=350,
            xaxis_title="Period",
            yaxis_title="ROI (%)",
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#374151'),
            xaxis=dict(gridcolor='#e5e7eb'),
            yaxis=dict(gridcolor='#e5e7eb')
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        col1.metric("Real Estate Average", f"{np.nanmean(roi_imoveis):.2f}%")
        col2.metric("Insurance Average", f"{np.nanmean(roi_seguros):.2f}%")

    st.markdown("---")

    # Comparative Summary
    st.markdown("### Performance Summary")

    leads_imoveis, _ = get_metric_data(df_imoveis, 'Leads Gerados')
    leads_seguros, _ = get_metric_data(df_seguros, 'Leads Gerados')
    conv_imoveis, _ = get_metric_data(df_imoveis, 'Clientes Convertidos')
    conv_seguros, _ = get_metric_data(df_seguros, 'Clientes Convertidos')

    comparacao = pd.DataFrame({
        'Metric': ['Total Investment', 'Leads Generated', 'Conversions', 'Average ROI', 'Cost per Lead'],
        'Real Estate': [
            f"R$ {np.nansum(inv_imoveis):,.2f}" if inv_imoveis is not None else 'N/A',
            f"{np.nansum(leads_imoveis):.0f}" if leads_imoveis is not None else 'N/A',
            f"{np.nansum(conv_imoveis):.0f}" if conv_imoveis is not None else 'N/A',
            f"{np.nanmean(roi_imoveis):.2f}%" if roi_imoveis is not None else 'N/A',
            f"R$ {np.nansum(inv_imoveis)/np.nansum(leads_imoveis):,.2f}" if inv_imoveis is not None and leads_imoveis is not None else 'N/A'
        ],
        'Insurance': [
            f"R$ {np.nansum(inv_seguros):,.2f}" if inv_seguros is not None else 'N/A',
            f"{np.nansum(leads_seguros):.0f}" if leads_seguros is not None else 'N/A',
            f"{np.nansum(conv_seguros):.0f}" if conv_seguros is not None else 'N/A',
            f"{np.nanmean(roi_seguros):.2f}%" if roi_seguros is not None else 'N/A',
            f"R$ {np.nansum(inv_seguros)/np.nansum(leads_seguros):,.2f}" if inv_seguros is not None and leads_seguros is not None else 'N/A'
        ]
    })

    st.dataframe(comparacao, hide_index=True, use_container_width=True, height=250)

# Footer corporativo
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9ca3af; font-size: 0.875rem; padding: 2rem 0 1rem 0;'>
    <p style='margin: 0; font-weight: 500;'>BAP Marketing Analytics Platform</p>
    <p style='margin: 0.5rem 0 0 0; font-weight: 300;'>Last updated: October 2025 | Business Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)
