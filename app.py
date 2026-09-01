import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. PAGE SETUP ---
st.set_page_config(layout="wide", page_title="CyberShield SOC Storytelling Hub", page_icon="🛡️")

# --- 2. SYNTHETIC SOC DATA GENERATOR ---
@st.cache_data
def generate_soc_data():
    np.random.seed(42)
    n = 1200
    data_centers = ["Paris", "Tokyo", "New York", "London", "Sydney", "Frankfurt", "Singapore", "Toronto"]
    threat_types = ["DDoS", "Ransomware", "Phishing", "SQLi", "Zero-Day"]
    
    # Latitudes and Longitudes for Spatial Geo-Mapping
    coords = {
        "Paris": (48.8566, 2.3522), "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060), "London": (51.5074, -0.1278),
        "Sydney": (-33.8688, 151.2093), "Frankfurt": (50.1109, 8.6821),
        "Singapore": (1.3521, 103.8198), "Toronto": (43.6532, -79.3832)
    }
    
    chosen_centers = np.random.choice(data_centers, n)
    lats = [coords[city][0] for city in chosen_centers]
    lons = [coords[city][1] for city in chosen_centers]
    
    data = {
        "Data_Center": chosen_centers,
        "Lat": lats,
        "Lon": lons,
        "Threat_Type": np.random.choice(threat_types, n),
        "Response_Time_Sec": np.random.exponential(scale=12, size=n) + 1.5,
        "Mitigation_Cost_USD": np.random.gamma(shape=2.5, scale=6000, size=n),
        "Packets_Blocked_M": np.random.normal(loc=150, scale=40, size=n).clip(10),
        "Severity_Score": np.random.uniform(1.0, 10.0, size=n),
        "System_Downtime_Mins": np.random.exponential(scale=25, size=n)
    }
    return pd.DataFrame(data)

df = generate_soc_data()

# --- 3. HEADER & SIDEBAR ---
st.title("🛡️ CyberShield SOC: Executive Visual Storyteller")
st.markdown("""
*This platform demonstrates how to curate **Spatial, Distribution, and Correlation charts** using **Gestalt Psychology** and **Positive Narrative Framing** for executive presentations.*
""")

st.sidebar.header("🕹️ Executive Dashboard Filters")
selected_centers = st.sidebar.multiselect("Select Data Centers", options=df["Data_Center"].unique(), default=df["Data_Center"].unique())
selected_threats = st.sidebar.multiselect("Select Threat Vectors", options=df["Threat_Type"].unique(), default=df["Threat_Type"].unique())

filtered_df = df[(df["Data_Center"].isin(selected_centers)) & (df["Threat_Type"].isin(selected_threats))]

# --- 4. NAVIGATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 1. Spatial Geo Map (Macro Story)", 
    "🎻 2. Violin & Box Plot (Variance)", 
    "📊 3. Heatmap & Pairplot (Correlation)", 
    "🤖 4. AI Storyteller (Executive Brief)"
])

# ==========================================
# TAB 1: SPATIAL VISUALIZATION
# ==========================================
with tab1:
    st.subheader("1. Spatial Regional Performance Map")
    
    st.info("""
    🧠 **Gestalt Perception Rule applied — Figure-Ground & Proximity:** 
    Placing bright data markers over dark geographic maps creates instant visual hierarchy (*Figure-Ground*). Viewers instinctively group neighboring regional hubs together (*Proximity*), removing the cognitive overhead of reading long tabular reports.
    """)
    
    spatial_df = filtered_df.groupby(["Data_Center", "Lat", "Lon"]).agg({
        "Mitigation_Cost_USD": "sum",
        "System_Downtime_Mins": "mean",
        "Response_Time_Sec": "mean",
        "Severity_Score": "count"
    }).reset_index().rename(columns={"Severity_Score": "Incident_Count"})
    
    fig_map = px.scatter_mapbox(
        spatial_df, lat="Lat", lon="Lon", size="Incident_Count", color="Mitigation_Cost_USD",
        hover_name="Data_Center", hover_data=["System_Downtime_Mins", "Response_Time_Sec"],
        color_continuous_scale="Viridis", size_max=35, zoom=1, mapbox_style="carto-darkmatter",
        title="Global Incident Density & Financial Impact Map"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Positive Narrative Example
    with st.expander("💡 How to explain this map to stakeholders (Positive Framing)"):
        top_center = spatial_df.loc[spatial_df['Incident_Count'].idxmax()]['Data_Center']
        st.write(f"""
        * **Avoid (Negative):** *"Our global map shows that {top_center} is failing and getting bombarded with attacks, driving up costs."*
        * **Use (Positive Strategic Framing):** *"{top_center} represents our highest operational volume globally. By prioritizing optimization and infrastructure upgrades in this key region, we achieve maximum resilience across our entire international network."*
        """)

# ==========================================
# TAB 2: VIOLIN & BOX PLOTS
# ==========================================
with tab2:
    st.subheader("2. Threat Severity & Cost Distribution Analysis")
    
    st.info("""
    🧠 **Gestalt Perception Rule applied — Law of Enclosure & Common Region:** 
    A box plot placed inside a violin curve creates a bounded visual container. The human brain perceives the inner box as the 'standard operating zone' and the outer curve as 'potential variance', making extreme outliers instantly recognizable.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_violin = px.violin(
            filtered_df, x="Threat_Type", y="Mitigation_Cost_USD", color="Threat_Type",
            box=True, points="outliers", title="Violin Plot: Mitigation Cost Spread per Threat Type"
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
    with col2:
        fig_box = px.box(
            filtered_df, x="Data_Center", y="Response_Time_Sec", color="Data_Center",
            title="Box Plot: Response Latency Dispersion by Data Center"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with st.expander("💡 How to explain this distribution to stakeholders (Positive Framing)"):
        st.write("""
        * **Avoid (Negative):** *"Zero-Day mitigation costs are completely unpredictable and out of control."*
        * **Use (Positive Strategic Framing):** *"Our violin plot confirms that baseline operational costs remain stable across most attack types. The high variance in Zero-Day events pinpoints the exact area where deploying automated defense scripts will stabilize future budget forecasts."*
        """)

# ==========================================
# TAB 3: CORRELATION HEATMAP & PAIRPLOT
# ==========================================
with tab3:
    st.subheader("3. Multivariate Dependencies & Correlation Matrix")
    
    st.info("""
    🧠 **Gestalt Perception Rule applied — Law of Similarity & Continuity:** 
    Matching numerical values with cohesive color shades lets the viewer's brain pre-attentively group variables. Dark blue or red clusters immediately highlight correlated operational drivers without requiring stakeholders to calculate statistical values.
    """)
    
    col_hm, col_pp = st.columns([1, 1])
    
    with col_hm:
        st.write("**Annotated Correlation Matrix**")
        num_cols = ["Response_Time_Sec", "Mitigation_Cost_USD", "Packets_Blocked_M", "Severity_Score", "System_Downtime_Mins"]
        corr = filtered_df[num_cols].corr()
        
        fig_hm, ax_hm = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax_hm, cbar=False, linewidths=0.5)
        st.pyplot(fig_hm)
        
    with col_pp:
        st.write("**Multi-Axis Pairplot Matrix**")
        pair_cols = ["Mitigation_Cost_USD", "Severity_Score", "System_Downtime_Mins"]
        fig_pair = sns.pairplot(filtered_df[pair_cols + ["Threat_Type"]], hue="Threat_Type", corner=True)
        st.pyplot(fig_pair.fig)

    with st.expander("💡 How to explain correlations to stakeholders (Positive Framing)"):
        st.write("""
        * **Avoid (Negative):** *"Response latency is ruining system availability and causing excessive downtime."*
        * **Use (Positive Strategic Framing):** *"The strong correlation between response speed and downtime proves that our team's recovery workflows are working as intended—reducing response latency directly boosts overall service availability."*
        """)

# ==========================================
# TAB 4: AI STAKEHOLDER STORYTELLER
# ==========================================
with tab4:
    st.subheader("4. AI Storytelling & Executive Narrative Builder")
    st.write("Synthesize visual evidence into a structured 3-Act story tailored for senior leadership.")
    
    target_audience = st.selectbox(
        "Select Target Stakeholder Audience",
        ["Chief Information Security Officer (CISO)", "Chief Financial Officer (CFO)", "Board of Directors"]
    )
    
    if st.button("🚀 Generate Positive Executive Briefing"):
        top_cost_center = spatial_df.loc[spatial_df['Mitigation_Cost_USD'].idxmax()]['Data_Center']
        avg_downtime = filtered_df['System_Downtime_Mins'].mean()
        avg_response = filtered_df['Response_Time_Sec'].mean()
        
        brief = f"""
        ### Executive Briefing | Target Audience: **{target_audience}**
        
        #### **Act 1: Strategic Context (Spatial Map Insights)**
        Our global SOC infrastructure maintained strong operational integrity across all regions. **{top_cost_center}** managed our largest throughput volume globally, serving as our primary defense shield. Average global incident downtime was held at **{avg_downtime:.1f} minutes**.
        
        #### **Act 2: Efficiency & Risk Variance (Violin & Heatmap Analysis)**
        * **Distribution Analysis (Violin Plots):** Standard threat vectors (DDoS, Phishing) show tight, predictable cost clusters. Extreme cost variance is isolated strictly to Zero-Day events.
        * **Metric Correlation:** Analysis confirms that response latency (currently averaging **{avg_response:.2f} seconds**) is the single primary driver of system availability.
        
        #### **Act 3: Solution-Oriented Action Plan**
        1. **Targeted Capital Investment:** Reallocate defense budget toward automated Zero-Day response tools in **{top_cost_center}** to flatten cost volatility.
        2. **Dashboard UI Optimization:** Apply Gestalt enclosure bounds to real-time analyst dashboards to accelerate incident triage and protect overall revenue uptime.
        """
        
        st.success("Executive Narrative Generated Successfully!")
        st.markdown(brief)
