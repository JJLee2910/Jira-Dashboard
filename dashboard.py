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

# Define callback to update the test Type graph and display details
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

# Define callback to update the quest number graph based on test type
@app.callback(
    Output('modified-summary-distribution-graph', 'figure'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_modified_summary_graph(selectedData):
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

# Callback to update the feature graph based on test type and quest number
@app.callback(
    Output('feature-type-distribution-graph', 'figure'),
    Input('modified-summary-distribution-graph', 'selectedData'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_feature_graph(selectedFeatureData, selectedTestTypeData):
    selected_summary = ""
    selected_test = ""

    try:
        if selectedFeatureData is not None:
            # Get the selected feature (Modified Summary)
            selected_summary = selectedFeatureData['points'][0]['x']

        if selectedTestTypeData is not None:
            # Get the selected test type
            selected_test = selectedTestTypeData['points'][0]['x']

        # Filter data based on both selected test type and quest numb
        filtered_data = df[(df['Test Type'] == selected_test) & (df['Modified Summary'] == selected_summary)]

        # Calculate the frequency of each feature type within the selected Quest Number and Test Type
        feature_counts = filtered_data['Feature Type'].value_counts()
        fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
                     title=f"Test Type Distribution for Quest Number: {selected_summary} and Test Type: {selected_test}",
                     labels={'x': 'Feature Type', 'y': 'Count'},
                     template='plotly_white')

        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6,
                          texttemplate='%{y}', textposition='outside')

        fig.update_layout(clickmode='event+select')

        return fig

    except Exception as e:
        return {}

# Callback to update the Defect Type graph based on Test Type, Quest Number & Feature Type
@app.callback(
    Output('defect-distribution-graph', 'figure'),
    Input('feature-type-distribution-graph', 'selectedData'),
    Input('modified-summary-distribution-graph', 'selectedData'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_defect_graph(selectedFeatureData, selectedModifiedSummaryData, selectedTestTypeData):
    try:
        if selectedFeatureData is not None:
            selected_summary = ""
            selected_category = ""

            if selectedModifiedSummaryData is not None:
                # Get the selected feature (Modified Summary)
                selected_summary = selectedModifiedSummaryData['points'][0]['x']

            if selectedTestTypeData is not None:
                # Get the selected category (Test Type)
                selected_category = selectedTestTypeData['points'][0]['x']

            # Filter the data based on the selected data from the previous 3 graphs
            filtered_data = df.copy()  # start with a copy of the data frame

            if selected_summary:
                filtered_data = filtered_data[filtered_data['Modified Summary'] == selected_summary]

            if selected_category:
                filtered_data = filtered_data[filtered_data['Test Type'] == selected_category]

            # calculate the frequency of the selected defect type
            defect_counts = filtered_data['Defect Type'].value_counts()

            # Create the bar chart for the Defect Type distribution
            fig = px.bar(defect_counts, x=list(defect_counts.index), y=defect_counts.values,
                        title="Defect Type Distribution",
                        labels={'x': 'Defect Type', 'y': 'Count'},
                        template='plotly_white')

            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                            marker_line_width=1.5, opacity=0.6,
                            texttemplate='%{y}', textposition='outside')

            fig.update_layout(clickmode='event+select')

            return fig
        else:
            # If no Feature Type is selected, show an empty graph
            return go.Figure()

    except Exception as e:
        return {}

# Callback to update the labels graph based on previous 4 drill downs
@app.callback(
    Output('labels-distribution-graph', 'figure'),
    Input('defect-distribution-graph', 'selectedData'),
    Input('feature-type-distribution-graph', 'selectedData'),
    Input('modified-summary-distribution-graph', 'selectedData'),
    Input('test-type-distribution-graph', 'selectedData')
)
def update_labels_graph(selectedDefectData, selectedFeatureData, selectedModifiedSummaryData, selectedTestTypeData):
    try:
        if selectedDefectData is not None:
            selected_defect = selectedDefectData['points'][0]['x']
            
            filtered_data = df[df['Defect Type'] == selected_defect]
            
            if selectedFeatureData:
                selected_feature = selectedFeatureData['points'][0]['x']
                filtered_data = filtered_data[filtered_data['Feature Type'] == selected_feature]
            
            if selectedModifiedSummaryData:
                selected_summary = selectedModifiedSummaryData['points'][0]['x']
                filtered_data = filtered_data[filtered_data['Modified Summary'] == selected_summary]
            
            if selectedTestTypeData:
                selected_category = selectedTestTypeData['points'][0]['x']
                filtered_data = filtered_data[filtered_data['Test Type'] == selected_category]
            
            # Combine the results from both "Labels" and "Labels.1" columns using "/" separator
            combined_labels = filtered_data['Labels'] + '/' + filtered_data['Labels.1']

            combined_label_counts = combined_labels.value_counts()
            
            if not combined_label_counts.empty:
                fig = px.bar(combined_label_counts, x=list(combined_label_counts.index), y=combined_label_counts.values,
                            title="Label Distribution",
                            labels={'x': 'Label', 'y': 'Count'},
                            template='plotly_white')

                fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                marker_line_width=1.5, opacity=0.6,
                                texttemplate='%{y}', textposition='outside')

                fig.update_layout(clickmode='event+select')

                return fig

        # If no Defect Type is selected or no data for the selection, show an empty graph
        return go.Figure()

    except Exception as e:
        return {}


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
