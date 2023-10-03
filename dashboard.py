import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

class JiraDashboardApp:
    def __init__(self, data_file='modified_new.csv'):
        self.df = pd.read_csv(data_file)
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.server = self.app.server
        self.selected_summary = ""
        self.selected_defect = ""
        
        self.app.layout = html.Div([
            dcc.Graph(id='defect-distribution-graph'),
            dcc.Graph(id='feature-distribution-graph'),
            dcc.Graph(id='modified-summary-distribution-graph'),
            dcc.Graph(id='test-type-distribution-graph'),
            dcc.Graph(id='creator-distribution-graph'),
            html.Div(id='selected-category'),
        ])

        self.app.callback(
            Output('defect-distribution-graph', 'figure'),
            Output('selected-category', 'children'),
            Input('defect-distribution-graph', 'selectedData')
        )(self.update_defect_graph)
        
        self.app.callback(
            Output('feature-distribution-graph', 'figure'),
            Input('defect-distribution-graph', 'selectedData')
        )(self.update_summary_graph)

        self.app.callback(
            Output('modified-summary-distribution-graph', 'figure'),
            Input('feature-distribution-graph', 'selectedData'),
            Input('defect-distribution-graph', 'selectedData')
        )(self.update_modified_summary_graph)

        self.app.callback(
            Output('test-type-distribution-graph', 'figure'),
            Input('defect-distribution-graph', 'selectedData')
        )(self.update_test_type_graph)

        self.app.callback(
            Output('creator-distribution-graph', 'figure'),
            Input('defect-distribution-graph', 'selectedData')
        )(self.update_creator_graph)

    def run(self):
        self.app.run_server(debug=True, use_reloader=False)

    def update_defect_graph(self, selectedData):
        selected_category = ""

        try:
            if selectedData is not None:
                selected_category = selectedData['points'][0]['x']
                filtered_data = self.df[self.df['Defect Type'] == selected_category]
                category_counts = filtered_data['Defect Type'].value_counts()
                fig = px.bar(category_counts, x=list(category_counts.index), y=category_counts.values,
                             title=f"Details for Defect Type: {selected_category}",
                             labels={'x': 'Defect Type', 'y': 'Count'},
                             template='plotly_white')
            else:
                defect_counts = self.df['Defect Type'].value_counts()
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

    def update_summary_graph(self, selectedData):
        selected_category = ""

        try:
            if selectedData is not None:
                selected_category = selectedData['points'][0]['x']
                filtered_data = self.df[self.df['Defect Type'] == selected_category]
                feature_counts = filtered_data['Modified Summary'].value_counts()
                fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
                             title=f"Modified Summary Distribution for Defect Type: {selected_category}",
                             labels={'x': 'Modified Summary', 'y': 'Count'},
                             template='plotly_white')

            else:
                fig = go.Figure()

            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6,
                              texttemplate='%{y}', textposition='outside')

            fig.update_layout(clickmode='event+select')

            return fig

        except Exception as e:
            return {}

    def update_modified_summary_graph(self, selectedFeatureData, selectedDefectData):
        try:
            if selectedFeatureData is not None:
                self.selected_summary = selectedFeatureData['points'][0]['x']

            if selectedDefectData is not None:
                self.selected_defect = selectedDefectData['points'][0]['x']

            filtered_data = self.df[(self.df['Modified Summary'] == self.selected_summary) & 
                                    (self.df['Defect Type'] == self.selected_defect)]

            feature_counts = filtered_data['Feature Type'].value_counts()
            fig = px.bar(feature_counts, x=list(feature_counts.index), y=feature_counts.values,
                         title=f"Feature Type Distribution for Modified Summary: {self.selected_summary} and Defect Type: {self.selected_defect}",
                         labels={'x': 'Feature Type', 'y': 'Count'},
                         template='plotly_white')

            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6,
                              texttemplate='%{y}', textposition='outside')

            fig.update_layout(clickmode='event+select')

            return fig

        except Exception as e:
            return {}

    def update_test_type_graph(self, selectedData):
        selected_defect_type = ""

        try:
            if selectedData is not None:
                selected_defect_type = selectedData['points'][0]['x']
                filtered_data = self.df[self.df['Defect Type'] == selected_defect_type]
                test_type_counts = filtered_data['Test Type'].value_counts()
                fig = px.bar(test_type_counts, x=list(test_type_counts.index), y=test_type_counts.values,
                             title=f"Test Type Distribution for Defect Type: {selected_defect_type}",
                             labels={'x': 'Test Type', 'y': 'Count'},
                             template='plotly_white')

            else:
                fig = go.Figure()

            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6,
                              texttemplate='%{y}', textposition='outside')

            fig.update_layout(clickmode='event+select')

            return fig

        except Exception as e:
            return {}
    
    def update_creator_graph(self, selectedData):
        defect_selected = ""

        try:
            if selectedData is not None:
                defect_selected = selectedData['points'][0]['x']
                filtered_data = self.df[self.df['Defect Type'] == defect_selected]
                creator_counts = filtered_data['Creator'].value_counts()
                fig = px.bar(creator_counts, x=list(creator_counts.index), y=creator_counts.values,
                             title=f"Distribution of Issue Creator by Defect Type: {defect_selected}",
                             labels={'x': 'Creator', 'y': 'Count'},
                             template='plotly_white')
            else:
                fig = go.Figure()

            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6,
                              texttemplate='%{y}', textposition='outside')

            fig.update_layout(clickmode='event+select')

            return fig

        except Exception as e:
            return {}

if __name__ == '__main__':
    dashboard_app = JiraDashboardApp()
    dashboard_app.run()
