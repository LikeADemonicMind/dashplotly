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
    html.Div([
        dcc.Graph(id='genre-map', style={'width': '50vw', 'height': '50vw'}),
        dcc.Graph(id='libelle-francais-map', style={'width': '50vw', 'height': '50vw'})
    ], style={'display': 'flex', 'gap': '20px', 'flexDirection': 'row', 'width': '100%'}),
    html.Div([
        dcc.Graph(id='stade-development-map', style={'width': '50vw', 'height': '50vw'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '50vw'}),
    html.Div([
        dcc.Dropdown(
            id='arrondissement-dropdown',
            options=[
                {'label': arrondissement, 'value': arrondissement}
                for arrondissement in data['ARRONDISSEMENT'].unique()
                if pd.notna(arrondissement)  # Supprimer les valeurs nulles
            ],
            value=data['ARRONDISSEMENT'].iloc[0],  # Valeur par défaut
            multi=False,
            style={'width': '100%'}  # Largeur à 100%
        ),
    ]),
    # Placer la carte des arrondissements en bas
    html.Div([
        dcc.Graph(id='arrondissement-libelle-francais-map', style={'width': '100%', 'height': '50vw'})
    ]),
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

    # Histogrammes avec contours
    fig_circonference = px.histogram(filtered_data, x='CIRCONFERENCE (cm)', title=f'Histogramme de la circonférence pour {selected_domanialite} - {selected_stade}', nbins=20, barmode='overlay', histnorm='percent')
    fig_circonference.update_traces(marker=dict(color='rgba(0, 0, 255, 0.5)', line=dict(color='rgba(0, 0, 0, 1)', width=1)))

    fig_hauteur = px.histogram(filtered_data, x='HAUTEUR (m)', title=f'Histogramme de la hauteur pour {selected_domanialite} - {selected_stade}', nbins=20, barmode='overlay', histnorm='percent')
    fig_hauteur.update_traces(marker=dict(color='rgba(0, 0, 255, 0.5)', line=dict(color='rgba(0, 0, 0, 1)', width=1)))

    return fig_circonference, fig_hauteur

# Définir la logique de callback pour mettre à jour la carte en fonction de tous les arbres
@app.callback(
    [Output('genre-map', 'figure'),
     Output('libelle-francais-map', 'figure')],
    [Input('domanialite-dropdown', 'value'),
     Input('stade-dropdown', 'value')]
)
def update_maps(selected_domanialite, selected_stade):
    # Carte Genre
    fig_genre_map = px.scatter_mapbox(
        data,
        lat=data['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
        lon=data['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
        color='GENRE',
        title=f'Carte des arbres par genre',
        mapbox_style="carto-positron",
        zoom=10
    )

    # Carte Libellé Français
    fig_libelle_francais_map = px.scatter_mapbox(
        data,
        lat=data['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
        lon=data['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
        color='LIBELLE FRANCAIS',
        title=f'Carte des arbres par libellé français',
        mapbox_style="carto-positron",
        zoom=10
    )

    return fig_genre_map, fig_libelle_francais_map

@app.callback(
    Output('stade-development-map', 'figure'),
    [Input('domanialite-dropdown', 'value')]
)
def update_stade_map(selected_domanialite):
    # Carte Stade de Développement
    fig_stade_map = px.scatter_mapbox(
        data,
        lat=data['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
        lon=data['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
        color='STADE DE DEVELOPPEMENT',
        title=f'Carte des arbres par stade de développement',
        mapbox_style="carto-positron",
        zoom=10
    )

    return fig_stade_map

@app.callback(
    Output('arrondissement-libelle-francais-map', 'figure'),
    [Input('arrondissement-dropdown', 'value')]
)
def update_arrondissement_libelle_francais_map(selected_arrondissement):
    # Filtrer les données pour la carte
    filtered_data = data[data['ARRONDISSEMENT'] == selected_arrondissement]

    # Carte Libellé Français par Arrondissement
    fig_arrondissement_libelle_francais_map = px.scatter_mapbox(
        filtered_data,
        lat=filtered_data['geo_point_2d'].apply(lambda x: float(x.split(',')[0])),
        lon=filtered_data['geo_point_2d'].apply(lambda x: float(x.split(',')[1])),
        color='LIBELLE FRANCAIS',
        title=f'Carte des arbres par libellé français dans l\'arrondissement {selected_arrondissement}',
        mapbox_style="carto-positron",
        zoom=12,
        height=600  # Ajuster la hauteur selon tes préférences
    )

    return fig_arrondissement_libelle_francais_map

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
