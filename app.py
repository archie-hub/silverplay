import os
import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output

from data import create_ratio, get_melt_prices

GOLDHOLDINGS = int(os.getenv("goldholdings", 52))
SILVERHOLDINGS = int(os.getenv("silverholdings", 625))
MYHOLDINGS = os.getenv("myholdingsstring", "my new string")

app = Dash(__name__, title="Work in progress")
server = app.server

STATE = "ok"


@server.route("/health")
def health_check():
    return STATE


# ──────────────── HELPER ────────────────
def slider(min, max, step, value, id):
    """Create a slider showing only significant marks."""
    # Determine interval for marks to show only significant numbers
    interval = max // 5 if max > 0 else 1
    marks = {i: str(i) for i in range(min, max + 1, interval)}
    return dcc.Slider(
        id=id,
        min=min,
        max=max,
        step=step,
        value=value,
        updatemode="drag",
        marks=marks,
        tooltip={"placement": "top", "always_visible": False},  # only show while dragging
    )


# ──────────────── LAYOUT ────────────────
app.layout = html.Div(
    [
        # ──────────────── ROW 1 ────────────────
        html.Div(
            [
                dcc.Graph(id="gauge", style={"width": "25%"}),
                dcc.Graph(id="silver-price-gauge", style={"width": "25%"}),
                dcc.Graph(id="gold-price-gauge", style={"width": "25%"}),
                dcc.Graph(id="total-value-gauge", style={"width": "25%"}),
            ],
            style={"display": "flex"},
        ),

        html.H1(MYHOLDINGS, style={"textAlign": "center"}),

        # ──────────────── ROW 2 ────────────────
        html.Div(
            [
                dcc.Graph(id="gold-value-gauge", style={"width": "25%"}),
                dcc.Graph(id="silver-value-gauge", style={"width": "25%"}),
                dcc.Graph(id="required-gold-price-gauge", style={"width": "25%"}),
                dcc.Graph(id="required-silver-price-gauge", style={"width": "25%"}),
            ],
            style={"display": "flex"},
        ),

        # ──────────────── WISH GAUGES ────────────────
        html.Div(
            [
                dcc.Graph(id="silver_wish", style={"width": "45%"}),
                dcc.Graph(id="gold_wish", style={"width": "45%"}),
            ],
            style={"display": "flex", "justifyContent": "space-evenly"},
        ),

        # ──────────────── CONTROLS ────────────────
        html.Div(
            [
                html.Button(
                    "⚙ Controls",
                    id="toggle-controls",
                    n_clicks=0,
                    style={
                        "width": "100%",
                        "padding": "12px",
                        "fontSize": "18px",
                        "background": "#222",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                    },
                ),

                html.Div(
                    [
                        html.Label("Gold Oz Held"),
                        slider(0, 100, 1, GOLDHOLDINGS, "gold"),

                        html.Label("Gold $ Spent"),
                        slider(0, 100000, 100, 20000, "goldoutlay"),

                        html.Label("Silver Oz Held"),
                        slider(0, 1000, 1, SILVERHOLDINGS, "silver"),

                        html.Label("Silver $ Spent"),
                        slider(0, 50000, 100, 20000, "silveroutlay"),

                        html.Label("Ideal Holdings ($)"),
                        slider(0, 1_000_000, 1000, 500000, "ideal"),

                        html.Label("Silver Dream Price $/oz"),
                        slider(0, 4000, 10, 1000, "silverdreamprice"),

                        html.Label("Gold Dream Price $/oz"),
                        slider(0, 30000, 100, 25000, "golddreamprice"),
                    ],
                    id="controls-panel",
                    style={
                        "maxHeight": "0px",
                        "overflow": "hidden",
                        "opacity": "0",
                        "padding": "0 24px",
                        "transition": "all 0.4s cubic-bezier(.34,1.56,.64,1)",
                        "background": "white",
                        "borderTop": "1px solid #ddd",
                    },
                ),
            ],
            style={
                "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "zIndex": 1000,
            },
        ),

        dcc.Interval(id="interval-component", interval=120000),
    ],
    style={"paddingBottom": "340px"},
)


# ──────────────── CONTROLS ANIMATION ────────────────
@app.callback(
    Output("controls-panel", "style"),
    Input("toggle-controls", "n_clicks"),
)
def animate_controls(n):
    open_panel = n % 2 == 1
    return {
        "maxHeight": "600px" if open_panel else "0px",
        "opacity": "1" if open_panel else "0",
        "padding": "12px 24px" if open_panel else "0 24px",
        "overflow": "auto" if open_panel else "hidden",
        "transition": "all 0.4s cubic-bezier(.34,1.56,.64,1)",
        "background": "white",
        "borderTop": "1px solid #ddd",
    }


# ──────────────── GAUGES ────────────────
@app.callback(
    [
        Output("gauge", "figure"),
        Output("silver-price-gauge", "figure"),
        Output("gold-price-gauge", "figure"),
        Output("total-value-gauge", "figure"),
        Output("gold-value-gauge", "figure"),
        Output("silver-value-gauge", "figure"),
        Output("required-gold-price-gauge", "figure"),
        Output("required-silver-price-gauge", "figure"),
        Output("silver_wish", "figure"),
        Output("gold_wish", "figure"),
    ],
    [
        Input("gold", "value"),
        Input("silver", "value"),
        Input("silveroutlay", "value"),
        Input("goldoutlay", "value"),
        Input("ideal", "value"),
        Input("silverdreamprice", "value"),
        Input("golddreamprice", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_charts(
    gold, silver, silveroutlay, goldoutlay, ideal, silverdreamprice, golddreamprice, _
):
    goldvalue, silvervalue = get_melt_prices(silver, gold)

    gold_price = goldvalue["meltprice"]
    silver_price = silvervalue["meltprice"]

    gold_dollar_value = goldvalue["values"]
    silver_dollar_value = silvervalue["values"]

    total = gold_dollar_value + silver_dollar_value
    ratio = round(float(create_ratio(gold_price, silver_price)),2)
    print(ratio,777)
    
    #ratio = float(create_ratio(gold_price, silver_price),2)

    def dollar_gauge(value, title, color):
        print(value)
        return go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                number={"valueformat": "$,.2f"},
                #number={"valueformat": ".2f"},
                title={"text": title},
                gauge={
                    "axis": {"range": [0, value * 1.25 if value else 1]},
                    "bar": {"color": color},
                },
            )
        )

    return (
        go.Figure(go.Indicator(mode="gauge+number", value=ratio, title={"text": "G/S Ratio"})),
        dollar_gauge(silver_price, "Silver $/oz", "silver"),
        dollar_gauge(gold_price, "Gold $/oz", "gold"),
        dollar_gauge(total, "Total Holdings ($)", "green"),
        dollar_gauge(gold_dollar_value, "Gold Holdings ($)", "gold"),
        dollar_gauge(silver_dollar_value, "Silver Holdings ($)", "silver"),
        dollar_gauge(ideal / max(gold, 1), "Required Gold $/oz", "blue"),
        dollar_gauge(ideal / max(silver, 1), "Required Silver $/oz", "powderblue"),
        dollar_gauge(silver * silverdreamprice, "Silver Dream Value", "silver"),
        dollar_gauge(gold * golddreamprice, "Gold Dream Value", "gold"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
