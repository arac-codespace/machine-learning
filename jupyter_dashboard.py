import pandas as pd
from ipywidgets import HTML
from ipyleaflet import (
    Map,
    Marker,
    MarkerCluster,
    LayersControl,
    Popup,
    AwesomeIcon  
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
            center=center,
            zoom=zoom,
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
        popup = Popup(
            location=location,
            child=HTML(html_template(*args, **kwargs))
        )
        return popup

    # Appends markers to map based on df
    # and return map
    @staticmethod
    def create_stations_map(df):
        m1 = StudyMap.create_map(scroll_wheel_zoom=True)

        for station_type in df.StationType.unique().tolist():
            mask = (df["StationType"] == station_type)
            df2 = df.loc[mask]

            # markers that will be added to the cluster...
            markers = []
            for idx, row in df2.iterrows():
                location = [row.geometry.y, row.geometry.x]                
                popup = StudyMap.create_popups_from_template(
                    location,
                    POPUP_TEMPLATE,
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

                icon_name = "check-circle" if row.Status == "Active" else "times-circle"

                icon = AwesomeIcon(
                    name=icon_name,
                    marker_color=get_color(row.StationType),
                    icon_color='white',
                    spin=False
                )

                markers.append(
                    Marker(
                        location=location,
                        popup=popup,
                        title=f"{row.StationType} - {row.StationCode}",
                        icon=icon
                    )
                )
            # Group all the markers for each station type
            # and add them as a layer to map
            marker_cluster = MarkerCluster(
                name=station_type,
                markers=markers
            )
            m1.add_layer(marker_cluster)
        # Create the layer control and add to map
        control = LayersControl(position='topright')
        m1.add_control(control)
        return m1
