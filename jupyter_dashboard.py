import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import IFrame


MAP_POPUP = """
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
    def create_map(location=PR_CENTER, zoom_start=13, *args, **kwargs):
        follium_map = folium.Map(
            location=location,
            zoom_start=zoom_start,
            *args,
            **kwargs
        )
        return follium_map

    # Based on the popup html...
    @staticmethod
    def create_popups_from_template(html_template, *args, **kwargs):
        width, height = 300, 150
        popup = folium.Popup(
            IFrame(
                MAP_POPUP(*args, **kwargs),
                width=width,
                height=height
            )
        )
        return popup

    # Appends markers to map based on df
    # and return map
    @staticmethod
    def create_stations_map(df):
        follium_map = StudyMap.create_map()

        for station_type in df.StationType.unique().tolist():
            marker_cluster = MarkerCluster(
                name=station_type).add_to(follium_map)
            mask = (df["StationType"] == station_type)
            df2 = df.loc[mask]
            for idx, row in df2.iterrows():
                popup = StudyMap.create_popups_from_template(
                    MAP_POPUP,
                    row.StationName,
                    row.StationCode,
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

                icon = "ok-sign" if row.Status == "Active" else "remove-sign"
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    popup=popup,
                    tooltip=f"{row.StationType} - {row.StationCode}",
                    icon=folium.Icon(color=get_color(row.StationType), icon=icon),
                ).add_to(marker_cluster)

        follium_map.add_child(folium.LayerControl())
        return follium_map
