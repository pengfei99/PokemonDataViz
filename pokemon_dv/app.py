import os

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import sqlalchemy as sa
from dash import dcc
from dash import html
from dash.dependencies import Output, Input


def run_query(query: str, db_connection):
    rs = db_connection.execute(query)
    columns = None
    for row in rs:
        if columns is None:
            columns = row.keys()
        print(dict(zip(columns, row)))


def get_dataframe(table_name: str):
    db_login = os.getenv("DB_LOGIN")
    db_pwd = os.getenv("DB_PWD")
    db_url = os.getenv("DB_URL")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_location = f"{db_url}:{db_port}/{db_name}"
    engine = sa.create_engine(f'postgresql://{db_login}:{db_pwd}@{db_location}')
    df = None
    try:
        db_connection = engine.connect()
        df = pd.read_sql(f"select * from {table_name}", db_connection)
    except Exception as e:
        pass
    if df is None:
        df = default_df()
    return df


def default_df():
    lst = [[1, "Bulbasaur", "Grass", "Poison", 318, 45, 49, 49, 65, 65, 45, 1, False, 318, 159, 159, 420],
           [2, "Ivysaur", "Grass", "Poison", 405, 60, 62, 63, 80, 80, 60, 1, False, 405, 202, 203, 536],
           [3, "Venusaur", "Grass", "Poison", 525, 80, 82, 83, 100, 100, 80, 1, False, 525, 262, 263, 696],
           [3, "VenusaurMega Venusaur", "Grass", "Poison", 625, 80, 100, 123, 122, 120, 80, 1, False, 625, 302, 323,
            816],
           [4, "Charmander", "Fire", "", 309, 39, 52, 43, 60, 50, 65, 1, False, 309, 177, 132, 430]
           ]
    df = pd.DataFrame(lst, columns=["index", "name", "type_1", "type_2", "total", "hp", "attack", "defense",
                                    "special_attack",
                                    "special_defense", "speed", "generation", "legendary", "base_stats", "off_stats",
                                    "def_stats",
                                    "overall_score"])
    return df


# templates used in graphs
graph_template = "plotly_dark"

# layout_style = {'background-color':'#FF9F1C','font-size':15}
layout_style = {"background-color": "#D75C37"}

# ------------------------------------------------------------------------------
# app
# good themes - SLATE,BOOTSTRAP, DARKLY, CYBORG
app = dash.Dash(
    "DashPokemon",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SLATE],
)
app.title = "Pokemon Analytics: Understand Your Pokemons!"

app_name = "Dash Pokemon"

server = app.server

db_table_name = os.getenv("DB_TABLE_NAME")
# --------------------------------------------------------------------------------------------
# app controls

app.layout = html.Div(
    children=[
        # 1st html div for showing the site header
        html.Div(
            children=[
                # add a new component which is the logo
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Pokemon Analytics",
                    # use a css class to customize the style of this header h1
                    className="header-title"
                ),
                html.P(
                    children="Get the best pokemon by their type",
                    # use a css class to customize the style of this paragraph
                    className="header-description",
                ),
            ],
            # use a css class to customize the style of this header div
            className="header",
        ),
        # 2nd div for the data filtering menu
        html.Div(

            children=[
                html.Div(
                    children=[
                        html.Div(children="Pokemon Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": type1, "value": type1}
                                for type1 in np.sort(get_dataframe(db_table_name).type_1.unique())
                            ],
                            value="Bug",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Criteria", className="menu-title"),
                        dcc.Dropdown(
                            id="criteria-filter",
                            options=[
                                {"label": criteria, "value": criteria}
                                for criteria in [
                                    "overall_score",
                                    "hp",
                                    "attack",
                                    "defense",
                                    "special_attack",
                                    "special_defense",
                                    "speed",
                                ]
                            ],
                            value="overall_score",
                            clearable=False,
                            className="dropdown",
                        ),

                    ],
                ),
            ],
            className="menu",
        ),

        # 3rd div for the two graphs
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="generation-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="legendary-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    #  define the inputs and outputs of the callback
    [Output("generation-chart", "figure"), Output("legendary-chart", "figure")],
    [
        Input("type-filter", "value"),
        Input("criteria-filter", "value"),

    ],
)
def update_charts(type1, criteria):

    df = get_dataframe(db_table_name)
    filtered_df = df[df["type_1"] == type1]
    best_pokemon = filtered_df.loc[filtered_df[criteria].idxmax()].name
    print(filtered_df.head())
    print(best_pokemon)
    generation_chart_figure = px.bar(
        filtered_df,
        y="name",
        x=criteria,
        color="generation",
        template=graph_template,
        height=600,
    )
    generation_chart_figure.update_traces(textfont_size=20)
    generation_chart_figure.update_layout(
        title="Six Generations of pokemons",
        uniformtext_minsize=15,
        transition_duration=500,
    )

    legendary_chart_figure = px.bar(
        filtered_df,
        y="name",
        x=criteria,
        color="legendary",
        template=graph_template,
        height=600,
    )
    legendary_chart_figure.update_traces(textfont_size=20)

    legendary_chart_figure.update_layout(
        title="Legendary/Non-legendary pokemons ",
        uniformtext_minsize=15,
        uniformtext_mode="hide",
        transition_duration=500,
    )

    return generation_chart_figure, legendary_chart_figure


if __name__ == "__main__":
    app.run_server(host="0.0.0.0",debug=False, threaded=True, port=8888)
