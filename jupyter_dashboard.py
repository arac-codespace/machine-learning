import pandas as pd
import ipywidgets as widgets
from custom_widgets import FilterWidgets, HeatmapWidgets, LineplotWidgets, PairplotWidgets, StudyMap
from custom_widgets import filter_by_station_code, filter_by_validation_code
from IPython.display import display

class WidgetDashboard(HeatmapWidgets, LineplotWidgets, PairplotWidgets):
    # https://towardsdatascience.com/interactive-controls-for-jupyter-notebooks-f5c94829aee6
    # https://python-forum.io/Thread-Visualisation-of-gaps-in-time-series-data

    @classmethod
    def display_summary_widget(cls, df, locations_df, include_all=False):
        options = df.StationCode.unique().tolist()
        stations_dropdown = cls.create_stations_dropdown(options, include_all)
        validation_dropdown = cls.create_validation_dropdown()

        def on_dropdown_update(df, locations_df, station_code, validation_code):
            # Filter by validation code
            df = filter_by_station_code(df, station_code)
            # Filter by station code
            df = filter_by_validation_code(df, validation_code)

            # Filter locations_df by station code
            filtered_stations = df.StationCode.unique().tolist()
            mask = (locations_df["StationCode"].isin(filtered_stations))
            locations_df = locations_df.loc[mask]
            study_map = StudyMap.create_stations_map(locations_df)

            display(study_map)
            if not df.empty:
                msg = f"Summary for {station_code}: {validation_code}"
                display(widgets.HTML(msg))
                display(df.groupby("StationCode").describe().stack())
            else:
                msg = "No data was found with the selected filters. {station_code}: {validation_code}"
                msg += "Unable to generate report."
                display(widgets.HTML(msg))

        widgets.interact(
            on_dropdown_update,
            df=widgets.fixed(df),
            locations_df=widgets.fixed(locations_df),
            station_code=stations_dropdown,
            validation_code=validation_dropdown
        )
