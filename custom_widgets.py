import ipywidgets as widgets
import pandas as pd
import seaborn as sns
from IPython.display import display
import folium
from folium.plugins import MarkerCluster
from folium import IFrame, Map, Popup, Icon, Marker, LayerControl

ALL = "All"


def resample_reindex_by_freq(df, freq="1M"):
    min_date = df.DateTimeStamp.min().date()
    max_date = df.DateTimeStamp.max().date()

    grouper_list = [
        pd.Grouper(key="StationCode"), pd.Grouper(
            key="DateTimeStamp", freq=freq)
    ]
    df = df.groupby(grouper_list).mean().sort_index()

    idx = pd.date_range(
        min_date, max_date, freq=freq, name="DateTimeStamp")
    mdx = pd.MultiIndex.from_product(
        [df.index.get_level_values(0).unique(), idx]
    )
    df = df.reindex(mdx)
    return df


# Filter by station_code...
def filter_by_station_code(df, station_code):
    if station_code == ALL:
        return df
    else:
        mask = (df["StationCode"] == station_code)
        df = df.loc[mask]
    return df


# Filter by validation_code...
def filter_by_validation_code(df, validation_code):
    if validation_code == ALL:
        return df
    elif validation_code == "Historical":
        mask = (df["Historical"] == "1")
    elif validation_code == "ProvisionalPlus":
        mask = (df["ProvisionalPlus"] == "1")
    return df.loc[mask]


# Filter by station_code...
def filter_by_nutrient_code(df, nutrient_code):
    if nutrient_code == ALL:
        return df
    else:
        df = df.loc[:, nutrient_code]
    return df


def filter_by_year_code(df, year_code):
    if year_code == ALL:
        return df
    else:
        mask = (df["DateTimeStamp"].dt.year == year_code)
        df = df.loc[mask]
    return df


def create_corr_matrix(df, method, *args, **kwargs):
    corr_df = df.corr(
        method,
        *args,
        **kwargs
    )
    return corr_df


class FilterWidgets:
    @classmethod
    def create_dropdown(cls, options_list, include_all=False, *args, **kwargs):
        options_list.sort()
        if include_all:
            options_list.insert(0, ALL)

        dropdown = widgets.Dropdown(
            options=options_list,
            *args,
            **kwargs
        )
        return dropdown

    @classmethod
    def create_validation_dropdown(cls, include_all=True):
        options = ["Historical", "ProvisionalPlus"]
        kwargs = dict(
            value=ALL,
            description="Validation:"
        )
        dropdown = cls.create_dropdown(options, include_all=True, **kwargs)
        return dropdown

    @classmethod
    def create_corr_dropdown(cls):
        corr_methods = ["pearson", "kendall", "spearman"]
        kwargs = dict(
            value="pearson",
            description="Correlation Method:"
        )
        dropdown = cls.create_dropdown(corr_methods, **kwargs)
        return dropdown

    # Station code dropdown
    @classmethod
    def create_stations_dropdown(cls, options, include_all=False):
        kwargs = dict(
            description="Station Code:"
        )
        dropdown = cls.create_dropdown(options, include_all, **kwargs)
        return dropdown

    @classmethod
    def create_freq_dropdown(cls):
        options = ["None", "1D", "1M", "1Y"]
        kwargs = dict(
            value="None",
            description="Frequency:"
        )
        dropdown = cls.create_dropdown(options, **kwargs)
        return dropdown

    @classmethod
    def create_nutrients_dropdown(cls):
        options = ["PO4F", "NH4F", "NO2F", "NO3F", "NO23F", "CHLA_N"]
        kwargs = dict(
            value="PO4F",
            description="Nutrients:"
        )
        dropdown = cls.create_dropdown(options, **kwargs)
        return dropdown

    @classmethod
    def create_param_dropdown(cls, options, include_all=False):
        kwargs = dict(
            description="Parameter:"
        )
        dropdown = cls.create_dropdown(options, include_all, **kwargs)
        return dropdown

    @classmethod
    def create_year_dropdown(cls, options, include_all=False):
        kwargs = dict(
            description="Year:"
        )
        dropdown = cls.create_dropdown(options, include_all, **kwargs)
        return dropdown

class PairplotWidgets(FilterWidgets):
    # Accepts args and kwargs for sns.heatmap
    @classmethod
    def create_pairplot(cls, df, *args, **kwargs):
        ax = sns.pairplot(
            df,
            *args,
            **kwargs
        )
        return ax

    # Given a df, returns correlation df and heatmap ax
    @classmethod
    def create_dist_pairplot(cls, df):
        var_cols = df.select_dtypes("float").columns.tolist()
        pairplot_options = dict(
            vars=var_cols,
            hue="StationCode"
        )
        ax = cls.create_pairplot(df, **pairplot_options)
        return ax

    @classmethod
    def display_distribution_widget(cls, df, include_all=False):
        options = df.StationCode.unique().tolist()
        stations_dropdown = cls.create_stations_dropdown(options, include_all)

        validation_dropdown = cls.create_validation_dropdown()

        def on_dropdown_update(df, station_code, validation_code):
            df = filter_by_station_code(df, station_code)
            df = filter_by_validation_code(df, validation_code)

            if not df.empty:
                msg = f"Generating pairplot for {station_code}: {validation_code}"
                display(widgets.HTML(msg))
                cls.create_dist_pairplot(df)
            else:
                msg = "No data was found with the selected filters."
                msg += "Unable to generate report."
                display(widgets.HTML(msg))

        widgets.interact(
            on_dropdown_update,
            df=widgets.fixed(df),
            station_code=stations_dropdown,
            validation_code=validation_dropdown
        )


class LineplotWidgets(FilterWidgets):
    # Accepts args and kwargs for sns.heatmap
    @classmethod
    def create_lineplot(cls, df, *args, **kwargs):
        ax = sns.lineplot(
            data=df,
            *args,
            **kwargs
        )
        return ax

    # @classmethod
    # def create_param_lineplot(cls, df, nutrient_code):
    #     lineplot_options = dict(
    #         x="DateTimeStamp",
    #         y=var_cols,
    #         hue="StationCode"
    #     )
    #     ax = cls.create_lineplot(df, **lineplot_options)
    #     return ax

    @classmethod
    def display_lineplot_widget(cls, df, include_all=False):
        options = df.StationCode.unique().tolist()
        stations_dropdown = cls.create_stations_dropdown(options, include_all)

        validation_dropdown = cls.create_validation_dropdown()
        options = df.select_dtypes("float").columns.tolist()
        param_dropdown = cls.create_param_dropdown(options)
        options = df.DateTimeStamp.dt.year.unique().tolist()
        year_dropdown = cls.create_year_dropdown(options)

        def on_dropdown_update(df, station_code, validation_code, param_code, year_code):
            df = filter_by_station_code(df, station_code)
            df = filter_by_year_code(df, year_code)
            df = filter_by_validation_code(df, validation_code)

            if not df.empty:
                msg = f"Generating lineplot for {station_code}: {validation_code}"
                display(widgets.HTML(msg))
                lineplot_options = dict(
                    x="DateTimeStamp",
                    y=param_code,
                    hue="StationCode",
                    ci=None
                )
                cls.create_lineplot(df, **lineplot_options)
            else:
                msg = "No data was found with the selected filters."
                msg += "Unable to generate report."
                display(widgets.HTML(msg))

        widgets.interact(
            on_dropdown_update,
            df=widgets.fixed(df),
            station_code=stations_dropdown,
            validation_code=validation_dropdown,
            param_code=param_dropdown,
            year_code=year_dropdown
        )


class HeatmapWidgets(FilterWidgets):
    # Accepts args and kwargs for sns.heatmap
    @classmethod
    def create_heatmap(cls, df, *args, **kwargs):
        ax = sns.heatmap(
            data=df,
            *args,
            **kwargs
        )
        return ax

    @classmethod
    def create_missing_val_heatmap(cls, df):
        kwargs = dict(
            cbar=True,
            cmap="Greys"
        )
        ax = cls.create_heatmap(df, **kwargs)
        return ax

    # Given a df, returns correlation df and heatmap ax
    @classmethod
    def create_corr_heatmap(cls, df, method="pearson"):
        corr_df = create_corr_matrix(df, method, min_periods=1)

        heatmap_options = dict(
            annot=True,
            fmt='.1g',
            vmin=-1,
            vmax=1,
            center=0,
            cmap='RdBu',
            square=True
        )
        ax = cls.create_heatmap(corr_df, **heatmap_options)
        return (corr_df, ax)

    @classmethod
    def display_missing_val_widget(cls, df, include_all=False):
        options = df.StationCode.unique().tolist()
        stations_dropdown = cls.create_stations_dropdown(options, include_all)

        validation_dropdown = cls.create_validation_dropdown()
        frequency_dropdown = cls.create_freq_dropdown()

        def on_dropdown_update(
            df,
            station_code,
            validation_code,
            frequency_code
        ):
            df = filter_by_station_code(df, station_code)
            df = filter_by_validation_code(df, validation_code)

            if not df.empty:
                msg = f"Generating missing values heatmap for {station_code}: {validation_code}"
                if frequency_code != "None":
                    df = resample_reindex_by_freq(df, frequency_code)
                else:
                    df = df.set_index(["StationCode", "DateTimeStamp"])

                display(widgets.HTML(msg))
                start_date = df.index.get_level_values(1).min()
                end_date = df.index.get_level_values(1).max()
                msg = f"Earliest Date: {start_date}.  Latest Date: {end_date}"
                display(widgets.HTML(msg))
                cls.create_missing_val_heatmap(
                    df.notnull()
                )
            else:
                msg = "No data was found with the selected filters."
                msg += "Unable to generate report."
                display(widgets.HTML(msg))

        widgets.interact(
            on_dropdown_update,
            df=widgets.fixed(df),
            station_code=stations_dropdown,
            validation_code=validation_dropdown,
            frequency_code=frequency_dropdown
        )

    @classmethod
    def display_correlation_widget(cls, df, include_all=False):
        options = df.StationCode.unique().tolist()
        stations_dropdown = cls.create_stations_dropdown(options, include_all)

        corr_method_dropdown = cls.create_corr_dropdown()
        validation_dropdown = cls.create_validation_dropdown()

        def on_dropdown_update(df, station_code, validation_code, corr_method):
            df = filter_by_station_code(df, station_code)
            df = filter_by_validation_code(df, validation_code)

            if not df.empty:
                msg = f"Generating {corr_method} correlation plot for {station_code}: {validation_code}"
                display(widgets.HTML(msg))
                cls.create_corr_heatmap(df, method=corr_method)
            else:
                msg = "No data was found with the selected filters."
                msg += "Unable to generate report."
                display(widgets.HTML(msg))

        widgets.interact(
            on_dropdown_update,
            df=widgets.fixed(df),
            station_code=stations_dropdown,
            validation_code=validation_dropdown,
            corr_method=corr_method_dropdown
        )


POPUP_TEMPLATE = """
  <!DOCTYPE html>
  <html>
  <head>
  <style>
  table {{
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
  }}

  td, th {{
    border: 1px solid #dddddd;
    text-align: left;
    padding: 4px;
  }}

  </style>
  </head>
  <body>
  <table>
    <tr>
      <td><strong>Station Name</strong></td>
      <td>{}</td>
    </tr>
    <tr>
      <td><strong>Station Code</strong></td>
      <td>{}</td>
    </tr>
    <tr>
      <td><strong>Station Type</strong></td>
      <td>{}</td>
    </tr>
    <tr>
      <td><strong>Status</strong></td>
      <td>{}</td>
    </tr>
    <tr>
      <td><strong>Reserve Name</strong></td>
      <td>{}</td>
    </tr>
    <tr>
      <td><strong>Active Dates</strong></td>
      <td>{}</td>
    </tr>
  </table>

  </body>
  </html>
""".format

class StudyMap():
    PR_CENTER = [17.95524, -66.2200]

    @staticmethod
    def create_map(center=PR_CENTER, zoom=13, *args, **kwargs):
        m1 = Map(
            location=center,
            zoom_start=zoom,
            *args,
            **kwargs
        )
        return m1

    # Based on the popup html...
    @staticmethod
    def create_popups_from_template(
        location,
        html_template=POPUP_TEMPLATE,
        *args,
        **kwargs
    ):
        iframe = IFrame(
            html=html_template(*args, **kwargs),
            width=400,
            height=200
        )
        popup = Popup(
            iframe,
            max_width=500
        )
        return popup

    # Appends markers to map based on df
    # and return map
    @staticmethod
    def create_stations_map(df):
        m1 = StudyMap.create_map()

        for station_type in df.StationType.unique().tolist():
            mask = (df["StationType"] == station_type)
            df2 = df.loc[mask]

            # markers that will be added to the cluster...
#             marker_cluster = MarkerCluster(name=station_type).add_to(m1)
            for idx, row in df2.iterrows():
                location = [row.geometry.y, row.geometry.x]
                popup = StudyMap.create_popups_from_template(
                    location,
                    POPUP_TEMPLATE,
                    row.StationName,
                    row.StationCode,
                    row.StationType,
                    row.Status,
                    row.ReserveName,
                    row.ActiveDates,
                    row.StationType
                )

                # Give color to marker based on station_type
                def get_color(station_type):
                    switcher = {
                        "Meteorological": "blue",
                        "Nutrients": "green",
                        "Water Quality": "red",
                    }

                    color = switcher.get(station_type, "gray")
                    return color

#                 icon_name = "check-circle" if row.Status == "Active" else "times-circle"
                icon_name = "glyphicon-ok" if row.Status == "Active" else "glyphicon-remove"

                icon = Icon(
                    icon=icon_name,
                    color=get_color(row.StationType),
                    icon_color='white'
                )

                Marker(
                    location=location,
                    popup=popup,
                    tooltip=f"{row.StationType} - {row.StationCode}",
                    icon=icon,
                    draggable=False
                ).add_to(m1)

        # Create the layer control and add to map
        control = LayerControl(position='topright')
        control.add_to(m1)
        return m1
