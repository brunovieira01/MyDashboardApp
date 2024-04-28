import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Read data
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean().reset_index()

# Create Dash app
app = Dash(__name__)

# Get all unique bee diseases
all_diseases = df['Affected by'].unique()

# App layout
app.layout = html.Div([
    html.H1("Bee Colonies Affected: U.S.", style={'textAlign': 'center', 'color': '#000000'}),
    
    html.Div([
        html.Div([
            html.Label("Select Year:", style={'fontSize': '20px'}),
            dcc.Dropdown(
                id="slct_year",
                options=[
                    {"label": str(year), "value": year}
                    for year in df['Year'].unique()
                ],
                multi=False,
                value=df['Year'].min(),
                style={'width': "100%"}
            )
        ], style={'width': '45%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select Bee Disease:", style={'fontSize': '20px'}),
            dcc.Dropdown(
                id="slct_disease",
                options=[
                    {"label": disease, "value": disease}
                    for disease in all_diseases
                ],
                multi=False,
                value=all_diseases[0],
                style={'width': "100%"}
            )
        ], style={'width': '45%', 'display': 'inline-block'})
    ], style={'textAlign': 'left', 'marginBottom': '20px'}),
    
    html.Div(id='output_container', children=[], style={'textAlign': 'center', 'fontSize': '20px'}),
    
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])


# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_disease', component_property='value')]
)
def update_graph(option_slctd_year, option_slctd_disease):
    container = f"The year chosen by user was: {option_slctd_year}, affected by {option_slctd_disease}."
    
    dff = df[df["Year"] == option_slctd_year]
    dff = dff[dff["Affected by"] == option_slctd_disease]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    return container, fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
