import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Read data from Excel file
df = pd.read_csv('new.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='defect-distribution-graph'),
    dcc.Graph(id='feature-distribution-graph'),
    html.Div(id='selected-category'),
])

# Define callback to update the Defect Type graph and display details
@app.callback(
    Output('defect-distribution-graph', 'figure'),
    Output('selected-category', 'children'),
    Input('defect-distribution-graph', 'selectedData')
)
def update_defect_graph(selectedData):
    selected_category = ""

    try:
        if selectedData is not None:
            # Get the selected category (Defect Type)
            selected_category = selectedData['points'][0]['x']

            # Filter data for the selected category
            filtered_data = df[df['Defect Type'] == selected_category]

            # Calculate the frequency of the selected category
            category_counts = filtered_data['Defect Type'].value_counts()
            fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                         title=f"Details for Defect Type: {selected_category}",
                         labels={'x': 'Defect Type', 'y': 'Count'},
                         template='plotly_white')
        else:
            # Calculate the frequency of each defect type
            defect_counts = df['Defect Type'].value_counts()
            fig = px.bar(defect_counts, x=defect_counts.index, y=defect_counts.values,
                         title="Defect Type Distribution",
                         labels={'x': 'Defect Type', 'y': 'Count'},
                         template='plotly_white')

        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6,
                          texttemplate='%{y}', textposition='outside')

        fig.update_layout(clickmode='event+select')

        return fig, f"Selected Category: {selected_category}"

    except Exception as e:
        return {}, f"Error: {str(e)}"

# Define callback to update the Feature Type graph
@app.callback(
    Output('feature-distribution-graph', 'figure'),
    Input('defect-distribution-graph', 'selectedData')
)
def update_feature_graph(selectedData):
    selected_category = ""

    try:
        if selectedData is not None:
            # Get the selected category (Defect Type)
            selected_category = selectedData['points'][0]['x']

            # Filter data for the selected category
            filtered_data = df[df['Defect Type'] == selected_category]

            # Calculate the frequency of each feature type within the selected Defect Type
            feature_counts = filtered_data['Feature Type'].value_counts()
            fig = px.bar(feature_counts, x=feature_counts.index, y=feature_counts.values,
                         title=f"Feature Type Distribution for Defect Type: {selected_category}",
                         labels={'x': 'Feature Type', 'y': 'Count'},
                         template='plotly_white')

        else:
            # If no Defect Type is selected, show an empty graph
            fig = go.Figure()

        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6,
                          texttemplate='%{y}', textposition='outside')


        fig.update_layout(clickmode='event+select')

        return fig

    except Exception as e:
        return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
