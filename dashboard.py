import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Read data from Excel file
df = pd.read_csv('modified_new.csv')

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server


# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='defect-distribution-graph'),
    dcc.Graph(id='feature-distribution-graph'),
    dcc.Graph(id='modified-summary-distribution-graph'),
    dcc.Graph(id='test-type-distribution-graph'),
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
            fig = px.bar(category_counts, x=list(category_counts.index), y=category_counts.values,
                         title=f"Details for Defect Type: {selected_category}",
                         labels={'x': 'Defect Type', 'y': 'Count'},
                         template='plotly_white')
        else:
            # Calculate the frequency of each defect type
            defect_counts = df['Defect Type'].value_counts()
            fig = px.bar(defect_counts, x=list(defect_counts.index), y=defect_counts.values,
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
def update_summary_graph(selectedData):
    selected_category = ""

    try:
        if selectedData is not None:
            # Get the selected category (Defect Type)
            selected_category = selectedData['points'][0]['x']

            # Filter data for the selected category
            filtered_data = df[df['Defect Type'] == selected_category]

            # Calculate the frequency of each feature type within the selected Modified Summary
            feature_counts = filtered_data['Modified Summary'].value_counts()
            fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
                         title=f"Modified Summary Distribution for Defect Type: {selected_category}",
                         labels={'x': 'Modified Summary', 'y': 'Count'},
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

# Define callback to update the Modified Summary graph based on Feature Type
@app.callback(
    Output('modified-summary-distribution-graph', 'figure'),
    Input('feature-distribution-graph', 'selectedData')
)
def update_modified_summary_graph(selectedData):
    selected_feature = ""

    try:
        if selectedData is not None:
            # Get the selected feature (Modified Summary)
            selected_feature = selectedData['points'][0]['x']

            # Filter data for the selected feature
            filtered_data = df[df['Modified Summary'] == selected_feature]

            # Calculate the frequency of each defect type within the selected Modified Summary
            defect_counts = filtered_data['Feature Type'].value_counts()
            fig = px.bar(defect_counts, x=list(defect_counts.index), y=defect_counts.values,
                         title=f"Feature Type Distribution for Modified Summary: {selected_feature}",
                         labels={'x': 'Feature Type', 'y': 'Count'},
                         template='plotly_white')

        else:
            # If no Feature Type is selected, show an empty graph
            fig = go.Figure()

        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                        marker_line_width=1.5, opacity=0.6,
                        texttemplate='%{y}', textposition='outside')

        fig.update_layout(clickmode='event+select')

        return fig

    except Exception as e:
        return {}
    
# Define callback to update the Test Type drill-down graph
@app.callback(
    Output('test-type-distribution-graph', 'figure'),
    Input('defect-distribution-graph', 'selectedData')
)
def update_test_type_graph(selectedData):
    selected_defect_type = ""

    try:
        if selectedData is not None:
            # Get the selected defect type
            selected_defect_type = selectedData['points'][0]['x']

            # Filter data for the selected defect type
            filtered_data = df[df['Defect Type'] == selected_defect_type]

            # Calculate the frequency of each test type within the selected defect type
            test_type_counts = filtered_data['Test Type'].value_counts()
            fig = px.bar(test_type_counts, x=list(test_type_counts.index), y=test_type_counts.values,
                         title=f"Test Type Distribution for Defect Type: {selected_defect_type}",
                         labels={'x': 'Test Type', 'y': 'Count'},
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
    app.run_server(debug=True, use_reloader=False)
