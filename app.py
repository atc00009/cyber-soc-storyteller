import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. PAGE SETUP ---
st.set_page_config(
    layout="wide", 
    page_title="CyberShield SOC | Executive Dashboard", 
    page_icon="🛡️"
)

# --- 2. CLEAN SLATE DARK THEME CSS ---
st.markdown("""
<style>
    /* Dark Slate Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Clean Cards */
    div.css-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-family: monospace;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    /* Multi-select Badges (Cyan / Dark Text) */
    span[data-baseweb="tag"] {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        font-weight: 600;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA GENERATOR ---
@st.cache_data
def generate_soc_data():
    np.random.seed(42)
    n = 1200
    data_centers = ["Paris", "Tokyo", "New York", "London", "Sydney", "Frankfurt", "Singapore", "Toronto"]
    threat_types = ["DDoS", "Ransomware", "Phishing", "SQLi", "Zero-Day"]
    
    coords = {
        "Paris": (48.8566, 2.3522), "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060), "London": (51.5074, -0.1278),
        "Sydney": (-33.8688, 151.2093), "Frankfurt": (50.1109, 8.6821),
        "Singapore": (1.3521, 103.8198), "Toronto": (43.6532, -79.3832)
    }
    
    chosen_centers = np.random.choice(data_centers, n)
    lats = [coords[city][0] for city in chosen_centers]
    lons = [coords[city][1] for city in chosen_centers]
    
    return pd.DataFrame({
        "Data_Center": chosen_centers,
        "Lat": lats,
        "Lon": lons,
        "Threat_Type": np.random.choice(threat_types, n),
        "Response_Time_Sec": np.random.exponential(scale=12, size=n) + 1.5,
        "Mitigation_Cost_USD": np.random.gamma(shape=2.5, scale=6000, size=n),
        "Packets_Blocked_M": np.random.normal(loc=150, scale=40, size=n).clip(10),
        "Severity_Score": np.random.uniform(1.0, 10.0, size=n),
        "System_Downtime_Mins": np.random.exponential(scale=25, size=n)
    })

df = generate_soc_data()

# --- 4. HEADER ---
st.title("🛡️ CYBERSHIELD SOC: EXECUTIVE DASHBOARD")
st.caption("Applying Gestalt Visual Psychology (Enclosure, Proximity, Similarity) to Security Analytics")
st.markdown("---")

# Sidebar Controls
st.sidebar.markdown("### 🕹️ Executive Filters")
selected_centers = st.sidebar.multiselect("Data Centers", options=df["Data_Center"].unique(), default=df["Data_Center"].unique())
selected_threats = st.sidebar.multiselect("Threat Vectors", options=df["Threat_Type"].unique(), default=df["Threat_Type"].unique())

filtered_df = df[(df["Data_Center"].isin(selected_centers)) & (df["Threat_Type"].isin(selected_threats))]

# KPI Banner
k1, k2, k3, k4 = st.columns(4)
k1.metric("Global Incidents", f"{len(filtered_df):,}")
k2.metric("Total Cost", f"${filtered_df['Mitigation_Cost_USD'].sum()/1e6:.2f}M")
k3.metric("Avg Response Speed", f"{filtered_df['Response_Time_Sec'].mean():.1f}s")
k4.metric("Mean Downtime", f"{filtered_df['System_Downtime_Mins'].mean():.1f}m")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Spatial Map", 
    "🎻 Distribution (Box & Violin)", 
    "📊 Heatmap & Pairplot", 
    "🤖 AI Executive Briefing"
])

# --- TAB 1: SPATIAL MAP (WITH DYNAMIC AUTO-CENTERING & SIZE ATTRIBUTES) ---
with tab1:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("1. Spatial Regional Performance Mapping")
    st.caption("🧠 Gestalt Law applied: Figure-Ground & Proximity.")
    
    spatial_df = filtered_df.groupby(["Data_Center", "Lat", "Lon"]).agg({
        "Mitigation_Cost_USD": "sum",
        "System_Downtime_Mins": "mean",
        "Response_Time_Sec": "mean",
        "Severity_Score": "count"
    }).reset_index().rename(columns={"Severity_Score": "Incident_Count"})
    
    # Dynamic Map Centering Calculation
    avg_lat = spatial_df["Lat"].mean() if not spatial_df.empty else 20
    avg_lon = spatial_df["Lon"].mean() if not spatial_df.empty else 0
    map_zoom = 3 if len(spatial_df) < 3 else 1.5

    try:
        fig_map = px.scatter_map(
            spatial_df, 
            lat="Lat", 
            lon="Lon", 
            size="Incident_Count",             # SIZE ATTRIBUTE
            color="Mitigation_Cost_USD", 
            hover_name="Data_Center", 
            color_continuous_scale="Viridis",  # PALETTE ATTRIBUTE
            size_max=30,                       # SIZE RANGE
            zoom=map_zoom, 
            center={"lat": avg_lat, "lon": avg_lon}, # DYNAMIC RE-CENTERING
            title="Global Incident Density & Financial Impact Map"
        )
    except AttributeError:
        fig_map = px.scatter_geo(
            spatial_df, 
            lat="Lat", 
            lon="Lon", 
            size="Incident_Count",             # SIZE ATTRIBUTE
            color="Mitigation_Cost_USD", 
            hover_name="Data_Center", 
            color_continuous_scale="Viridis",  # PALETTE ATTRIBUTE
            size_max=30,
            title="Global Incident Density & Financial Impact Map"
        )
        
    fig_map.update_layout(template="plotly_dark", paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: VIOLIN & BOX PLOTS (ALPHA & PALETTE ATTRIBUTES) ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        fig_violin = px.violin(
            filtered_df, 
            x="Threat_Type", 
            y="Mitigation_Cost_USD", 
            color="Threat_Type",
            box=True, 
            points="outliers", 
            color_discrete_sequence=px.colors.qualitative.Plotly, # PALETTE
            title="Mitigation Cost Distribution"
        )
        fig_violin.update_traces(marker=dict(opacity=0.7))        # ALPHA ATTRIBUTE
        fig_violin.update_layout(template="plotly_dark", paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
        st.plotly_chart(fig_violin, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        fig_box = px.box(
            filtered_df, 
            x="Data_Center", 
            y="Response_Time_Sec", 
            color="Data_Center",
            color_discrete_sequence=px.colors.qualitative.Dark24, # PALETTE
            title="Regional Latency Variance"
        )
        fig_box.update_traces(marker=dict(opacity=0.8))           # ALPHA ATTRIBUTE
        fig_box.update_layout(template="plotly_dark", paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: HEATMAP & PAIRPLOT (HUE, PALETTE, MARKERS, ALPHA) ---
with tab3:
    c_hm, c_pp = st.columns([1, 1])
    with c_hm:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("Correlation Matrix")
        num_cols = ["Response_Time_Sec", "Mitigation_Cost_USD", "Packets_Blocked_M", "Severity_Score", "System_Downtime_Mins"]
        corr = filtered_df[num_cols].corr()
        
        fig_hm, ax_hm = plt.subplots(figsize=(6, 5))
        fig_hm.patch.set_facecolor('#1E293B')
        ax_hm.set_facecolor('#1E293B')
        
        # Seaborn Heatmap with Palette and Alpha
        sns.heatmap(
            corr, 
            annot=True, 
            fmt=".2f", 
            cmap="mako",               # PALETTE ATTRIBUTE
            alpha=0.9,                  # ALPHA ATTRIBUTE
            ax=ax_hm, 
            cbar=False, 
            annot_kws={"color": "white"}
        )
        ax_hm.tick_params(colors='white')
        st.pyplot(fig_hm)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_pp:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("Multivariate Pairplot Grid")
        pair_cols = ["Mitigation_Cost_USD", "Severity_Score", "System_Downtime_Mins"]
        
        # Seaborn Pairplot using Hue, Palette, Markers, and Alpha
        fig_pair = sns.pairplot(
            filtered_df[pair_cols + ["Threat_Type"]], 
            hue="Threat_Type",         # HUE ATTRIBUTE
            palette="viridis",         # PALETTE ATTRIBUTE
            markers=["o", "s", "D", "^", "v"], # MARKERS ATTRIBUTE
            plot_kws={"alpha": 0.6},    # ALPHA ATTRIBUTE
            corner=True
        )
        fig_pair.fig.patch.set_facecolor('#1E293B')
        for ax in fig_pair.axes.flatten():
            if ax is not None:
                ax.set_facecolor('#1E293B')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.tick_params(colors='white')
        st.pyplot(fig_pair.fig)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: AI STORYTELLER ---
with tab4:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.subheader("4. AI Stakeholder Narrative Engine")
    audience = st.selectbox("Target Stakeholder", ["CISO", "CFO", "Board of Directors"])
    
    if st.button("🚀 Generate Executive Briefing"):
        top_cost_center = spatial_df.loc[spatial_df['Mitigation_Cost_USD'].idxmax()]['Data_Center'] if not spatial_df.empty else "Global Hubs"
        st.success(f"**Executive Story generated for {audience}:** Operational volume is highest in {top_cost_center}. Targeting zero-day response automation in this hub will maximize overall system uptime.")
    st.markdown("</div>", unsafe_allow_html=True)
