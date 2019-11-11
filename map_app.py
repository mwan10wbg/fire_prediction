import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
import plotly.graph_objects as go
#from plotly import graph_objects as go
from plotly.graph_objs import *
from datetime import datetime as dt

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoibWVpeGluLXdhbmciLCJhIjoiY2p6aW5scmo0MDB6ejNlazhidnFoYjB5MSJ9.QgnWR6h9ZMhEPRiPj_d7-g"

# Dictionary of important locations in Mexico City
list_of_locations = {
    "Washington": {"lat": 47.7511, "lon": -120.7401},
    "Oregon": {"lat": 43.8041, "lon": -120.5542},
    "California": {"lat": 36.7783, "lon": -119.4179},
}

# Get index for the specified month in the dataframe
monthList = ["Jan","Feb","Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Initialize data frame
df = pd.read_csv(
    '/Users/Meixin/fire/clusters_csv_data/cluster_over_month.csv',  #date 2017-09-07 to 2017-10-10
    dtype={"lon" : "float64", "lat" : "float64", "num" : "int", "month" : "object"},
)
df_m = pd.read_csv(
    '/Users/Meixin/fire/over_month_csv_data/states_over_month.csv',  #date 2017-09-07 to 2017-10-10
    dtype={'month':'object','num':'int','state':'object'},
)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(className="logo", src=app.get_asset_url("dash-logo-new.png")),
                        html.H2("Predicting Risk of Fire Using Historical Data"),
                        html.P(
                            """Select different month using the month picker or by selecting
                             on the histogram."""
                        ),

                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in list_of_locations
                                            ],
                                            value = 'Washington',
                                            placeholder="Select a state",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": monthList[n],
                                                    "value": monthList[n],
                                                }
                                                for n in range(12)
                                            ],
                                            value='Aug',
                                            placeholder="Select a month",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-fires"),
                        html.P(id="total-fires-selection"),
                        html.P(id="month-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [Cumulative MODIS fire detection](https://fsapps.nwcg.gov/gisdata.php)"
                            ]),
                    ],
                    #style = {'width': '40%','display':'inline-block'}
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                "View the number of fires changing over a year in 2014-2018 in a selected state."
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(location,monthSelected):
    xVal = []
    yVal = list(df_m[df_m.state==location].num)
    xSelected = []
    colorVal = [
        "#ffbaba",
        "#ff7b7b",
        "#ff7b7b",
        "#ff5252",
        "#ff0000",
        "#a70000",
        "#a70000",
        "#ff0000",
        "#ff5252",
        "#ff7b7b",
        "#ff7b7b",
        "#ffbaba"
    ]

    for i in range(12):
        # If bar is selected then color it white
        if monthList[i] == monthSelected:
            colorVal[i+1] = "#FFFFFF"
        xVal.append(i)
    return [np.array(xVal), np.array(yVal), np.array(colorVal)]


# Selected Data in the Histogram updates the Values in the DatePicker
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"),Input("histogram", "clickData")],
)
def update_bar_selector(value,clickData):
    holder = ''
    if clickData:
        holder=monthList[int(clickData["points"][0]["x"])-1]
    if value:
        for x in value["points"]:
            holder=monthList[int(x["x"])-1]
    return holder

# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(clickData):
    if clickData:
        return {"points": []}


# Update the total number of fires Tag
@app.callback(Output("total-fires", "children"), [Input("bar-selector", "value")])
def update_total_rides(monthPicked):
    return "Total Number of fires: {:,d}".format(
        sum(df.num))


# Update the total number of rides in selected times
@app.callback(
    [Output("total-fires-selection", "children"), Output("month-value", "children")],
    [Input("bar-selector", "value")]
)
def update_total_rides_selection(monthPicked):
    firstOutput = "Total Pings in Selection: {:,d}".format(
        sum(df[df.month==monthPicked].num))
    return (firstOutput, 'in the month: '+monthPicked)


# Update Histogram Figure based on states Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("location-dropdown", "value"),Input("bar-selector", "value")],
)
def update_histogram(locationPicked,selection):
    [xVal, yVal, colorVal] = get_selection(locationPicked,selection)

    layout = go.Layout(
        bargap=0.3,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            range=[0.5, 12.5],
            showgrid=False,
            nticks=13,
            fixedrange=True,
            #ticksuffix=":00",
        ),
        yaxis=dict(
            range=[0, max(yVal) + max(yVal) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=False,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="white"),
            )
            for xi, yi in zip(xVal, yVal)
        ],
    )

    return go.Figure(
        data=[
            go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
            go.Scatter(
                opacity=0,
                x=xVal,
                y=yVal / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=layout,
    )


# Get the Coordinates of the chosen months, dates and times

@app.callback(
    Output("map-graph", "figure"),
    [
        Input("location-dropdown", "value"),
        Input("bar-selector", "value")
    ],
)
def update_geo_map(selectedLocation, month):
    zoom = 10.0
    latInitial = 43.8041
    lonInitial = -120.5542
    bearing = 0

    if selectedLocation:
        zoom = 12.0
        latInitial = list_of_locations[selectedLocation]["lat"]
        lonInitial = list_of_locations[selectedLocation]["lon"]

    listCoords = df[df.month==month][['lat','lon','num']]
    return go.Figure(
        data=[
            # Data for all rides based on date and time
            Scattermapbox(
                lat=list(listCoords["lat"]),
                lon=list(listCoords["lon"]),
                mode="markers",
                hoverinfo="lat+lon+text",
                text=listCoords["num"],
                marker=dict(
                    showscale=True,
                    color=np.insert(list(listCoords["num"]), 0, 0),
                    opacity=0.9,
                    size=25,
                    #colorscale="Reds"
                    colorscale=[
                        #[0, "#428bca"],
                        [0, "#f9f9f9"],
                        [0.5, "#ff6969"],
                        [1, "#d9534f"],
                    ],
                    colorbar=dict(
                        title="Number<br>of Fires",
                        x=0.93,
                        xpad=0,
                        nticks=12,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            # Plot of important locations on the map
            Scattermapbox(
                lat=[list_of_locations[i]["lat"] for i in list_of_locations],
                lon=[list_of_locations[i]["lon"] for i in list_of_locations],
                mode="markers",
                hoverinfo="text",
                text=[i for i in list_of_locations],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 19.5  # -99
                style="mapbox://styles/meixin-wang/ck2tvfsup5q9a1cnz45ewomg1",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-99",
                                        "mapbox.center.lat": "19.5",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )

if __name__ == "__main__":
    app.run_server(debug=True)
