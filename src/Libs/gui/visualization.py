import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import math


class VisualizationHandler():
    def plot_3d_coordinates(self,df:pd.DataFrame, title='3D Coordinates', label='Location (meters)'):
        fig = go.Figure()

        x = df['Acceleration_X'].cumsum()  # Cumulative sum for x-coordinate
        y = df['Acceleration_Y'].cumsum()  # Cumulative sum for y-coordinate
        z = df['Acceleration_Z'].cumsum()  # Cumulative sum for z-coordinate

        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            name=label
        ))

        fig.update_layout(scene=dict(xaxis_title='X (meters)', yaxis_title='Y (meters)', zaxis_title='Z (meters)'),
                        title=title)

        return fig


    def plot_2d_path_on_map(self,df:pd.DataFrame, title='2D Path on Map'):
        
        df['Time_Delta'] = pd.to_datetime(df['Timestamp']).diff().fillna(pd.Timedelta(seconds=0))
        df['Time_Delta'] = df['Time_Delta'].astype('int64')/10**9
        print(df['Time_Delta'])

        df['Accel_X_meters'] = df['Acceleration_X']*df["Time_Delta"].apply(lambda x: x**2)  # Convert acceleration to displacement in x direction
        df['Accel_Y_meters'] = df['Acceleration_Y']*df["Time_Delta"].apply(lambda x: x**2)  # Convert acceleration to displacement in y direction
        df['Accel_Z_meters'] = df['Acceleration_Z']*df["Time_Delta"].apply(lambda x: x**2)

        df['Accel_X_meters'] = df['Accel_X_meters'].cumsum()
        df['Accel_Y_meters'] = df['Accel_Y_meters'].cumsum()
        df['Accel_Z_meters'] = df['Accel_Z_meters'].cumsum()

        new_lon = []
        new_lat = []
        start_lat = 47.22436745102312
        start_lon = 7.805994521671979
        for i in df['Accel_X_meters']:
            print(i)
            lat = start_lat  + (i / 6378137 ) * (180 / math.pi);
            new_lat.append(lat)
        for i in df["Accel_Y_meters"]:
            lon = start_lon  + (i / 6378137 ) * (180 / math.pi);
            new_lon.append(lon)

        fig = sp.make_subplots(rows=5, cols=1, subplot_titles=['Map plot', 'height plot','path plot'],
                               specs=[[{"type": "mapbox","rowspan":2}],[None],[{"type": "xy"}],[{"type":"scene","rowspan":2}],[None]])

        map2d = go.Scattermapbox(
        mode='markers+lines',
        lat=new_lat,
        lon=new_lon,
        marker=dict(
            size=2,
            color='blue'
        ),
        line=dict(
            width=1,
            color='red'
        ),
        text=df.index,  # Display index as hover text
        hoverinfo='text+lon+lat'
        )

        fig.add_trace(map2d, row=1,col=1)

        scatter_2d = go.Scatter(
            x=df.index,  # X-axis represents the index (time or data points)
            y=df['Acceleration_Z'].cumsum(),
            mode='lines+markers',
            name='2D Plot'
        )
        
        fig.add_trace(scatter_2d, row=3,col=1)

        scatter_3d= go.Scatter3d(
            x=df['Accel_X_meters'],
            y=df['Accel_Y_meters'],
            z=df['Accel_Z_meters'],
            mode='lines',
            name='3d Path plot'
        )

        fig.add_trace(scatter_3d, row=4,col=1)

        fig.update_layout(
        title=title,
        mapbox=dict(
            style='open-street-map',  # You can choose different map styles
            zoom=15,
            center=dict(lon=start_lon, lat=start_lat)
        ),
        showlegend=False,  # Hide individual legends for each subplot
        xaxis_title='Time',  # Adjust the x-axis title as needed
        yaxis_title='Height (meters)',
        height=3000
    )

        return fig
