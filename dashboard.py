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
    dcc.Graph(id='test-type-distribution-graph'),
    dcc.Graph(id='modified-summary-distribution-graph'),
    dcc.Graph(id='feature-type-distribution-graph'),
    dcc.Graph(id='defect-distribution-graph'),
    dcc.Graph(id='labels-distribution-graph'),
    html.Div(id='selected-category'),
])

# Define callback to update the Defect Type graph and display details
@app.callback(
    Output('test-type-distribution-graph', 'figure'),
    Output('selected-category', 'children'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_test_type_graph(selectedData):
    selected_category = ""

    try:
        if selectedData is not None:
            # Get the selected category (Defect Type)
            selected_category = selectedData['points'][0]['x']

            # Filter data for the selected category
            filtered_data = df[df['Test Type'] == selected_category]

            # Calculate the frequency of the selected category
            category_counts = filtered_data['Test Type'].value_counts()
            fig = px.bar(category_counts, x=list(category_counts.index), y=category_counts.values,
                         title=f"Details for Test Type: {selected_category}",
                         labels={'x': 'Test Type', 'y': 'Count'},
                         template='plotly_white')
        else:
            # Calculate the frequency of each test type
            test_type_counts = df['Test Type'].value_counts()
            fig = px.bar(test_type_counts, x=list(test_type_counts.index), y=test_type_counts.values,
                         title="Test Type Distribution",
                         labels={'x': 'Test Type', 'y': 'Count'},
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
    Output('modified-summary-distribution-graph', 'figure'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_summary_graph(selectedData):
    selected_category = ""

    try:
        if selectedData is not None:
            # Get the selected category (test Type)
            selected_category = selectedData['points'][0]['x']

            # Filter data for the selected category
            filtered_data = df[df['Test Type'] == selected_category]

            # Calculate the frequency of each feature type within the selected Modified Summary
            feature_counts = filtered_data['Modified Summary'].value_counts()
            fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
                         title=f"Quest Number Distribution for Test Type: {selected_category}",
                         labels={'x': 'Quest Number', 'y': 'Count'},
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

# # Define callback to update the Modified Summary graph based on Feature Type
# @app.callback(
#     Output('modified-summary-distribution-graph', 'figure'),
#     Input('feature-distribution-graph', 'selectedData'),
#     Input('defect-distribution-graph', 'selectedData')
# )
# def update_modified_summary_graph(selectedFeatureData, selectedDefectData):
#     global selected_summary
#     global selected_defect

#     try:
#         if selectedFeatureData is not None:
#             # Get the selected feature (Modified Summary)
#             selected_summary = selectedFeatureData['points'][0]['x']

#         if selectedDefectData is not None:
#             # Get the selected defect type
#             selected_defect = selectedDefectData['points'][0]['x']

#         # Filter data based on both selected defect and summary
#         filtered_data = df[(df['Modified Summary'] == selected_summary) & (df['Defect Type'] == selected_defect)]

#         # Calculate the frequency of each feature type within the selected Modified Summary and Defect Type
#         feature_counts = filtered_data['Feature Type'].value_counts()
#         fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
#                      title=f"Feature Type Distribution for Modified Summary: {selected_summary} and Defect Type: {selected_defect}",
#                      labels={'x': 'Feature Type', 'y': 'Count'},
#                      template='plotly_white')

#         fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                           marker_line_width=1.5, opacity=0.6,
#                           texttemplate='%{y}', textposition='outside')

#         fig.update_layout(clickmode='event+select')

#         return fig

#     except Exception as e:
#         return {}

    
# # Define callback to update the Test Type drill-down graph
# @app.callback(
#     Output('test-type-distribution-graph', 'figure'),
#     Input('defect-distribution-graph', 'selectedData')
# )
# def update_test_type_graph(selectedData):
#     selected_defect_type = ""

#     try:
#         if selectedData is not None:
#             # Get the selected defect type
#             selected_defect_type = selectedData['points'][0]['x']

#             # Filter data for the selected defect type
#             filtered_data = df[df['Defect Type'] == selected_defect_type]

#             # Calculate the frequency of each test type within the selected defect type
#             test_type_counts = filtered_data['Test Type'].value_counts()
#             fig = px.bar(test_type_counts, x=list(test_type_counts.index), y=test_type_counts.values,
#                          title=f"Test Type Distribution for Defect Type: {selected_defect_type}",
#                          labels={'x': 'Test Type', 'y': 'Count'},
#                          template='plotly_white')

#         else:
#             # If no Defect Type is selected, show an empty graph
#             fig = go.Figure()

#         fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                           marker_line_width=1.5, opacity=0.6,
#                           texttemplate='%{y}', textposition='outside')

#         fig.update_layout(clickmode='event+select')

#         return fig

#     except Exception as e:
#         return {}
    
# @app.callback(
#     Output('creator-distribution-graph', 'figure'),
#     Input('defect-distribution-graph', 'selectedData')
# )
# def update_creator_graph(selectedData):
#     defect_selected = ""

#     try:
#         if selectedData is not None:
#             defect_selected = selectedData['points'][0]['x']

#             filtered_data = df[df['Defect Type'] == defect_selected]

#             creator_counts = filtered_data['Creator'].value_counts()
#             fig = px.bar(creator_counts, x=list(creator_counts.index), y=creator_counts.values,
#                          title=f"Distribution of Issue Creator by Defect Type: {defect_selected}",
#                          labels={'x': 'Creator', 'y': 'Count'},
#                          template='plotly_white')
#         else:
#             fig = go.Figure()

#         fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                           marker_line_width=1.5, opacity=0.6,
#                           texttemplate='%{y}', textposition='outside')

#         fig.update_layout(clickmode='event+select')

#         return fig

#     except Exception as e:
#         return {}

    
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
