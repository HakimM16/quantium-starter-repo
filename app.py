import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])

regions = sorted(df["region"].unique())
region_options = [{"label": "All Regions", "value": "all"}] + [
    {"label": r.title(), "value": r} for r in regions
]

app = dash.Dash(__name__)
app.title = "Soul Foods – Pink Morsel Sales"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Soul Foods: Pink Morsel Sales", style={"textAlign": "center"}),
        html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "16px", "marginBottom": "24px"},
            children=[
                html.Label("Filter by Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=region_options,
                    value="all",
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "16px"},
                ),
            ],
        ),
        dcc.Graph(id="sales-chart"),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df.groupby("date", as_index=False)["sales"].sum()
        filtered["region"] = "All Regions"
        fig = px.line(
            filtered,
            x="date",
            y="sales",
            title="Total Daily Sales – All Regions",
            labels={"date": "Date", "sales": "Sales ($)"},
        )
    else:
        filtered = df[df["region"] == selected_region].copy()
        fig = px.line(
            filtered,
            x="date",
            y="sales",
            title=f"Daily Sales – {selected_region.title()}",
            labels={"date": "Date", "sales": "Sales ($)"},
            color_discrete_sequence=["#e07b39"],
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis={"showgrid": True, "gridcolor": "#eeeeee"},
        yaxis={"showgrid": True, "gridcolor": "#eeeeee"},
        hovermode="x unified",
    )
    fig.update_traces(line_width=2)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
