import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/results.csv")
all_data = df.copy()

app = dash.Dash(__name__)

carbon_rates = sorted(all_data['carbon_rate'].unique())

app.layout = html.Div([
    html.H1("3D Visualization of Allocation by Land Use"),

    html.Label("Select Carbon Rate:"), 
    dcc.Slider(
        id='carbon-rate-slider',
        min=0,
        max=len(carbon_rates) - 1,
        step=1,
        value=0,
        marks={i: str(carbon_rates[i]) for i in range(len(carbon_rates))}
    ),

    html.Br(),

    html.Label("Select Region:"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': r, 'value': r} for r in sorted(all_data['region'].unique()) if r != 'ALL'],
        value=sorted(all_data['region'].unique())[0]
    ),

    html.Br(),

    dcc.Graph(id='3d-allocation-plot')
])


@app.callback(
    Output('3d-allocation-plot', 'figure'),
    Input('carbon-rate-slider', 'value'),
    Input('region-dropdown', 'value')
)
def update_3d_plot(carbon_rate_index, selected_region):
    current_carbon_rate = carbon_rates[carbon_rate_index]
    filtered = all_data[
        (all_data['carbon_rate'] == current_carbon_rate) &
        (all_data['region'] == selected_region)
    ]

    fig = px.scatter_3d(
        filtered,
        x='carbon_price',
        y='prod_price',
        z='allocation',
        color='land_use', 
        symbol='land_use',
        title=f"Allocation by Land Use at carbon_rate={current_carbon_rate}, region={selected_region}",
        labels={'allocation': 'Allocation'}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
