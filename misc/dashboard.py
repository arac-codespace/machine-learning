import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

from studydata import StudyData
import pdb

from collections import namedtuple

PlotData = namedtuple(
    'PlotData',
    [
        'df',
        'title'
    ]
)

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


class DashboardData:
    def __init__(
        self,
        date_start='1/1/2008',
        date_end='1/1/2020'
    ):
        self.date_start = date_start
        self.date_end = date_end
        self.well_rain_sites = None
        self.well_data = None
        self.rain_data = None
        self.aquifers = None
        self.hydrologic_basin = None

        self.well_site_options = None
        self.rain_site_options = None
        self.well_date_options = None
        self.rain_date_options = None
        self._id_to_name = None

        # Fetch data an load into class
        self._load_data()
        # Use loaded data to create
        # data constants...
        self._set_constants()

    def _load_data(self):
        date_start = self.date_start
        date_end = self.date_end

        # fetch study data
        sd = StudyData()

        def filter_by_date(df, date_start, date_end):
            mask = (df["date_time"] >= date_start) & (df["date_time"] <= date_end)
            df = df.loc[mask]
            return df

        usgs_well = sd.get_usgs_historical_well_data()
        usgs_well = filter_by_date(usgs_well, date_start, date_end)

        usgs_rain = sd.get_usgs_historical_rain_data()
        usgs_rain = filter_by_date(usgs_rain, date_start, date_end)

        usgs_well_rain_sites = sd.get_usgs_historical_well_rain_sites(
            as_gdf=False
        )

        self.well_data = usgs_well
        self.rain_data = usgs_rain
        self.well_rain_sites = usgs_well_rain_sites
        self.aquifers = sd.get_aquifers_df()
        self.hydrologic_basin = sd.get_hydrologic_basin_df()

    def _set_constants(self):
        well_rain_sites = self.well_rain_sites
        well_data = self.well_data
        rain_data = self.rain_data

        well_site_options = self._set_site_options(
            well_rain_sites, "Groundwater")
        rain_site_options = self._set_site_options(
            well_rain_sites, "Meteorological")

        well_date_options = self._set_date_options(well_data)
        rain_date_options = self._set_date_options(rain_data)

        self.well_site_options = well_site_options
        self.rain_site_options = rain_site_options
        self.well_date_options = well_date_options
        self.rain_date_options = rain_date_options
        self._id_to_name = self._set_id_to_name()

    def _set_site_options(self, df, site_type):
        # Get the site id to name dict mapping
        def site_to_name_mapping(df):
            site_ids = df.site_id.unique()
            mask = (df["site_id"].isin(site_ids), ["site_id", "site_name"])
            sites_to_name = df.loc[mask].sort_values("site_name")

            sites_to_name = sites_to_name.set_index(
                ["site_id"]).to_dict()["site_name"]
            return sites_to_name

        mask = (df["site_type"] == site_type)
        df = df.loc[mask]
        sites_to_name = site_to_name_mapping(df)

        # Define site options
        sites_options = [
            {
                "value": key,
                "label": val
            } for key, val in (sites_to_name).items()
        ]

        return sites_options

    def _set_date_options(self, df):
        # define year options
        all_years = list(
            df.date_time.dt.year.unique().tolist()
        )
        all_years.sort()
        years_options = [
            {
                "value": year,
                "label": str(year)
            } for i, year in enumerate(all_years)
        ]
        return years_options

    def _set_id_to_name(self):
        well_options = self.well_site_options
        rain_options = self.rain_site_options
        all_options = well_options + rain_options
        id_to_name = {}
        for row in all_options:
            id_to_name[row.get("value")] = row.get("label")

        return id_to_name

    # create pivot table by datetime and siteid where
    # var_name is the name of the measurement ie:
    # rain, water level, etc...
    # Reindex the timeseries to make sure that
    # every time freq is represented by a row...
    @staticmethod
    def pivot_reindex_df(df, var_name, reindex_range):
        pivot_df = pd.pivot_table(
            df,
            values=var_name,
            index=["date_time"],
            columns="site_id",
            aggfunc="mean"
        )

        pivot_df = pivot_df.reindex(reindex_range)
        return pivot_df

    # With a reindex pivot table, find the missing
    # values and calculate the percent missing.
    # Note that this uses the mean operation, so
    # it's important for the table to have a
    # representing row for every time frequency...

    def calculate_percent_missing(
        self,
        df,
        var_name,
        reindex_freq="1H",
        summary_freq="1M"
    ):
        date_start = self.date_start
        date_end = self.date_end
        reindex_range = pd.date_range(
            date_start,
            date_end,
            freq=reindex_freq,
            name="date_time"
        )
        pivot_df = self.pivot_reindex_df(df, var_name, reindex_range)

        def _calculate_percent_missing(pivot_df, freq):
            missing_well = pivot_df.isna().sort_index()

            grouper_list = [
                pd.Grouper(level=0, freq=freq)
            ]

            percent_missing = missing_well.groupby(grouper_list).mean()*100
            percent_missing = percent_missing.unstack().reset_index().rename(
                {0: "percent_missing"}, axis=1)
            return percent_missing

        percent_missing = _calculate_percent_missing(pivot_df, summary_freq)
        return percent_missing

    def get_well_rain_sites(self):
        return self.well_rain_sites.copy()

    def get_rain_data(self):
        return self.rain_data.copy()

    def get_well_data(self):
        return self.well_data.copy()

    def get_aquifers(self):
        return self.aquifers.copy()

    def get_hydrologic_basin(self):
        return self.hydrologic_basin.copy()

    def convert_id_to_name(self, site_id):
        id_to_name = self._id_to_name

        return id_to_name.get(site_id, "Unknown")

def resample_df(df, freq, agg_functions):
    # resample usgs to hourly
    grouper_list = [
        pd.Grouper(level="site_id"),
        pd.Grouper(level="date_time", freq=freq)
    ]
    df = df.set_index(["site_id", "date_time"]).sort_index()
    df = df.groupby(grouper_list).agg(agg_functions)
    df = df.reset_index()
    return df

dd = DashboardData()
well_data = dd.get_well_data()
rain_data = dd.get_rain_data()
aquifers = dd.get_aquifers()
hydrologic_basin = dd.get_hydrologic_basin()

# Hourly freq is too much for plotly to display...
# Resampling to help with displaying all this data...
agg_functions = dict(
    water_level="mean",
    quality_flag="first"
)
resampled_well_data = resample_df(well_data, "1D", agg_functions)

agg_functions = dict(
    precipitation="mean",
    quality_flag="first"
)
resampled_rain_data = resample_df(rain_data, "1D", agg_functions)

# Define site options
well_site_options = dd.well_site_options
all_well_sites = [row.get("value") for row in well_site_options]
first_well_site = all_well_sites[0]

# Define site options
rain_site_options = dd.rain_site_options
all_rain_sites = [row.get("value") for row in rain_site_options]
first_rain_site = all_rain_sites[0]

# define year options
year_options = dd.well_date_options
all_years = [row.get("value") for row in year_options]
latest_year = all_years[-1]

# Create map function
# def create_map(df, locations, z):
#     # pdb.set_trace()
#     print(df.columns)


#     fig = go.Figure(
#         go.Scattermapbox(
#             lat=df.latitude,
#             lon=df.longitude,
#             text=df.aq_name,
#             hoverinfo='text'
#         )
#     )
#     # fig = go.Figure(
#     #     go.Choroplethmapbox(
#     #         geojson=df.to_json(),
#     #         locations=df[locations],
#     #         z=df["shape_area"],
#     #         colorscale="Viridis",
#     #         # zmin=0,
#     #         # zmax=12,
#     #         marker_opacity=0.5,
#     #         marker_line_width=0
#     #     )
#     # )
#     fig.update_layout(
#         mapbox_style="open-street-map",
#         mapbox_zoom=3,
#         # mapbox_center={
#         #     "lat": 37.0902,
#         #     "lon": -95.7129
#         # }
#     )
#     fig.update_layout(
#         margin={
#             "r": 0,
#             "t": 0,
#             "l": 0,
#             "b": 0
#         }
#     )
#     return fig

# list of dfs
def create_missing_plot(plots_data):

    plots_data = list(plots_data)
    fig = make_subplots()
    row_num = len(plots_data)
    col_num = 1

    fig = make_subplots(
        rows=row_num,
        cols=col_num,
        shared_xaxes=True,
        shared_yaxes=False,
        vertical_spacing=0.05,
        subplot_titles=[dataset.title for dataset in plots_data]
    )

    i=1
    for dataset in plots_data:
        filtered_df = dataset.df
        trace = go.Heatmap(
            z=filtered_df.percent_missing,
            x=filtered_df.date_time,
            y=filtered_df.site_id,
            colorscale='Electric_r'
        )
        fig.add_trace(
            trace,
            row=i,
            col=1,
        )
        i+=1

    fig.update_layout(
        title="Percent Missing Values per Month - Hourly Timestep",
        xaxis_nticks=12,
        height=1000,
        yaxis={
            "type": "category",
            "fixedrange": True
        },
        yaxis2={
            "type": "category",
            "fixedrange": True
        }
    )
    return fig


def create_missing_table(df, title):
    fig = go.Figure()
    headers = df.percent_missing.reset_index().columns
    values = list(df.percent_missing.reset_index().to_dict("list").values())

    trace = go.Table(
        header=dict(
            values=list(headers),
            # fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=list(values),
            # fill_color='lavender',
            align='left',
            height=20,
        )
    )
    fig.add_trace(trace)

    fig.update_layout(
        title=title,
        # autosize=False,
        # width=500,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=1
        ),
    )

    return fig

@app.callback(
    Output("map", "figure"),[
        Input("frequency_selector", "value")
    ]
)
def update_map(placeholder):
    df = aquifers
    # fig = go.Figure(
    #     go.Scattermapbox(
    #         lat=df.latitude,
    #         lon=df.longitude,
    #         text=df.aq_name,
    #         hoverinfo='text'
    #     )
    # )
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=df.to_json(),
            locations=df["aq_name"].tolist(),
            z=df["shape_area"].tolist(),
            colorscale="Viridis",
            # zmin=0,
            # zmax=12,
            # marker_opacity=0.5,
            # marker_line_width=0
        )
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=3,
        # mapbox_center={
        #     "lat": 37.0902,
        #     "lon": -95.7129
        # }
    )
    # fig.update_layout(
    #     margin={
    #         "r": 0,
    #         "t": 0,
    #         "l": 0,
    #         "b": 0
    #     }
    # )

    return fig


@app.callback(
    Output("all_water_level_graph", "figure"), [
        Input("year_selector", "value")
    ]
)
def update_all_water_level_plot(selected_year):
    df = resampled_well_data
    selected_siteid = all_well_sites
    fig = go.Figure()

    row_num = 2
    col_num = 1

    fig = make_subplots(
        rows=row_num,
        cols=col_num,
        shared_xaxes=True,
        shared_yaxes=False,
        vertical_spacing=0.05,
        subplot_titles=[
            "Precipitation",
            "Water Level"
        ],
        row_heights=[0.5, 2]
    )

    for site_id in selected_siteid:
        mask = (
            (
                df["site_id"] == site_id
            ) & (
                df["date_time"].dt.year == selected_year
            )
        )
        filtered_df = df.loc[mask]
        if not filtered_df.empty:
            trace = go.Scattergl(
                x=filtered_df.date_time,
                y=filtered_df.water_level,
                name=site_id
            )
            fig.add_trace(
                trace,
                row=2,
                col=1
            )

    df = resampled_rain_data
    selected_siteid = all_rain_sites

    for site_id in selected_siteid:
        mask = (
            (
                df["site_id"] == site_id
            ) & (
                df["date_time"].dt.year == selected_year
            )
        )
        filtered_df = df.loc[mask]
        if not filtered_df.empty:
            trace = go.Bar(
                x=filtered_df.date_time,
                y=filtered_df.precipitation,
                name=site_id
            )
            fig.add_trace(
                trace,
                row=1,
                col=1
            )

    fig.update_layout(
        # title="Precipitation Timeseries",
        height=800,
        barmode="stack",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
    )

    return fig

# @app.callback(
#     Output("all_rain_graph", "figure"), [
#         Input("year_selector", "value")
#     ]
# )
# def update_all_rain_plot(selected_year):
#     df = resampled_rain_data
#     selected_siteid = all_rain_sites
#     fig = go.Figure()

#     for site_id in selected_siteid:
#         mask = (
#             (
#                 df["site_id"] == site_id
#             ) & (
#                 df["date_time"].dt.year == selected_year
#             )
#         )
#         filtered_df = df.loc[mask]
#         trace = go.Bar(
#             x=filtered_df.date_time,
#             y=filtered_df.precipitation,
#             name=site_id
#         )
#         fig.add_trace(trace)

#     fig.update_layout(
#         title="Precipitation Timeseries",
#         # barmode="group"
#     )

#     return fig

@app.callback(
    Output("missing_values_graph", "figure"), [
        Input("frequency_selector", "value")
    ]
)
def update_missing_plot(freq_selection):
    if not freq_selection:
        freq_selection = "1M"

    well_missing_values = dd.calculate_percent_missing(
        well_data,
        "water_level",
        reindex_freq="1H",
        summary_freq=freq_selection
    )

    rain_missing_values = dd.calculate_percent_missing(
        rain_data,
        "precipitation",
        reindex_freq="1H",
        summary_freq=freq_selection
    )

    df1 = well_missing_values
    df2 = rain_missing_values

    plots_data = []
    title = "Water Level Data"
    data = PlotData(df1, title)
    plots_data.append(data)

    title = "Precipitation Data"
    data = PlotData(df2, title)
    plots_data.append(data)

    fig = create_missing_plot(plots_data)
    return fig

@app.callback(
    Output("missing_values_well_table", "figure"), [
        Input("frequency_selector", "value"),
        Input("visibility_checkbox", "value")
    ]
)
def update_missing_table_well(freq_selection, visibility):
    if not visibility:
        return go.Figure()

    if not freq_selection:
        freq_selection = "1M"

    df = dd.calculate_percent_missing(
        well_data,
        "water_level",
        reindex_freq="1H",
        summary_freq=freq_selection
    )
    df_pivot = pd.pivot_table(
        df,
        index=df["date_time"],
        columns=df["site_id"],
        values=["percent_missing"],
        aggfunc="first"
    )

    df_pivot.index = df_pivot.index.strftime("%Y %B")
    title = "Water Level Missing Values"
    fig = create_missing_table(df_pivot, title)
    return fig

@app.callback(
    Output("missing_values_rain_table", "figure"), [
        Input("frequency_selector", "value"),
        Input("visibility_checkbox", "value")
    ]
)
def update_missing_table_rain(freq_selection, visibility):
    if not visibility:
        return go.Figure()

    if not freq_selection:
        freq_selection = "1M"

    df = dd.calculate_percent_missing(
        rain_data,
        "precipitation",
        reindex_freq="1H",
        summary_freq=freq_selection
    )
    df_pivot = pd.pivot_table(
        df,
        index=df["date_time"],
        columns=df["site_id"],
        values=["percent_missing"],
        aggfunc="first"
    )

    df_pivot.index = df_pivot.index.strftime("%Y %B")
    title = "Precipitation Missing Values"
    fig = create_missing_table(df_pivot, title)
    return fig

@app.callback(
    [Output("missing_values_well_table", "style"),
     Output("missing_values_rain_table", "style")],
    [Input("visibility_checkbox", "value")]
)
def update_visibility_table_data(visibility):
    if visibility:
        return [{"display": "block"}]*2
    else:
        return [{"display": "none"}]*2

# @app.callback(
#     Output("missing_values_rain_table", "style"), [
#         Input("visibility_checkbox", "value"),
#     ]
# )
# def update_visibility_table_rain(visibility):
#     if visibility:
#         return {"display": "block"}
#     else:
#         return {"display": "none"}


frequency_options = [
    {
        "value": "1M", "label": "Month"
    },
    {
        "value": "1Y", "label": "Year"
    }
]


frequency_selection = html.Div(
    children=[
        dcc.Dropdown(
            id="frequency_selector",
            options=frequency_options,
            value="1M",
            multi=False,
            searchable=False,
            clearable=False
        ),
    ]
)

year_selection = html.Div(
    children=[
        dcc.Dropdown(
            id="year_selector",
            options=year_options,
            value=latest_year,
            multi=False,
            searchable=False,
            clearable=False
        ),
    ]
)

visibility_checkbox = html.Div(
    children=[
        dcc.RadioItems(
            id="visibility_checkbox",
            options=[
                {'label': 'Show Content', 'value': 1},
                {'label': 'Hide Content', 'value': 0}
            ],
            value=0
        )
    ]
)


general_tab_content = html.Div(
    children=[
        dcc.Graph(id="all_water_level_graph"),
        dcc.Graph(id="map")
    ]
)

missing_values_content = html.Div(
    children=[
        dcc.Graph(id="missing_values_graph"),
        dcc.Graph(id="missing_values_well_table"),
        dcc.Graph(id="missing_values_rain_table")
    ]
)

general_tab = dcc.Tab(
    label='General',
    children=[
        dbc.Row(
            [
                dbc.Col([
                    html.H6("Frequency"),
                    year_selection
                    ], width=1),
                dbc.Col(general_tab_content),
            ]
        )
    ]
)

missing_values_tab = dcc.Tab(
    label='Missing Values',
    children=[
        dbc.Row(
            [
                dbc.Col([
                    html.H6("Frequency"),
                    frequency_selection,
                    html.H6("Raw Data"),
                    visibility_checkbox
                ], width=1),
                dbc.Col(missing_values_content)
            ]
        )
    ]
)



if __name__ == '__main__':

    app.layout = html.Div(
        children=[
            dcc.Tabs(
                [
                    general_tab,
                    missing_values_tab
                ]
            )
        ]
    )

    app.run_server(debug=True)
