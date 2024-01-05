import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Charger les données
data = pd.read_csv('arbres10percent.csv')

# Initialiser ton app Dash
app = dash.Dash(__name__)

# Créer le layout de ton app
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='domanialite-dropdown',
            options=[
                {'label': domanialite, 'value': domanialite}
                for domanialite in data['DOMANIALITE'].unique()
            ],
            value=data['DOMANIALITE'].iloc[0],  # Valeur par défaut
            multi=False,
            style={'width': '100%'}  # Largeur à 100%
        ),
        dcc.Dropdown(
            id='stade-dropdown',
            options=[
                {'label': stade, 'value': stade}
                for stade in data['STADE DE DEVELOPPEMENT'].unique()
                if pd.notna(stade)  # Supprimer les valeurs nulles
            ],
            value=data['STADE DE DEVELOPPEMENT'].iloc[1],  # Valeur par défaut
            multi=False,
            style={'width': '100%'}  # Largeur à 100%
        ),
    ], style={'display': 'flex', 'gap': '20px'}),  # Ajout de l'espace
    html.Div([
        dcc.Graph(id='histogram-circonference', style={'width': '50vw', 'height': '50vw'}),
        dcc.Graph(id='histogram-hauteur', style={'width': '50vw', 'height': '50vw'})
    ], style={'display': 'flex', 'gap': '20px', 'flexDirection': 'row', 'width': '100%'}),
    dcc.Graph(id='genre-map', style={'width': '50vw', 'height': '50vw'})
])

# Définir la logique de callback pour mettre à jour les histogrammes et la carte en fonction des menus déroulants
@app.callback(
    [Output('histogram-circonference', 'figure'),
     Output('histogram-hauteur', 'figure')],
    [Input('domanialite-dropdown', 'value'),
     Input('stade-dropdown', 'value')]
)
def update_histograms(selected_domanialite, selected_stade):
    # Filtrer les données pour les histogrammes
    filtered_data = data[(data['DOMANIALITE'] == selected_domanialite) & (data['STADE DE DEVELOPPEMENT'] == selected_stade)]

    # Histogrammes
    fig_circonference = px.histogram(filtered_data, x='CIRCONFERENCE (cm)', title=f'Histogramme de la circonférence pour {selected_domanialite} - {selected_stade}', nbins=20)
    fig_hauteur = px.histogram(filtered_data, x='HAUTEUR (m)', title=f'Histogramme de la hauteur pour {selected_domanialite} - {selected_stade}', nbins=20)

    return fig_circonference, fig_hauteur

# Définir la logique de callback pour mettre à jour la carte en fonction de tous les arbres
@app.callback(
    Output('genre-map', 'figure'),
    [Input('domanialite-dropdown', 'value'),
     Input('stade-dropdown', 'value')]
)
def update_map(selected_domanialite, selected_stade):
    # Carte
    fig_map = px.scatter_mapbox(
        data,
        lat=data['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
        lon=data['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
        color='GENRE',
        title=f'Carte des arbres par genre',
        mapbox_style="carto-positron",
        zoom=10
    )

    return fig_map

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
