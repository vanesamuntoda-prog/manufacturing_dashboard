import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="PT Smart Manufacturing Indonesia",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS MODERN — REDESIGNED
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] * { color: #c4c9e2 !important; }
section[data-testid="stSidebar"] h2 {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stDateInput label,
section[data-testid="stSidebar"] .stSlider label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #8b92b8 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ---- PAGE HEADER ---- */
.page-header {
    padding: 28px 0 24px 0;
    margin-bottom: 28px;
}
.page-header h1 {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.page-header p {
    font-size: 13px;
    color: #8b92b8;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.badge-live {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(99,102,241,0.2);
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.35);
    letter-spacing: 0.3px;
}
.badge-live::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #818cf8;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.8); }
}

/* ---- KPI CARDS ---- */
.kpi-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 22px 22px 18px 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 12px;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 20px 20px 0 0;
}
.kpi-icon {
    width: 44px; height: 44px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    margin-bottom: 14px;
}
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #8b92b8;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.kpi-sub {
    font-size: 11px;
    color: #6b7280;
}
.kpi-glow {
    position: absolute;
    width: 100px; height: 100px;
    border-radius: 50%;
    top: -20px; right: -20px;
    opacity: 0.12;
    filter: blur(20px);
}

/* ---- CHART CARDS ---- */
.chart-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 22px 24px 16px 24px;
    margin-bottom: 16px;
}
.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 4px;
}
.chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 2px;
}
.chart-subtitle {
    font-size: 11px;
    color: #6b7280;
    margin-bottom: 16px;
}
.chart-badge {
    font-size: 10px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}

/* ---- CONNECTION STATUS ---- */
.conn-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; border-radius: 20px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.3px;
    margin-bottom: 16px;
}
.conn-ok   { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.conn-fail { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* ---- DIVIDER ---- */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 8px 0 24px 0;
}

/* ---- Streamlit overrides ---- */
.stPlotlyChart { border-radius: 12px; overflow: hidden; }
div[data-testid="column"] { gap: 0; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# KONEKSI DATABASE
# ============================================================
DB_USER     = "root"
DB_PASSWORD = ""
DB_HOST     = "localhost"
DB_NAME     = "manufacturing_db"

koneksi_berhasil = False

try:
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
        connect_args={"connect_timeout": 5}
    )

    @st.cache_data(ttl=5)
    def ambil_data_master():
        query = """
        SELECT
            fp.tanggal             AS Tanggal,
            dp.product_name        AS Nama_Produk,
            dp.category            AS Kategori,
            df.city                AS Wilayah,
            dm.machine_type        AS Jenis_Mesin,
            fp.planned_qty         AS Target_Produksi,
            fp.actual_qty          AS Aktual_Produksi,
            fp.defect_qty          AS Jumlah_Defect,
            fp.downtime_minutes    AS Downtime
        FROM fact_production fp
        JOIN dim_product dp ON fp.product_key = dp.product_key
        JOIN dim_machine dm ON fp.machine_key  = dm.machine_key
        JOIN dim_factory df ON fp.factory_key  = df.factory_key
        ORDER BY fp.tanggal ASC
        """
        df = pd.read_sql(query, engine)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        harga_map = {'Snack': 15000, 'Beverage': 20000, 'Food': 25000}
        df['Total_Revenue'] = df['Aktual_Produksi'] * df['Kategori'].map(harga_map).fillna(15000)
        return df

    df_master = ambil_data_master()
    koneksi_berhasil = True

except Exception:
    koneksi_berhasil = False
    df_master = pd.DataFrame({
        'Tanggal': pd.to_datetime([
            '2026-06-10','2026-06-11','2026-06-12',
            '2026-06-13','2026-06-14','2026-06-15',
        ]),
        'Nama_Produk':      ['Chocolate Drink 1','Instant Coffee 2','Snack Bar 3','Noodle Cup 11','Chocolate Drink 1','Instant Coffee 2'],
        'Kategori':         ['Snack','Beverage','Snack','Food','Snack','Beverage'],
        'Wilayah':          ['Bandung','Makassar','Bandung','Surabaya','Makassar','Surabaya'],
        'Jenis_Mesin':      ['Cooling Machine','Mixer Machine','Filler Machine','Packing Machine','Cooling Machine','Mixer Machine'],
        'Target_Produksi':  [5000, 4000, 6000, 4500, 5200, 4200],
        'Aktual_Produksi':  [4800, 3920, 5850, 4410, 5100, 4150],
        'Jumlah_Defect':    [50,   20,   110,  40,   35,   15],
        'Downtime':         [15,   45,   10,   30,   5,    20],
    })
    harga_map = {'Snack': 15000, 'Beverage': 20000, 'Food': 25000}
    df_master['Total_Revenue'] = df_master['Aktual_Produksi'] * df_master['Kategori'].map(harga_map)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("<h2>🎛️ Filter & Kontrol</h2>", unsafe_allow_html=True)

    if koneksi_berhasil:
        st.markdown('<div class="conn-badge conn-ok">✅ DATABASE TERHUBUNG </div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="conn-badge conn-fail">⚠️ Demo Mode (DB Offline)</div>', unsafe_allow_html=True)

    list_wilayah  = ['Semua Wilayah']  + sorted(df_master['Wilayah'].unique().tolist())
    list_kategori = ['Semua Kategori'] + sorted(df_master['Kategori'].unique().tolist())
    list_mesin    = ['Semua Mesin']    + sorted(df_master['Jenis_Mesin'].unique().tolist())

    wilayah_terpilih  = st.selectbox("📍 Wilayah",      list_wilayah)
    kategori_terpilih = st.selectbox("🏷️ Kategori",     list_kategori)
    mesin_terpilih    = st.selectbox("⚙️ Jenis Mesin",  list_mesin)

    st.markdown("---")
    tanggal_min = df_master['Tanggal'].min().date()
    tanggal_max = df_master['Tanggal'].max().date()
    rentang = st.date_input(
        "📅 Rentang Tanggal",
        value=(tanggal_min, tanggal_max),
        min_value=tanggal_min,
        max_value=tanggal_max
    )

    st.markdown("---")
    top_n = st.slider("🏆 Top N Produk", min_value=3, max_value=10, value=5)

    st.markdown(
        "<div style='font-size:11px;color:#6b7280;margin-top:12px;line-height:1.8'>"
        "⏱️ Cache diperbarui tiap 5 detik<br>"
        f"🗄️ Source: {DB_NAME} (MySQL)"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FILTER DATA
# ============================================================
df = df_master.copy()
if wilayah_terpilih  != 'Semua Wilayah':  df = df[df['Wilayah']     == wilayah_terpilih]
if kategori_terpilih != 'Semua Kategori': df = df[df['Kategori']    == kategori_terpilih]
if mesin_terpilih    != 'Semua Mesin':    df = df[df['Jenis_Mesin'] == mesin_terpilih]
if isinstance(rentang, (list, tuple)) and len(rentang) == 2:
    df = df[(df['Tanggal'].dt.date >= rentang[0]) & (df['Tanggal'].dt.date <= rentang[1])]


# ============================================================
# BASE PLOTLY LAYOUT — dark glass theme
# ============================================================
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, Segoe UI, sans-serif', color='#8b92b8', size=12),
    margin=dict(l=4, r=4, t=10, b=4),
    showlegend=False,
)
GRID_COLOR  = 'rgba(255,255,255,0.06)'
AXIS_COLOR  = 'rgba(255,255,255,0.12)'


# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="page-header">
    <h1>🏭 Manufacturing Performance Dashboard</h1>
    <p>
        PT Smart Manufacturing Indonesia
        &nbsp;·&nbsp;
        <span class="badge-live">Live OLAP Engine</span>
        &nbsp;·&nbsp; Wilayah: <strong style="color:#a5b4fc">{wilayah_terpilih}</strong>
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI CARDS
# ============================================================
total_target  = int(df['Target_Produksi'].sum())
total_aktual  = int(df['Aktual_Produksi'].sum())
total_defect  = int(df['Jumlah_Defect'].sum())
total_revenue = df['Total_Revenue'].sum()
defect_rate   = (total_defect / total_aktual * 100) if total_aktual > 0 else 0
efisiensi     = (total_aktual / total_target * 100) if total_target > 0 else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,#6366f1,#818cf8);border-radius:20px 20px 0 0;"></div>
        <div class="kpi-glow" style="background:#6366f1;"></div>
        <div class="kpi-icon" style="background:rgba(99,102,241,0.18);">🎯</div>
        <div class="kpi-label">Planned Target</div>
        <div class="kpi-value" style="color:#a5b4fc;">{total_target:,}</div>
        <div class="kpi-sub">Unit alokasi produksi</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,#10b981,#34d399);border-radius:20px 20px 0 0;"></div>
        <div class="kpi-glow" style="background:#10b981;"></div>
        <div class="kpi-icon" style="background:rgba(16,185,129,0.18);">📦</div>
        <div class="kpi-label">Actual Output</div>
        <div class="kpi-value" style="color:#34d399;">{total_aktual:,}</div>
        <div class="kpi-sub">Efisiensi {efisiensi:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,#f43f5e,#fb7185);border-radius:20px 20px 0 0;"></div>
        <div class="kpi-glow" style="background:#f43f5e;"></div>
        <div class="kpi-icon" style="background:rgba(244,63,94,0.18);">⚠️</div>
        <div class="kpi-label">Defect Rate</div>
        <div class="kpi-value" style="color:#fb7185;">{defect_rate:.2f}%</div>
        <div class="kpi-sub">{total_defect:,} pcs rusak</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,#f59e0b,#fbbf24);border-radius:20px 20px 0 0;"></div>
        <div class="kpi-glow" style="background:#f59e0b;"></div>
        <div class="kpi-icon" style="background:rgba(245,158,11,0.18);">💰</div>
        <div class="kpi-label">Sales Revenue</div>
        <div class="kpi-value" style="color:#fbbf24;">Rp {total_revenue/1e6:.1f} Jt</div>
        <div class="kpi-sub">Omset penjualan</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ============================================================
# ROW 1 — TREND & REGIONAL
# ============================================================
col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📈 Sales Trend</div>
        <div class="chart-subtitle">Revenue per tanggal — agregasi harian / mingguan</div>
    """, unsafe_allow_html=True)

    if not df.empty:
        df_trend = df.groupby('Tanggal')['Total_Revenue'].sum().reset_index()
        df_trend['Revenue_M'] = df_trend['Total_Revenue'] / 1e6

        n_points = len(df_trend)
        if n_points > 30:
            df_trend = (
                df_trend.set_index('Tanggal')['Revenue_M']
                .resample('W').sum().reset_index()
            )
            tick_fmt = '%d %b %y'
            x_title  = "Minggu"
        else:
            tick_fmt = '%d %b'
            x_title  = "Tanggal"

        fig_trend = go.Figure()

        # Gradient fill area
        fig_trend.add_trace(go.Scatter(
            x=df_trend['Tanggal'],
            y=df_trend['Revenue_M'],
            mode='lines+markers',
            line=dict(color='#818cf8', width=2.5, shape='spline', smoothing=0.8),
            marker=dict(size=7, color='#1e1b4b', line=dict(color='#818cf8', width=2.5)),
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.12)',
            hovertemplate='<b>%{x|' + tick_fmt + '}</b><br>Revenue: Rp %{y:.1f} Jt<extra></extra>'
        ))

        fig_trend.update_layout(
            **PLOTLY_LAYOUT,
            height=270,
            xaxis=dict(
                showgrid=False, zeroline=False,
                showline=True, linecolor=AXIS_COLOR,
                tickfont=dict(size=11, color='#8b92b8'),
                tickformat=tick_fmt, tickangle=-30, nticks=10,
                title=dict(text=x_title, font=dict(size=11, color='#6b7280'), standoff=8),
            ),
            yaxis=dict(
                showgrid=True, gridcolor=GRID_COLOR,
                zeroline=False,
                tickfont=dict(size=11, color='#8b92b8'),
                tickprefix='Rp ', ticksuffix=' Jt',
            ),
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Tidak ada data trend.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📍 Regional Sales</div>
        <div class="chart-subtitle">Pangsa pasar per wilayah</div>
    """, unsafe_allow_html=True)

    if not df.empty:
        df_reg = df.groupby('Wilayah')['Total_Revenue'].sum().reset_index()
        REGION_COLORS = ['#818cf8','#34d399','#fbbf24','#f472b6','#fb7185','#38bdf8']

        fig_pie = go.Figure(go.Pie(
            labels=df_reg['Wilayah'],
            values=df_reg['Total_Revenue'],
            hole=0.62,
            marker=dict(
                colors=REGION_COLORS[:len(df_reg)],
                line=dict(color='rgba(15,12,41,0.8)', width=3)
            ),
            textinfo='percent+label',
            textfont=dict(size=11, color='#c4c9e2'),
            hovertemplate='<b>%{label}</b><br>Revenue: Rp %{value:,.0f}<br>Share: %{percent}<extra></extra>'
        ))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=270)
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Tidak ada data regional.")
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ============================================================
# ROW 2 — TOP PRODUCT & DOWNTIME
# ============================================================
col3, col4 = st.columns([3, 2], gap="medium")

with col3:
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-title">🏆 Top {top_n} Produk</div>
        <div class="chart-subtitle">Volume aktual produksi per komoditas</div>
    """, unsafe_allow_html=True)

    if not df.empty:
        df_top = (
            df.groupby('Nama_Produk')['Aktual_Produksi']
            .sum().reset_index()
            .sort_values('Aktual_Produksi', ascending=True)
            .tail(top_n)
        )
        # Gradient colors indigo→violet
        BAR_SHADES = ['#4338ca','#4f46e5','#6366f1','#818cf8','#a5b4fc',
                      '#c7d2fe','#ddd6fe','#ede9fe','#f5f3ff','#faf5ff']

        fig_bar = go.Figure(go.Bar(
            x=df_top['Aktual_Produksi'],
            y=df_top['Nama_Produk'],
            orientation='h',
            marker=dict(
                color=BAR_SHADES[:len(df_top)],
                line=dict(width=0),
                opacity=0.9
            ),
            text=df_top['Aktual_Produksi'].apply(lambda x: f'{x:,}'),
            textposition='outside',
            textfont=dict(size=11, color='#8b92b8'),
            hovertemplate='<b>%{y}</b><br>Produksi: %{x:,} unit<extra></extra>'
        ))
        fig_bar.update_layout(
            **PLOTLY_LAYOUT,
            height=max(230, top_n * 50),
            xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                       tickfont=dict(size=11, color='#8b92b8')),
            yaxis=dict(showgrid=False, tickfont=dict(size=11, color='#c4c9e2')),
            bargap=0.38,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Tidak ada data produk.")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">⚙️ Downtime per Mesin</div>
        <div class="chart-subtitle">Total menit downtime berdasarkan jenis mesin</div>
    """, unsafe_allow_html=True)

    if not df.empty and df['Downtime'].sum() > 0:
        df_dt = (
            df.groupby('Jenis_Mesin')['Downtime']
            .sum().reset_index()
            .sort_values('Downtime', ascending=False)
        )
        AMBER_SHADES = ['#f59e0b','#fbbf24','#fcd34d','#fde68a','#fef3c7','#fffbeb']

        fig_dt = go.Figure(go.Bar(
            x=df_dt['Jenis_Mesin'],
            y=df_dt['Downtime'],
            marker=dict(color=AMBER_SHADES[:len(df_dt)], line=dict(width=0), opacity=0.9),
            text=df_dt['Downtime'].apply(lambda x: f'{x} min'),
            textposition='outside',
            textfont=dict(size=11, color='#8b92b8'),
            hovertemplate='<b>%{x}</b><br>Downtime: %{y} menit<extra></extra>'
        ))
        fig_dt.update_layout(
            **PLOTLY_LAYOUT,
            height=max(230, len(df_dt) * 60),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#c4c9e2')),
            yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                       tickfont=dict(size=11, color='#8b92b8'), ticksuffix=' min'),
            bargap=0.4,
        )
        st.plotly_chart(fig_dt, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Tidak ada data downtime.")
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ============================================================
# ROW 3 — EFFICIENCY (full width)
# ============================================================
st.markdown("""
<div class="chart-card">
    <div class="chart-title">📊 Efisiensi Produksi per Produk</div>
    <div class="chart-subtitle">Perbandingan Target vs Aktual — top produk berdasarkan filter aktif</div>
""", unsafe_allow_html=True)

if not df.empty:
    df_eff = (
        df.groupby('Nama_Produk')
        .agg(Target=('Target_Produksi','sum'), Aktual=('Aktual_Produksi','sum'))
        .reset_index()
        .sort_values('Aktual', ascending=False)
        .head(top_n)
    )
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Bar(
        name='Target',
        x=df_eff['Nama_Produk'], y=df_eff['Target'],
        marker=dict(color='rgba(255,255,255,0.08)', line=dict(color='rgba(255,255,255,0.15)', width=1)),
        hovertemplate='<b>%{x}</b><br>Target: %{y:,}<extra></extra>'
    ))
    fig_eff.add_trace(go.Bar(
        name='Aktual',
        x=df_eff['Nama_Produk'], y=df_eff['Aktual'],
        marker=dict(color='#34d399', line=dict(width=0), opacity=0.85),
        hovertemplate='<b>%{x}</b><br>Aktual: %{y:,}<extra></extra>'
    ))
    eff_layout = PLOTLY_LAYOUT.copy()
    eff_layout['showlegend'] = True
    fig_eff.update_layout(
        **eff_layout,
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(size=11, color='#8b92b8'),
            bgcolor='rgba(0,0,0,0)'
        ),
        height=300,
        barmode='group',
        bargap=0.28,
        bargroupgap=0.06,
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#c4c9e2'), tickangle=-20),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                   tickfont=dict(size=11, color='#8b92b8')),
    )
    st.plotly_chart(fig_eff, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("Tidak ada data efisiensi.")

st.markdown("</div>", unsafe_allow_html=True)