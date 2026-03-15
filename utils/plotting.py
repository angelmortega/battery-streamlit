import matplotlib.pyplot as plt
import plotly.graph_objects as go

MODE_COLORS = {"CCC": "red", "CCD": "blue"}


def build_plot_sets(df_charge, df_discharge, view_mode):
    if view_mode == "Charge (CCC)":
        return [(df_charge, "CCC")]
    elif view_mode == "Discharge (CCD)":
        return [(df_discharge, "CCD")]
    return [(df_charge, "CCC"), (df_discharge, "CCD")]


def plot_matplotlib(plot_sets):
    fig, ax = plt.subplots(figsize=(6, 4))

    for df_subset, mode in plot_sets:
        color = MODE_COLORS[mode]
        for _, group in df_subset.groupby('CycleNo'):
            ax.plot(
                group['SpeCap/mAh/g'],
                group['Voltage/V'],
                color=color,
                alpha=0.8,
                linewidth=1.5,
            )

    ax.set_xlabel('SpeCap/mAh/g')
    ax.set_ylabel('Voltage/V')
    ax.set_title('Voltage vs Capacity')
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig


def plot_plotly(plot_sets):
    fig = go.Figure()

    for df_subset, mode in plot_sets:
        color = MODE_COLORS[mode]
        for cycle, group in df_subset.groupby('CycleNo'):
            fig.add_trace(
                go.Scatter(
                    x=group['SpeCap/mAh/g'],
                    y=group['Voltage/V'],
                    mode='lines',
                    line=dict(color=color, width=2),
                    opacity=0.8,
                    name=f"{mode} Cycle {cycle}",
                    hovertemplate=(
                        f"Mode: {mode}<br>"
                        f"Cycle: {cycle}<br>"
                        "SpeCap: %{x:.3f} mAh/g<br>"
                        "Voltage: %{y:.3f} V<br>"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

    fig.update_layout(
        title="Voltage vs Capacity",
        xaxis_title="SpeCap (mAh/g)",
        yaxis_title="Voltage (V)",
        height=450,
        margin=dict(l=40, r=20, t=60, b=40),
    )

    return fig
