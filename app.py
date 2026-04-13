import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])

REGION_COLOURS = {
    "all":   ("#e63946", "rgba(230,57,70,0.1)"),
    "north": ("#457b9d", "rgba(69,123,157,0.1)"),
    "south": ("#2a9d8f", "rgba(42,157,143,0.1)"),
    "east":  ("#e9c46a", "rgba(233,196,106,0.1)"),
    "west":  ("#f4a261", "rgba(244,162,97,0.1)"),
}

RADIO_OPTIONS = [
    {"label": "All",   "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "South", "value": "south"},
    {"label": "East",  "value": "east"},
    {"label": "West",  "value": "west"},
]

app = dash.Dash(__name__)
app.title = "Soul Foods – Pink Morsel Sales"

app.layout = html.Div(
    id="app-container",
    children=[
        # Header
        html.Div(
            id="header",
            children=[
                html.H1("Soul Foods: Pink Morsel Sales"),
                html.P("Daily revenue from Pink Morsels across all regions"),
            ],
        ),

        # Filter card
        html.Div(
            id="filter-card",
            children=[
                html.Span("Region", id="filter-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=RADIO_OPTIONS,
                    value="all",
                    className="radio-group",
                    inputStyle={"display": "none"},
                    labelStyle={},
                ),
            ],
        ),

        # Chart card
        html.Div(
            id="chart-card",
            children=[dcc.Graph(id="sales-chart", config={"displayModeBar": False})],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    if region == "all":
        data = df.groupby("date", as_index=False)["sales"].sum()
        title = "Total Daily Sales – All Regions"
    else:
        data = df[df["region"] == region].copy()
        title = f"Daily Sales – {region.title()}"

    colour, fill_colour = REGION_COLOURS[region]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["sales"],
            mode="lines",
            line={"color": colour, "width": 2.5},
            fill="tozeroy",
            fillcolor=fill_colour,
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 16, "color": "#1a202c", "family": "Inter, Arial, sans-serif"},
            "x": 0.0,
            "xanchor": "left",
            "pad": {"l": 8},
        },
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin={"t": 48, "b": 32, "l": 60, "r": 20},
        xaxis={
            "showgrid": False,
            "zeroline": False,
            "tickfont": {"size": 11, "color": "#718096"},
            "title": {"text": "Date", "font": {"size": 12, "color": "#718096"}},
        },
        yaxis={
            "showgrid": True,
            "gridcolor": "#edf2f7",
            "zeroline": False,
            "tickprefix": "$",
            "tickformat": ",.0f",
            "tickfont": {"size": 11, "color": "#718096"},
            "title": {"text": "Sales", "font": {"size": 12, "color": "#718096"}},
        },
        hovermode="x unified",
        hoverlabel={
            "bgcolor": "#1a202c",
            "font_color": "#ffffff",
            "font_size": 13,
        },
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
