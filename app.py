import os
import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output

from data import create_ratio, get_melt_prices

GOLDHOLDINGS = int(os.getenv("goldholdings", 52))
SILVERHOLDINGS = int(os.getenv("silverholdings", 618.5))
MYHOLDINGS = os.getenv("myholdingsstring", "my new string")

app = Dash(__name__, title="Work in progress")
server = app.server

STATE = "ok"


@server.route("/health")
def health_check():
    return STATE


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
            style={"display": "flex", "justifyContent": "center"},
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
            style={"display": "flex", "justifyContent": "center"},
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
                html.Label("Gold Oz Held"),
                dcc.Slider(id="gold", min=0, max=100, step=1, value=GOLDHOLDINGS, marks={i: str(i) for i in range(0, 501, 25)},),

                html.Label("Gold $ Spent"),
                dcc.Slider(id="goldoutlay", min=0, max=100000, value=20000),

                html.Label("Silver Oz Held"),
                dcc.Slider(id="silver", min=0, max=1000, value=SILVERHOLDINGS,  marks={i: str(i) for i in range(0, 1001, 100)},),

                html.Label("Silver $ Spent"),
                dcc.Slider(id="silveroutlay", min=0, max=50000, value=20000),

                html.Label("Ideal Holdings ($)"),
                dcc.Slider(id="ideal", min=0, max=1000000, value=500000),

                html.Label("Silver Dream Price $/oz"),
                dcc.Slider(id="silverdreamprice", min=0, max=4000, value=1000),

                html.Label("Gold Dream Price $/oz"),
                dcc.Slider(id="golddreamprice", min=0, max=30000, value=25000),
            ],
            style={
                "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "background": "white",
                "padding": "0 24px",   # left & right
                "boxSizing": "border-box"
            },
        ),

        dcc.Interval(id="interval-component", interval=120000),
    ]
)


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
    ratio = int(create_ratio(gold_price, silver_price))

    def dollar_gauge(value, title, color):
        return go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                number={"valueformat": "$,.2f"},
                title={"text": title},
                gauge={
                    "axis": {"range": [0, value * 1.25]},
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

