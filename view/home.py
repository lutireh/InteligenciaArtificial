import plotly.express as px
import pandas as pd


possibleNodes = []

with open('./map/possibleNodes.txt', 'r', encoding='utf-8') as file:

    lines = file.readlines()
    for line in lines:
        line = line.strip()
        possibleNodes.append(line)
    print(f'Os nós possíveis são: {possibleNodes}')


app.layout = html.Div([
    html.H1(children='A* para entregas', style={'textAlign':'center'}),
    dcc.Dropdown(possibleNodes, 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content','figure'),
    Input('dropdown-selection','value')
)

def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run_server(debug=True)