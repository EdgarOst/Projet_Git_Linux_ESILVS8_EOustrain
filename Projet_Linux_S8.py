import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import schedule
from datetime import datetime, timedelta

dfEURUSD = pd.read_csv("/home/ec2-user/prixUSD.csv",sep=',',names=['Date','Valeur'])

dfEURY = pd.read_csv("/home/ec2-user/prixYEN.csv",sep=',',names=['Date','Valeur'])

dfEURGBP = pd.read_csv("/home/ec2-user/prixGBP.csv",sep=',',names=['Date','Valeur'])

dfEURUSD2 = pd.read_csv("/home/ec2-user/prixUSD.csv",sep=',',names=['Date','Valeur'])
dfEURUSD2['Valeur'] = dfEURUSD2['Valeur'].apply(lambda x: str(x) + '$')

dfEURY2 = pd.read_csv("/home/ec2-user/prixYEN.csv",sep=',',names=['Date','Valeur'])
dfEURY2['Valeur'] = dfEURY2['Valeur'].apply(lambda x: '¥' + str(x))

dfEURGBP2 = pd.read_csv("/home/ec2-user/prixGBP.csv",sep=',',names=['Date','Valeur'])
dfEURGBP2['Valeur'] = dfEURGBP2['Valeur'].apply(lambda x: '£' + str(x))

current_date = datetime.now().date()

dfEURUSD3 = pd.read_csv("/home/ec2-user/prixUSD.csv",sep=',',names=['Date','Valeur'])
dfEURUSD3['Date'] = pd.to_datetime(dfEURUSD3['Date'])
dfEURUSD_today = dfEURUSD3[dfEURUSD3['Date'].dt.date == current_date]

MoyEURUSD = round(np.mean(dfEURUSD['Valeur']),4)
MaxEURUSD = round(max(dfEURUSD['Valeur']),4)
MinEURUSD = round(min(dfEURUSD['Valeur']),4)

def update_statistics():
    mean = dfEURUSD_today['Valeur'].mean()
    std = dfEURUSD_today['Valeur'].std()
    highest = dfEURUSD_today['Valeur'].max()
    lowest = dfEURUSD_today['Valeur'].min()

    return {'Mean': mean, 'Volatility': std, 'Highest Value': highest, 'Lowest Value': lowest}

schedule.every().day.at("20:00").do(update_statistics)

def style_cell(value):
    if value == MaxEURUSD:
        return {'backgroundColor': 'green', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid black'}
    elif value == MinEURUSD:
        return {'backgroundColor': 'red', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid black'}
    elif value == MoyEURUSD:
        return {'backgroundColor': 'blue', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid black'}





table = html.Table(
    [html.Tr([html.Th('MoyEURUSD'), html.Th('MaxEURUSD'), html.Th('MinEURUSD')]),
     html.Tr([html.Td((MoyEURUSD),style =style_cell(MoyEURUSD)), html.Td((MaxEURUSD),style =style_cell(MaxEURUSD)), html.Td((MinEURUSD),style =style_cell(MinEURUSD))])]
)

table_style = {'marginLeft': 'center', 'marginRight': 'center', 'textAlign': 'left'}

app = dash.Dash()

fig1 = go.Figure(data=go.Scatter(x=dfEURUSD['Date'], y=dfEURUSD['Valeur'], mode='lines'))

fig1.update_layout(
    title="Évolution du taux de change EUR/USD",
    xaxis_title="Date",
    yaxis_title="Taux de change EUR/USD en $",
    template='plotly_dark',
    yaxis=dict(ticksuffix='$'),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=12, label="12h", step="hour", stepmode="backward"),
                dict(count=1, label="1j", step="day", stepmode="backward"),
                dict(count=5, label="5j", step="day", stepmode="backward"),
                dict(count=15, label="15j", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

app.layout = html.Div(
    
    
    children=[html.H1(
        children='Évolution du taux de change EUR/USD',style ={'textAlign':'center', 'color':'#FFD700'
                                                                    ,'font-family':'Bodoni MT'}),
    

    dcc.Graph(
        id='example-graph',
        figure=fig1,
        style ={'width': 800, 'height' :400, 'float': 'right', 'marginLeft' : '50px'}
    ),
    html.Div(
        style={
        'border': '2px solid gray',
        'padding': '10px',
        'border-radius': '5px',
        'font-family': 'Bodoni MT',
        'max-width' : '600px'
    },
    children=[
        html.H3('Quelques comparaisons avec d\'autres valeurs de change de l\'Euro'),
        html.P(f'EURUSD : {dfEURUSD2.iloc[-1]["Date"]} - {dfEURUSD2.iloc[-1]["Valeur"]}'),
        html.P(f'EURJPY : {dfEURY2.iloc[-1]["Date"]} - {dfEURY2.iloc[-1]["Valeur"]}'),
        html.P(f'EURGBP : {dfEURGBP2.iloc[-1]["Date"]} - {dfEURGBP2.iloc[-1]["Valeur"]}')
    ]),
    html.Div(children=[table]),
    html.Div(children=[
        html.H2('Stock Statistics'),
        html.Table(id='stats-table', children=[
            html.Tr([html.Td(stat), html.Td(id=stat)]) for stat in update_statistics().keys()
        ])
    ])
             
    

])


current_time = datetime.now()

next_time = current_time + timedelta(seconds=1)

while datetime.now() < next_time:
    pass

schedule.run_pending()

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8050, debug=True)
