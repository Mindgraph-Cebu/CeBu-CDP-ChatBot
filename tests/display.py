import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandasaiapp

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ask me", style={'text-align': 'center'}),  # Center-align the heading
    dcc.Input(id='input-string', type='text', placeholder="", style={'font-size': '24px', 'text-align': 'center'}),  # Increase font size and center-align
    html.Button('Submit', id='submit-button', n_clicks=0, style={'text-align': 'center'}),
    html.Div(id='output-div', style={'text-align': 'center'})
], style={'text-align': 'center'}) 

@app.callback(
    Output('output-div', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-string', 'value')]
)
def update_output_div(n_clicks, input_string):
    if n_clicks > 0:
        if input_string:
            return html.Div([
                html.H3("Here's what I found : "),
                html.Div(pandasaiapp.get_response(input_string))
            ])
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
