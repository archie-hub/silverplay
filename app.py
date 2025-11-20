"""sds"""
import os
import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output
from flask import jsonify
from dash.development.update_components import status_print
#import jsonify

from data import create_ratio, get_melt_prices

GOLDHOLDINGS = int(os.getenv("goldholdings", 1))
SILVERHOLDINGS = int(os.getenv("silverholdings", 1))
MYHOLDINGS = os.getenv("myholdingsstring", "my new string")


#app = Dash(__name__,  routes_pathname_prefix='/silver/', title='Work in progress')
app = Dash(__name__,  title='Work in progress')

server = app.server

# @server.route("/health")
# def health_check():
#     try:
#         status = get_melt_prices(1, 1)
#         if not status or not isinstance(status, list) or 'meltprice' not in status[0]:
#             return jsonify(status="error", message="Invalid response from get_melt_prices()"), 500
#         melt_price = status[0]['meltprice']
#         health = "ok" if melt_price > 1 else "bad"
#         return jsonify(status=health, meltprice=melt_price), 200 if health == "ok" else 503
#
#     except Exception as e:
#         return jsonify(status="error", message=str(e)), 500
STATE = None
@server.route("/health")
def health_check():
    return STATE



app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id="gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="silver-price-gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="required-gold-price-gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="new-gauge-2",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "width": "100%",
                "padding": "0px 0",  # Reduce padding here if needed
            },
        ),
        html.H1(
            MYHOLDINGS,
            style={"textAlign": "center", "fontSize": "25px", "marginBottom": "1%"},
        ),
        # Second row of gauges
        html.Div(
            [
                dcc.Graph(
                    id="required-silver-price-gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="additional-gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="new-gauge-1",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
                dcc.Graph(
                    id="gold-price-gauge",
                    style={
                        "width": "25%",
                        "height": "10%",
                        "margin": "0px 5px",
                    },  # Adjusted height
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "width": "100%",
                "padding": "0px 0",  # Reduce padding here if needed
            },
        ),
        # Third row of gauges
        html.Div(
            [
                dcc.Graph(
                    id="silver_wish",
                    #style={'width': '55vh', 'height': '65vh', 'marginLeft': 'auto', 'marginRight': 'auto'},
style={
        'width': '55vh',         # Adjusted width for better fit
        'height': '55vh',        # Adjusted height to match
        'margin': '0 auto',      # Centers the gauge horizontally
        'padding-top': '2vh',}    # Small top padding for spacing
                ),
                dcc.Graph(
                    id="gold_wish",
                    # style={
                    #     "width": "25%",
                    #     "height": "25%",
                    #     #"margin": "250px",
                    # },  # Adjusted height
                    #style={'width': '55vh', 'height': '65vh', 'marginLeft': 'auto', 'marginRight': 'auto'},
                    # style={
                    #     'width': '55vh',
                    #     'height': '55vh',
                    #     'marginLeft': 'auto',
                    #     'marginRight': 'auto',
                    #     'marginTop': '0',       # Align with the top
                    #     #'position': 'relative',  # Ensure it's relative to the top
                    #     #'position': 'absolute',  # Align it to the top
                    #     #'top': '0',  # Set to top of its container
                    #                 "padding-top": "1vh",  # Reduce padding here if needed
                    # }
style={
        'width': '55vh',         # Adjusted width for better fit
        'height': '55vh',        # Adjusted height to match
        'margin': '0 auto',      # Centers the gauge horizontally
        'padding-top': '2vh',    # Small top padding for spacing
        #'border-radius': '15px', # Rounded corners for a modern look
        #'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow effect
        #'background-color': '#f9f9f9',  # Light background for contrast
    },
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "space-evenly",
                "width": "100%",
                'height': '45vh',

                #"height": "10%", # This
                #'marginTop': '0',  # Align with the top
                #'position': 'relative',  # Ensure it's relative to the top
                #"padding-bottom": "10%",  # Reduce padding here if needed
                "padding-bottom": "85vh",  # Reduce padding here if needed
                "padding-top": "1vh",  # Reduce padding here if needed

            },
            # style={
            #     'width': '55vh',
            #     'height': '65vh',
            #     'marginLeft': 'auto',
            #     'marginRight': 'auto',
            #     'marginTop': '0',       # Align with the top
            #     'position': 'relative'  # Ensure it's relative to the top
            # }
        ),
        html.Div(
            [
                # Row 1
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Gold Oz's held", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="gold",
                                    min=0,
                                    max=500,
                                    step=0.1,
                                    value=GOLDHOLDINGS,
                                    marks={i: str(i) for i in range(0, 501, 100)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Gold $'s spent", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="goldoutlay",
                                    min=0,
                                    max=100000,
                                    step=0.1,
                                    value=20000,
                                    marks={i: str(i) for i in range(0, 100001, 10000)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "width": "100%",
                    },
                ),
                # Row 2
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Silver Oz's held", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="silver",
                                    min=0,
                                    max=4000,
                                    # step=0.1,
                                    value=SILVERHOLDINGS,
                                    marks={i: str(i) for i in range(0, 4001, 500)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Silver $'s spent", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="silveroutlay",
                                    min=0,
                                    max=25000,
                                    step=100,
                                    value=20000,
                                    marks={i: str(i) for i in range(0, 50000, 5000)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "width": "100%",
                    },
                ),
                # Row 3
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Ideal holdings", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="ideal",
                                    min=0,
                                    max=1000000,
                                    value=500000,
                                    marks={
                                        i: str(i) for i in range(0, 1000001, 100000)
                                    },
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "width": "100%",
                    },
                ),
# Row 4
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Silver dream price $/oz", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="silverdreamprice",
                                    min=0,
                                    max=4000,
                                    # step=0.1,
                                    value=1000,
                                    marks={i: str(i) for i in range(0, 4001, 500)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Gold dream price $/oz", style={"fontSize": "18px"}
                                ),
                                dcc.Slider(
                                    id="golddreamprice",
                                    min=0,
                                    max=30001,
                                    step=100,
                                    value=25000,
                                    marks={i: str(i) for i in range(0, 30001, 2500)},
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "0 10px 0 0",
                                "paddingRight": "50px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "width": "100%",
                    },
                ),
            ],
            style={
                "width": "100%",
                "padding": "10px",
                "position": "fixed",
                "bottom": "0",
                "backgroundColor": "white",
                "boxShadow": "0px -2px 10px rgba(0, 0, 0, 0.1)",
            },
        ),
        # Interval for periodic updates
        dcc.Interval(id="interval-component", interval=120 * 1000, n_intervals=0),
    ]
)


# Define callback to update all gauges
@app.callback(
    [
        Output("gauge", "figure"),
        Output("additional-gauge", "figure"),
        Output("new-gauge-1", "figure"),
        Output("new-gauge-2", "figure"),
        Output("required-gold-price-gauge", "figure"),
        Output("silver-price-gauge", "figure"),
        Output("gold-price-gauge", "figure"),
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
        Input("interval-component", "n_intervals"),  # Triggers updates
    ],
)
def update_charts(gold, silver, silveroutlay, goldoutlay, ideal, silverdreamprice, golddreamprice, n_intervals):
    """adsfdsf"""
    goldvalue, silvervalue = get_melt_prices(silver, gold)
    print(goldvalue)
    # if goldvalue >=1:
    #     STATE = "ok"
    gold_dollar_value = goldvalue.get("values")
    silver_dollar_value = silvervalue.get("values")
    onces_to_sell_to_make_money = silveroutlay / silvervalue.get("meltprice")
    gold_onces_to_sell_to_make_money = goldoutlay / goldvalue.get("meltprice")
    total = gold_dollar_value + silver_dollar_value
    ratio = int(create_ratio(goldvalue.get("meltprice"), silvervalue.get("meltprice")))
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=ratio,
            title={"text": "Gold/Silver Ratio"},
            gauge={
                "axis": {"range": [0, ratio * 1.2]},
                "bar": {"color": "gold"},
                "steps": [
                    {"range": [0, 80], "color": "silver"},
                    {"range": [80, 100], "color": "gold"},
                ],
            },
        )
    )
    additional_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=onces_to_sell_to_make_money,
            title={"text": "Oz's of Silver to sell to break even"},
            gauge={
                "axis": {"range": [1, silver]},
                "bar": {"color": "silver"},
                "steps": [
                    {
                        "range": [0, onces_to_sell_to_make_money - silver],
                        "color": "red",
                    },
                    {"range": [silver, onces_to_sell_to_make_money], "color": "green"},
                ],
            },
        )
    )
    new_gauge_1 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gold_onces_to_sell_to_make_money,
            title={"text": "Oz's of Gold to sell to break even"},
            gauge={
                "axis": {"range": [0, gold_onces_to_sell_to_make_money * 1.2]},
                "bar": {"color": "blue"},
            },
        )
    )

    new_gauge_2 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=total,
            title={"text": "Total $ Gold and Silver holdings"},
            gauge={
                "axis": {"range": [0, (total + total * 0.25)]},
                "bar": {"color": "green"},
                # color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                "steps": [
                    #{"range": [0, 150000], "color": "orange"},
                    #{"range": [140001, 175000], "color": "green"},
                    {"range": [175001, 1000000], "color": "gold"},
                ],
            },
        )
    )

    gold_price_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=goldvalue.get("meltprice"),
            number={"valueformat": ".2f"},
            title={"text": "Gold Price/Oz ($)"},
            gauge={
                "axis": {"range": [0, goldvalue.get("meltprice") * 1.2]},
                "bar": {"color": "gold"},
            },
        )
    )
    silver_price_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=silvervalue.get("meltprice"),
            title={"text": "Silver Price/Oz ($)"},
            number={"valueformat": ".2f"},
            gauge={
                "axis": {"range": [0, silvervalue.get("meltprice") * 1.2]},
                "bar": {"color": "silver"},
            },
        )
    )
    required_gold_price_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=ideal / gold,
            number={"valueformat": ".2f"},
            title={"text": "Required Gold Price/Oz ($)"},
            gauge={
                "bar": {"color": "blue"},
                "axis": {"range": [0, (ideal / gold) * 1.2]},
                "steps": [
                    {"range": [0, 2000], "color": "blue"},
                    {"range": [2000, 2500], "color": "green"},
                    {"range": [2500, 3000], "color": "orange"},
                    {"range": [3000, (ideal / gold) * 1.2], "color": "green"},
                ],
            },
        )
    )
    required_silver_price_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=ideal / silver,
            title={"text": "Required Silver Price/Oz ($)"},
            number={"valueformat": ".2f"},
            gauge={
                "axis": {"range": [0, (ideal / silver) * 1.5]},
                "bar": {"color": "powderblue"},
                "steps": [
                    {"range": [0, 50], "color": "blue"},
                    {"range": [51, 100], "color": "green"},
                    {"range": [101, 3000], "color": "pink"},
                ],
            },
        )
    )
    silver_wish = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=silver * silverdreamprice,
            title={"text": "If Silver dream price is met"},
            #number={"valueformat": ".2f"},
            gauge={
                #"axis": {"range": [0, (silver * silverdreamprice) * 1.5]},
                "axis": {"range": [0, 3000000]},

                "bar": {"color": "silver"},
                # "steps": [
                #     {"range": [0, 1000001], "color": "red"},
                #     {"range": [1000001, 2000001], "color": "orange"},
                #     {"range": [2000001, 3000001], "color": "green"},
                # ],
            },
        )
    )
    gold_wish = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gold * golddreamprice,
            title={"text": "If Gold dream price is met"},
            gauge={
                #"axis": {"range": [0, (gold * golddreamprice) * 1.5]},
                "axis": {"range": [0, 3000000]},

                "bar": {"color": "gold"},
            },
        )
    )

    return (
        gauge,
        additional_gauge,
        new_gauge_1,
        new_gauge_2,
        gold_price_gauge,
        silver_price_gauge,
        required_gold_price_gauge,
        required_silver_price_gauge,
        silver_wish,
        gold_wish
    )


# Run the app
if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", debug=False, port=5000)
    #app.run_server(host="0.0.0.0", port=8080)$
    app.run(host="0.0.0.0", debug=False, port=5001)

