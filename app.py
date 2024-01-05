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
    dcc.Dropdown(
        id='domanialite-dropdown',
        options=[
            {'label': domanialite, 'value': domanialite}
            for domanialite in data['DOMANIALITE'].unique()
        ],
        value=data['DOMANIALITE'].iloc[0],  # Valeur par défaut
        multi=False,
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='stade-dropdown',
        options=[
            {'label': stade, 'value': stade}
            for stade in data['STADE DE DEVELOPPEMENT'].unique()
            if pd.notna(stade)  # Supprimer les valeurs nulles
        ],
        value=data['STADE DE DEVELOPPEMENT'].iloc[0],  # Valeur par défaut
        multi=False,
        style={'width': '50%'}
    ),
    dcc.Graph(id='histogram-circonference'),
    dcc.Graph(id='histogram-hauteur')
])

# Définir la logique de callback pour mettre à jour les histogrammes en fonction de la domanialité et du stade de développement sélectionnés
@app.callback(
    [Output('histogram-circonference', 'figure'),
     Output('histogram-hauteur', 'figure')],
    [Input('domanialite-dropdown', 'value'),
     Input('stade-dropdown', 'value')]
)
def update_histograms(selected_domanialite, selected_stade):
    filtered_data = data[(data['DOMANIALITE'] == selected_domanialite) & (data['STADE DE DEVELOPPEMENT'] == selected_stade)]

    fig_circonference = px.histogram(filtered_data, x='CIRCONFERENCE (cm)', title=f'Histogramme de la circonférence pour {selected_domanialite} - {selected_stade}', nbins=20)
    fig_hauteur = px.histogram(filtered_data, x='HAUTEUR (m)', title=f'Histogramme de la hauteur pour {selected_domanialite} - {selected_stade}', nbins=20)

    return fig_circonference, fig_hauteur

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
