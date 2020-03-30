# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from data_load.usgs_data_load import USGS


external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'
]

external_javascript = [
    "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"  
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_javascript
)
app.title = "Groundwater Exploration Dashboard"

# Content for header div...
header_children = [
    html.H4(
        className = "title",
        children="Southern Puerto Rico Groundwater and Water Quality Dashboard"
    ),
    html.P(
        className = "description",
        children=[(
            "Dashboard application for exploring groundwater "
            "and water quality data from southern Puerto Rico"
        )]
    )        
]

filter_pane = [
    html.Div(
        className = "card-body",
        children = [
            html.P(
                "Filter by observation date (or select range in histogram):",
                className="control_label",
            ),
            dcc.RangeSlider(
                id="year_slider",
                min=1960,
                max=2017,
                value=[1990, 2010],
                className="dcc_control",
            ),
            html.P("Filter by observation type:", className="control_label"),
            # dcc.Dropdown(
            #     id="well_types",
            #     options=site_type_options,
            #     multi=True,
            #     # value=list(site_type_options.keys()),
            #     className="dcc_control",
            # ),
        ],
    )
]

graph_pane = [
    html.Div(
        id="countGraphContainer",
        className="card-body",        
        children = [
            dcc.Graph(id="count_graph")
        ],
    )
]

content_children = [
    html.Div(
        className = "filter_pane card col",
        children = filter_pane
    )
    ,
    html.Div(
        className = "graph_pane card col8",
        children = graph_pane
    )      
]

# Main app layout...
app.layout = html.Div(
    className = "container-fluid",
    children=[
        html.Div(
            className = "header row",
            children = header_children
        ),
        html.Div(
            className = "content row",
            children = content_children
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)