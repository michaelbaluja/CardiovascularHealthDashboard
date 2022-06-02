
import pandas as pd
from dash.dependencies import Input, Output
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
app = Dash(__name__)

#data
dataset1=pd.read_csv("datasets/Kagglecleaned3.csv")
dataset1.loc[dataset1['cardio']==0,'cardio'] = 'No CVD'
dataset1.loc[dataset1['cardio']==1,'cardio'] = 'CVD patient'

dataset2 = pd.read_csv('datasets/kaggle_cleaned.csv') #for easy use
dataset2.loc[dataset2['cardio']==0,'cardio'] = 'No CVD'
dataset2.loc[dataset2['cardio']==1,'cardio'] = 'CVD patient'
dataset2.loc[dataset2['cholesterol']==1,'cholesterol'] = 'Normal'
dataset2.loc[dataset2['cholesterol']==2,'cholesterol'] = 'Above Normal'
dataset2.loc[dataset2['cholesterol']==3,'cholesterol'] = 'Well Above Normal'
dataset2.loc[dataset2['gluc']==1,'gluc'] = 'Normal'
dataset2.loc[dataset2['gluc']==2,'gluc'] = 'Above Normal'
dataset2.loc[dataset2['gluc']==3,'gluc'] = 'Well Above Normal'

#figure for high blood pressure
fig1 = px.box(dataset1, y = 'ap_hi', x='cardio', color='cardio') 
fig2 = px.box(dataset1, y = 'ap_lo', x='cardio', color='cardio')

#figure for Smoking (data from heart_2020_cleaned.csv, the other dataset does not show significant relationship on smoking, weird)
fig3 = go.Figure(data=[go.Table(header=dict(values=['','CVD patient', 'No CVD']),
                 cells=dict(values=[['Smoker', 'Non-Smoker'],[16037, 11336], [115871, 176551]]))])

#figure for cholesterol
fig4 = px.histogram(dataset2, x='cardio', color="cholesterol", barmode='group')

#fig for high glucolse
fig5 = px.histogram(dataset2, x='cardio', color="gluc", barmode='group')
#fig for Inactivity
fig6 = px.histogram(dataset1, x='cardio', color="active", barmode='group')
#fig for Obsease
dataset1['BMI'] = dataset1['weight']/(dataset1['height']**2)*10000
dataset1 = dataset1[dataset1['BMI']<50]
fig7 = px.box(dataset1, y = 'BMI', x='cardio', color='cardio')

risk_suggestions = {
    'High blood Pressure':html.Div([
        html.P(['''High blood pressure (hypertension) is one of the most 
        important risk factors for Cardiovascular disease. The ideal blood 
        pressure is usually considered to be between 90/60mmHg and 120/80mmHg.
        Blood pressure readings between 120/80mmHg and 140/90mmHg could mean 
        you're at risk of developing high blood pressure if you do not take 
        steps to keep your blood pressure under control. ''']),
        html.P(['These lifestyle changes can help prevent and lower high blood pressure:',html.Br(),
        '· reduce the amount of salt you eat and have a generally healthy diet',html.Br(),
        "· exercise regularly",html.Br(),
        "· cut down on caffeine",html.Br(),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
        ]),
    ]),
    'Smoking':html.Div([
        html.P(['''Smoking and other tobacco use is also a significant 
        risk factor for CVD. The harmful substances in tobacco can damage
        and narrow your blood vessels. If you smoke, you should try to give
        up as soon as possible.''']),
        dcc.Graph(figure=fig3),
        html.P(['Odds-ratio = 2.16. Smoking siginificantly increases the probability of getting a heart disease.']),
    ]),
    'High Cholesterol':html.Div([
        html.P(['''Cholesterol is a fatty substance found in the blood. 
        It's mainly caused by eating fatty food, not exercising enough, 
        being overweight, smoking and drinking alcohol. It can also run 
        in families.Too much cholesterol can block your blood vessels. 
        It makes you more likely to have heart problems or a stroke. 
        You can lower your cholesterol by eating healthily and getting more exercise. 
        Some people also need to take medicine.''']),
        dcc.Graph(figure=fig4)
    ]),
    'Diabetes':html.Div([
        html.P(['''Diabetes is a lifelong condition that causes your blood sugar level to become too high. 
        High blood sugar levels can damage the blood vessels, making them more likely to become narrowed.
        If you're diagnosed with diabetes, you'll need to eat healthily, take regular exercise and carry 
        out regular blood tests to ensure your blood glucose levels stay balanced.''']),
        html.Br(),
        html.P(['''People diagnosed with type 1 diabetes also require regular insulin injections for the 
        rest of their life. As type 2 diabetes is a progressive condition, medicine may eventually be required, 
        usually in the form of tablets.''']),
        dcc.Graph(figure=fig5)
    ]),
    'Inactivity':html.Div([
        html.P(['''If you don't exercise regularly, it's more likely that you'll have high blood pressure, 
    high cholesterol levels and be overweight. All of these are risk factors for CVD. Exercising regularly 
    will help keep your heart healthy. When combined with a healthy diet, exercise can also help you maintain 
    a healthy weight.
    ''']),
        dcc.Graph(figure=fig6)
    ]),
    'Obsease':html.Div([
        html.P(['The best way to treat obesity is to eat a healthy reduced-calorie diet and exercise regularly.',html.Br(),
        'To do this, you should:',html.Br(),
        '·Eat a balanced calorie-controlled diet as recommended by a GP or weight loss management health professional (such as a dietitian) join a local weight loss group',html.Br(),
        '·Take up activities such as fast walking, jogging, swimming or tennis for 150 to 300 minutes (2.5 to 5 hours) a week.',html.Br(),
        '·Eat slowly and avoid situations where you know you could be tempted to overeat',html.Br(),
        '·You may also benefit from receiving psychological support from a trained healthcare professional to help change the way you think about food and eating.',html.Br(),
        html.Br(),
        'If lifestyle changes alone do not help you lose weight, a medicine called orlistat may be recommended.'
        ]),
        dcc.Graph(figure=fig7)
    ]),
    'Alcohol':html.Div([
        html.P(['''
        Excessive alcohol consumption can also increase your cholesterol and blood pressure levels, 
        and contribute to weight gain. 
        ''']) #no figure for alcohol drinking
    ])
}

app.layout = html.Div([
    dcc.Checklist(
        id="risk_factors",
        options=[
            {"label": l.capitalize(), "value": l}
            for l in risk_suggestions.keys()
        ],
        value=[]
    ),
    html.Br(),
    html.Div(id = 'suggestions')
])

@app.callback(
    Output('suggestions','children'),
    Input('risk_factors', 'value')
)
def give_suggestions(factors):
    suggestions = []
    if len(factors)==0:
        suggestions.append("Your condition is perfect! (This cannot be used as medical advice)")
        return suggestions
    for i in factors:
        suggestions.append(risk_suggestions[i])
    return html.Div(suggestions)

    

if __name__ == '__main__': 
    app.run_server(debug=True)