"""
Generate example interactive Plotly charts for the visualization gallery.
Run: python scripts/generate-example-plots.py

Output: docs/assets/plots/*.html  (interactive HTML files)
         docs/assets/images/*.png  (static PNG fallbacks)
"""

import os
import numpy as np
import pandas as pd

# --- 确保输出目录存在 ---
os.makedirs("docs/assets/plots", exist_ok=True)
os.makedirs("docs/assets/images", exist_ok=True)

# ============================================================
# 1. Forest Plot
# ============================================================
def make_forest_plot():
    import plotly.graph_objects as go

    forest_data = pd.DataFrame({
        "Subgroup": ["Overall", "Age < 65", "Age ≥ 65", "Male", "Female",
                     "Region Asia", "Region EU", "Region US"],
        "HR": [0.72, 0.68, 0.78, 0.74, 0.70, 0.71, 0.73, 0.69],
        "Lower": [0.58, 0.48, 0.55, 0.53, 0.50, 0.49, 0.51, 0.47],
        "Upper": [0.89, 0.96, 1.10, 1.03, 0.98, 1.02, 1.04, 1.01],
        "p_value": ["0.003", "0.032", "0.145", "0.067", "0.052",
                    "0.062", "0.058", "0.041"]
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forest_data["HR"],
        y=forest_data["Subgroup"],
        mode="markers",
        marker=dict(size=12, color="#1f77b4", line=dict(color="white", width=1)),
        error_x=dict(
            type="data", symmetric=False,
            arrayminus=forest_data["HR"] - forest_data["Lower"],
            array=forest_data["Upper"] - forest_data["HR"],
            thickness=2, color="#1f77b4"
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "HR: %{x:.2f}<br>"
            "95%% CI: (%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>"
            "p = %{customdata[2]}<extra></extra>"
        ),
        customdata=np.column_stack([
            forest_data["Lower"], forest_data["Upper"], forest_data["p_value"]
        ])
    ))

    fig.add_vline(x=1, line_dash="dash", line_color="gray", line_width=1,
                  annotation_text="HR = 1", annotation_position="top right")

    # 右侧文本注释
    annotations = []
    for i, (_, row) in enumerate(forest_data.iterrows()):
        annotations.append(dict(
            x=1.45, y=row["Subgroup"],
            xref="x", yref="y",
            text=f"{row['HR']:.2f} ({row['Lower']:.2f}, {row['Upper']:.2f})",
            showarrow=False,
            font=dict(size=10),
            xanchor="left"
        ))

    fig.update_layout(
        title=dict(text="Forest Plot — Subgroup Analysis", x=0.5),
        xaxis=dict(
            title="Hazard Ratio (95% CI)",
            range=[0.3, 1.8],
            zeroline=False
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=forest_data["Subgroup"][::-1]
        ),
        height=400,
        margin=dict(l=20, r=200, t=50, b=50),
        hovermode="y",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    fig.write_html("docs/assets/plots/forest-plot.html")
    fig.write_image("docs/assets/images/forest-plot-example.png", scale=2)
    print("  [OK] Forest Plot")

# ============================================================
# 2. KM Curve
# ============================================================
def make_km_curve():
    import plotly.graph_objects as go
    from lifelines import KaplanMeierFitter

    np.random.seed(42)
    n = 100
    adtte_treat = pd.DataFrame({
        "avalu": np.random.exponential(18, n),
        "event": np.random.binomial(1, 0.7, n),
    })
    adtte_ctrl = pd.DataFrame({
        "avalu": np.random.exponential(12, n),
        "event": np.random.binomial(1, 0.8, n),
    })

    kmf_treat = KaplanMeierFitter()
    kmf_ctrl = KaplanMeierFitter()
    kmf_treat.fit(adtte_treat["avalu"], adtte_treat["event"], label="Drug")
    kmf_ctrl.fit(adtte_ctrl["avalu"], adtte_ctrl["event"], label="Placebo")

    fig = go.Figure()

    for kmf, color, dash in [(kmf_treat, "#1f77b4", "solid"),
                               (kmf_ctrl, "#ff7f0e", "solid")]:
        sf = kmf.survival_function_
        ci = kmf.confidence_interval_
        fig.add_trace(go.Scatter(
            x=sf.index, y=sf.iloc[:, 0],
            mode="lines", name=kmf._label,
            line=dict(color=color, width=2.5),
            legendgroup=kmf._label,
        ))
        fig.add_trace(go.Scatter(
            x=sf.index.tolist()[::-1] + sf.index.tolist(),
            y=ci.iloc[:, 1].tolist()[::-1] + ci.iloc[:, 0].tolist(),
            fill="toself", fillcolor=color,
            opacity=0.15, name=kmf._label,
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False, legendgroup=kmf._label,
            hoverinfo="skip"
        ))

    fig.update_layout(
        title=dict(text="Kaplan-Meier Survival Curve", x=0.5),
        xaxis=dict(title="Time (months)", range=[0, 30]),
        yaxis=dict(title="Survival Probability", range=[0, 1]),
        height=400,
        hovermode="x",
        legend=dict(title="Treatment", yanchor="top", y=0.99, x=0.99),
        plot_bgcolor="rgba(0,0,0,0)",
    )

    fig.write_html("docs/assets/plots/km-curve.html")
    # KM curve image skipped — uses lifelines data
    print("  [OK] KM Curve")

# ============================================================
# 3. Boxplot + Violin
# ============================================================
def make_boxplot_violin():
    import plotly.express as px

    np.random.seed(42)
    n = 60
    bp_data = pd.DataFrame({
        "Treatment": ["Drug"] * n + ["Placebo"] * n,
        "Endpoint": np.concatenate([
            np.random.normal(45, 10, n),
            np.random.normal(50, 12, n)
        ])
    })

    fig = px.violin(bp_data, x="Treatment", y="Endpoint", color="Treatment",
                    box=True, points="all",
                    title="Boxplot + Violin — Distribution by Treatment",
                    color_discrete_map={"Drug": "#1f77b4", "Placebo": "#ff7f0e"})
    fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)")
    fig.write_html("docs/assets/plots/boxplot-violin.html")
    fig.write_image("docs/assets/images/boxplot-violin-example.png", scale=2)
    print("  [OK] Boxplot / Violin")

# ============================================================
# 4. Swimmer Plot
# ============================================================
def make_swimmer_plot():
    import plotly.express as px

    swimmer_data = pd.DataFrame({
        "Subject": [f"S{i}" for i in range(1, 21)],
        "Response": ["CR"]*3 + ["PR"]*5 + ["SD"]*7 + ["PD"]*5,
        "Duration": [24,20,18,22,19,16,15,14,13,12,
                     11,10,9,8,7,6,5,4,3,2]
    })

    color_map = {"CR": "#2ca02c", "PR": "#1f77b4",
                 "SD": "#ff7f0e", "PD": "#d62728"}

    fig = px.bar(swimmer_data, x="Duration", y="Subject",
                 color="Response", color_discrete_map=color_map,
                 orientation="h",
                 title="Swimmer Plot — Individual Patient Response")
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True
    )
    fig.write_html("docs/assets/plots/swimmer-plot.html")
    fig.write_image("docs/assets/images/swimmer-plot-example.png", scale=2)
    print("  [OK] Swimmer Plot")

# ============================================================
# 5. Waterfall Plot
# ============================================================
def make_waterfall_plot():
    import plotly.graph_objects as go

    wf_data = pd.DataFrame({
        "Subject": [f"S{i}" for i in range(1, 41)],
        "PctChange": [-100,-85,-72,-65,-60,-55,-50,-45,-40,-35,
                      -30,-28,-25,-22,-20,-18,-15,-12,-10,-8,
                      -5,-2,0,5,8,10,12,15,18,20,
                      22,25,28,30,35,40,50,60,75,100]
    })

    colors = ["#1f77b4" if x <= -30 else "#ff7f0e" if x <= 20 else "#d62728"
              for x in wf_data["PctChange"]]

    fig = go.Figure(data=go.Bar(
        x=wf_data["Subject"], y=wf_data["PctChange"],
        marker_color=colors,
        hovertemplate="Subject: %{x}<br>Change: %{y:.1f}%<extra></extra>"
    ))

    fig.add_hline(y=-30, line_dash="dash", line_color="green",
                  annotation_text="PR (-30%)", annotation_position="top left")
    fig.add_hline(y=20, line_dash="dash", line_color="red",
                  annotation_text="PD (+20%)", annotation_position="top left")

    fig.update_layout(
        title=dict(text="Waterfall Plot — Best Tumor Response", x=0.5),
        xaxis_showticklabels=False,
        yaxis_title="Best Change from Baseline (%)",
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.write_html("docs/assets/plots/waterfall-plot.html")
    fig.write_image("docs/assets/images/waterfall-plot-example.png", scale=2)
    print("  [OK] Waterfall Plot")

# ============================================================
# 6. Volcano Plot
# ============================================================
def make_volcano_plot():
    import plotly.express as px

    np.random.seed(123)
    volcano_data = pd.DataFrame({
        "log2FC": np.random.normal(0, 1.5, 500),
        "pval": np.random.uniform(0, 1, 500)
    })
    volcano_data["logp"] = -np.log10(volcano_data["pval"])

    conditions = [
        (abs(volcano_data["log2FC"]) > 1) & (volcano_data["pval"] < 0.05),
        (abs(volcano_data["log2FC"]) > 1),
        (volcano_data["pval"] < 0.05)
    ]
    choices = ["Significant", "FC only", "p only"]
    volcano_data["Category"] = np.select(conditions, choices, default="NS")

    fig = px.scatter(volcano_data, x="log2FC", y="logp", color="Category",
                     color_discrete_map={
                         "Significant": "#d62728", "FC only": "#ff7f0e",
                         "p only": "#1f77b4", "NS": "gray"},
                     opacity=0.6,
                     title="Volcano Plot")
    fig.add_vline(x=-1, line_dash="dash", line_color="gray", line_width=1)
    fig.add_vline(x=1, line_dash="dash", line_color="gray", line_width=1)
    fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="gray",
                  line_width=1)
    fig.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="log₂(Fold Change)",
        yaxis_title="-log₁₀(p value)",
    )
    fig.write_html("docs/assets/plots/volcano-plot.html")
    fig.write_image("docs/assets/images/volcano-plot-example.png", scale=2)
    print("  [OK] Volcano Plot")

# ============================================================
# 7. Heatmap
# ============================================================
def make_heatmap():
    import plotly.express as px

    np.random.seed(42)
    vars = ["Biomarker1", "Biomarker2", "Biomarker3",
            "Age", "BMI", "BP_Sys", "BP_Dia", "Cholesterol"]
    n = len(vars)
    corr = np.random.uniform(-0.6, 0.8, (n, n))
    corr = (corr + corr.T) / 2
    np.fill_diagonal(corr, 1)

    fig = px.imshow(corr, x=vars, y=vars,
                    color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1,
                    title="Correlation Heatmap of Clinical Variables",
                    text_auto=".2f",
                    aspect="auto")
    fig.update_layout(height=500)
    fig.write_html("docs/assets/plots/heatmap.html")
    fig.write_image("docs/assets/images/heatmap-example.png", scale=2)
    print("  [OK] Heatmap")

# ============================================================
# 8. CONSORT Diagram (Mermaid — static placeholder)
# ============================================================
def make_consort_placeholder():
    """CONSORT uses Mermaid in Markdown, no Python generation needed."""
    print("  [OK] CONSORT Diagram (Mermaid in Markdown)")

# ============================================================
# 9. Spaghetti Plot
# ============================================================
def make_spaghetti_plot():
    import plotly.graph_objects as go

    np.random.seed(123)
    n_subj = 20
    visits = [0, 4, 8, 12, 16, 20, 24]

    rows = []
    for i in range(n_subj):
        trt = "Drug" if i < 10 else "Placebo"
        bl = np.random.normal(50, 10)
        slope = -2 if trt == "Drug" else -0.5
        for v in visits:
            rows.append({
                "Subject": f"S{i+1}", "Treatment": trt,
                "Visit": v, "Value": bl + slope*v + np.random.normal(0, 3)
            })
    spag_data = pd.DataFrame(rows)

    fig = go.Figure()

    for subj in spag_data["Subject"].unique():
        subj_data = spag_data[spag_data["Subject"] == subj]
        trt = subj_data["Treatment"].iloc[0]
        color = "#1f77b4" if trt == "Drug" else "#ff7f0e"
        fig.add_trace(go.Scatter(
            x=subj_data["Visit"], y=subj_data["Value"],
            mode="lines+markers", opacity=0.3,
            line=dict(color=color, width=0.8),
            marker=dict(size=3, color=color),
            name=subj, legendgroup=trt,
            showlegend=False,
            hovertemplate=f"Subject: {subj}<br>Visit: %{{x}}<br>Value: %{{y:.1f}}<extra></extra>"
        ))

    means = spag_data.groupby(["Treatment", "Visit"])["Value"].mean().reset_index()
    for trt, color in [("Drug", "#1f77b4"), ("Placebo", "#ff7f0e")]:
        trt_means = means[means["Treatment"] == trt]
        fig.add_trace(go.Scatter(
            x=trt_means["Visit"], y=trt_means["Value"],
            mode="lines+markers",
            line=dict(color=color, width=4),
            marker=dict(size=10, color=color),
            name=f"{trt} (Mean)"
        ))

    fig.update_layout(
        title=dict(text="Spaghetti Plot — Individual Trajectories", x=0.5),
        xaxis=dict(title="Visit (weeks)", dtick=4),
        yaxis=dict(title="Endpoint Value"),
        height=400,
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.write_html("docs/assets/plots/spaghetti-plot.html")
    fig.write_image("docs/assets/images/spaghetti-plot-example.png", scale=2)
    print("  [OK] Spaghetti Plot")

# ============================================================
# 10. Interaction Plot
# ============================================================
def make_interaction_plot():
    import plotly.express as px

    interact_data = pd.DataFrame({
        "Treatment": ["Drug", "Drug", "Drug", "Placebo", "Placebo", "Placebo"],
        "Biomarker": ["Low", "Medium", "High"] * 2,
        "Endpoint": [12, 10, 8, 10, 10, 10]
    })

    fig = px.line(interact_data, x="Biomarker", y="Endpoint",
                  color="Treatment", markers=True,
                  title="Treatment × Biomarker Interaction",
                  color_discrete_map={"Drug": "#1f77b4", "Placebo": "#ff7f0e"})
    fig.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[7, 13]),
    )
    fig.write_html("docs/assets/plots/interaction-plot.html")
    fig.write_image("docs/assets/images/interaction-plot-example.png", scale=2)
    print("  [OK] Interaction Plot")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Generating example plots...")
    make_forest_plot()
    make_km_curve()
    make_boxplot_violin()
    make_swimmer_plot()
    make_waterfall_plot()
    make_volcano_plot()
    make_heatmap()
    make_consort_placeholder()
    make_spaghetti_plot()
    make_interaction_plot()
    print("\nAll plots generated in docs/assets/")
