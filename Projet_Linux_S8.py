import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import schedule
from datetime import datetime, timedelta, time

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
    date_actuelle = datetime.now()
    date_actuelle_str = date_actuelle.date().strftime('%Y-%m-%d')
    statistiques = html.Div(
        style={
        'border': '2px solid gray',
        'padding': '10px',
        'border-radius': '5px',
        'font-family': 'Bodoni MT',
        'max-width' : '50vh'
    },
    children=[
        html.H3('Statistiques de la journée du : '+date_actuelle_str),
        html.P(f'Volatilité : {std}'),
        html.P(f'Valeur la plus élevée : {highest}'),
        html.P(f'Valeur la plus basse : {lowest}'),
        html.P(f'Moyenne de la journée : {mean}')
    ])
    return statistiques



def get_table():
    now = datetime.now() 
    today_at_8pm = datetime.combine(now.date(), time(hour=20)) 
    if now.hour >= today_at_8pm.hour:  
        return update_statistics()        


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

table_style = {'marginLeft': '50px', 'marginRight': 'center', 'textAlign': 'left', 'margin-top' : '10px'}

app = dash.Dash()

fig1 = go.Figure(data=go.Scatter(x=dfEURUSD['Date'], y=dfEURUSD['Valeur'], mode='lines'))

fig1.update_layout(
    title="Évolution du taux de change EUR/USD",
    xaxis_title="Date (Vous pouvez modifier la plage de dates des données en cliquant sur les boutons situés sur le graphique)",
    yaxis_title="Taux de change EUR/USD en $",
    template='plotly_white',
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
                dict(step="all")
            ]),
            bgcolor="navy",
            activecolor ="grey",
            font=dict(
                color="white"
            )
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

app.layout = html.Div(
    
    
    children=[html.H1(
        children='Évolution du taux de change EUR/USD',style ={'textAlign':'center', 'color': 'navy'
                                                                    ,'font-family':'Bodoni MT'}),
    

    dcc.Graph(
        id='example-graph',
        figure=fig1,
        style ={'width': '60%', 'height' : '70vh', 'float': 'right', 'marginLeft' : '50px'}
    ),
    html.Div(
        style={
        'border': '2px solid gray',
        'padding': '10px',
        'border-radius': '5px',
        'font-family': 'Bodoni MT',
        'max-width' : '50vh'
    },
    children=[
        html.H3('Quelques comparaisons avec d\'autres valeurs de change de l\'Euro'),
        html.P(f'EURUSD : {dfEURUSD2.iloc[-1]["Date"]} - {dfEURUSD2.iloc[-1]["Valeur"]}'),
        html.P(f'EURJPY : {dfEURY2.iloc[-1]["Date"]} - {dfEURY2.iloc[-1]["Valeur"]}'),
        html.P(f'EURGBP : {dfEURGBP2.iloc[-1]["Date"]} - {dfEURGBP2.iloc[-1]["Valeur"]}')
    ]),
    html.Div(children=[table]),
    html.Div(children=get_table())
             
    

])



if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8050, debug=True)
