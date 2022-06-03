from dash import Dash, html, dcc, Input, Output,callback
import plotly.express as px
import pandas as pd
import itertools
from urllib.request import urlopen
import json
import plotly.graph_objects as go
from sklearn.feature_selection import SelectKBest, chi2

app = Dash(__name__)
##################################1
CATEGORICAL_COLUMNS = ['gender', 'cholesterol', 'smoke', 'alco', 'active']
def get_categorical_table()-> pd.DataFrame:
    """Returns a section of the table with categorical variables only
    Returns
    -------
    pandas.DataFrame
    """
    # read the kaggle dataset
    df = pd.read_csv('../../data/kaggle_cleaned.csv')
    return df[[*CATEGORICAL_COLUMNS, 'cardio']]

df = get_categorical_table()

def get_dropdown_options():
    """Returns all the varibles to populate the dropdown
    Returns
    -------
    list(str)
    """
    return CATEGORICAL_COLUMNS

def compute_importance(x_vars) -> list:
    """Computes the importance score using the chi-squared statistic
    Input
    -------
    x_vars : list of fields for which the importance is computed
    y : Dependent variable
    Returns
    -------
    list: importance scores for each x with respect to y
    """
    #assert isinstance(x_vars, list)
    #assert all([(isinstance(x, str) and x in df.columns) for x in x_vars])
    if x_vars!=None:
        x_df = df[[*x_vars]]
        y_ds = df['cardio']

        fs = SelectKBest(score_func=chi2, k='all')
        fs.fit(x_df, y_ds)
        return fs.scores_
   

    




############################################2
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
#print(data.drop('cardio').index.tolist())
#This only uses the columns ['smoke', 'gender', 'alco', 'active', 'cardio'] from the kaggle_cleaned.csv

#data
dataset1=pd.read_csv("../../data/Kagglecleaned3.csv")
dataset1.loc[dataset1['cardio']==0,'cardio'] = 'No CVD'
dataset1.loc[dataset1['cardio']==1,'cardio'] = 'CVD patient'
dataset1.rename(columns = {'ap_hi':'systolic pressure', 'ap_lo':'diastolic pressure'}, inplace = True)
dataset1.loc[dataset1['active']==0,'active'] = 'Exercise Regularily'
dataset1.loc[dataset1['active']==1,'active'] = 'Lack of Exercise'

dataset2 = pd.read_csv('../../data/kaggle_cleaned.csv') #for easy use
dataset2.loc[dataset2['cardio']==0,'cardio'] = 'No CVD'
dataset2.loc[dataset2['cardio']==1,'cardio'] = 'CVD patient'
dataset2.loc[dataset2['cholesterol']==1,'cholesterol'] = 'Normal (<200mg/dL)'
dataset2.loc[dataset2['cholesterol']==2,'cholesterol'] = 'Above Normal (200~239mg/dL)'
dataset2.loc[dataset2['cholesterol']==3,'cholesterol'] = 'Well Above Normal (>240mg/dL)'
dataset2.loc[dataset2['gluc']==1,'gluc'] = 'Normal (<99mg/dL)'
dataset2.loc[dataset2['gluc']==2,'gluc'] = 'Above Normal (100~125mg/dL)'
dataset2.loc[dataset2['gluc']==3,'gluc'] = 'Well Above Normal (>126mg/dL)'
dataset2.rename(columns = {'gluc':'Glucose Level'}, inplace = True)

#figure for high blood pressure
fig1 = px.box(dataset1, y = 'systolic pressure', x='cardio', color='cardio') 
fig2 = px.box(dataset1, y = 'diastolic pressure', x='cardio', color='cardio')

#figure for Smoking (data from heart_2020_cleaned.csv, the other dataset does not show significant relationship on smoking, weird)
fig3 = go.Figure(data=[go.Table(header=dict(values=['','CVD patient', 'No CVD']),
                 cells=dict(values=[['Smoker', 'Non-Smoker'],[16037, 11336], [115871, 176551]]))])

#figure for cholesterol
fig4 = px.histogram(dataset2, x='cardio', color="cholesterol", barmode='group')

#fig for high glucolse
fig5 = px.histogram(dataset2, x='cardio', color="Glucose Level", barmode='group')
#fig for Inactivity
fig6 = px.histogram(dataset1, x='cardio', color="active", barmode='group')
#fig for Obsease
dataset1['BMI'] = dataset1['weight']/(dataset1['height']**2)*10000
dataset1 = dataset1[dataset1['BMI']<50]
fig7 = px.box(dataset1, y = 'BMI', x='cardio', color='cardio')


risk_suggestions = {
    'High blood Pressure':html.Div(children=[
                                     html.Div(className='graphs',children=[dcc.Graph(figure=fig1),
                                                        dcc.Graph(figure=fig2)]),
        
                                    html.Div(className='writings',children=[
                                                html.P(['''High blood pressure (hypertension) is one of the most 
                                                important risk factors for Cardiovascular disease. The ideal blood 
                                                pressure is usually considered to be between 90/60mmHg and 120/80mmHg.
                                                Blood pressure readings between 120/80mmHg and 140/90mmHg could mean 
                                                you're at risk of developing high blood pressure if you do not take 
                                                steps to keep your blood pressure under control. ''']),
                                                html.P(['These lifestyle changes can help prevent and lower high blood pressure:',html.Br(),
                                                '· reduce the amount of salt you eat and have a generally healthy diet',html.Br(),
                                                "· exercise regularly",html.Br(),
                                                "· cut down on caffeine",html.Br()]),
       ]),                            
    ]),
    'Smoking':html.Div(children=[   html.Div(dcc.Graph(figure=fig3),className='graphs'),


                                    html.Div(className='writings',children=[
                                                html.P(['''Smoking and other tobacco use is also a significant 
                                                risk factor for CVD. The harmful substances in tobacco can damage
                                                and narrow your blood vessels. If you smoke, you should try to give
                                                up as soon as possible.''']),
                                                
                                                html.P(['Odds-ratio = 2.16. Smoking siginificantly increases the probability of getting a heart disease.']),
                                        ]),
                                ]),
    'High Cholesterol':html.Div(children=[
                                            html.Div(dcc.Graph(figure=fig4),className='graphs'),


                                            html.Div(className='writings',children=[html.P(['''Cholesterol is a fatty substance found in the blood. 
                                            It's mainly caused by eating fatty food, not exercising enough, 
                                            being overweight, smoking and drinking alcohol. It can also run 
                                            in families.Too much cholesterol can block your blood vessels. 
                                            It makes you more likely to have heart problems or a stroke. 
                                            You can lower your cholesterol by eating healthily and getting more exercise. 
                                            Some people also need to take medicine.''']),])
                                
                            ]),
    'Diabetes':html.Div(children=[      html.Div(dcc.Graph(figure=fig5),className='graphs'),

                                        html.Div(className='writings',children=[html.P(['''Diabetes is a lifelong condition that causes your blood sugar level to become too high. 
                                        High blood sugar levels can damage the blood vessels, making them more likely to become narrowed.
                                        If you're diagnosed with diabetes, you'll need to eat healthily, take regular exercise and carry 
                                        out regular blood tests to ensure your blood glucose levels stay balanced.''']),
                                        html.Br(),
                                        html.P(['''People diagnosed with type 1 diabetes also require regular insulin injections for the 
                                        rest of their life. As type 2 diabetes is a progressive condition, medicine may eventually be required, 
                                        usually in the form of tablets.''']),
                                        ])
                                    ]),
    'Inactivity':html.Div(children=[    html.Div(dcc.Graph(figure=fig6),className='graphs'),
                                        html.Div(className='writings',children=[ html.P(['''If you don't exercise regularly, it's more likely that you'll have high blood pressure, 
                                                high cholesterol levels and be overweight. All of these are risk factors for CVD. Exercising regularly 
                                                will help keep your heart healthy. When combined with a healthy diet, exercise can also help you maintain 
                                                a healthy weight.
                                                '''])
                                            ]),
                            
                        ]),
    'Obese':html.Div(children=[ html.Div(dcc.Graph(figure=fig7),className='graphs'),
                                html.Div(className='writings',children=[html.P(['The best way to treat obesity is to eat a healthy reduced-calorie diet and exercise regularly.',html.Br(),
                                    'To do this, you should:',html.Br(),
                                    '·Eat a balanced calorie-controlled diet as recommended by a GP or weight loss management health professional (such as a dietitian) join a local weight loss group',html.Br(),
                                    '·Take up activities such as fast walking, jogging, swimming or tennis for 150 to 300 minutes (2.5 to 5 hours) a week.',html.Br(),
                                    '·Eat slowly and avoid situations where you know you could be tempted to overeat',html.Br(),
                                    '·You may also benefit from receiving psychological support from a trained healthcare professional to help change the way you think about food and eating.',html.Br(),
                                    html.Br(),
                                    'If lifestyle changes alone do not help you lose weight, a medicine called orlistat may be recommended.'
                                    ]),
                                ])
        
    ]),
    
}


#3





layout = html.Div(children=[

                    html.Div(style={ 'display': 'inline-flex'},
                        children=[  dcc.Link(html.Button("Risk Factor Analysis",style={'width': '230%','margin-left': '0%','background': 'rgb(0,255,156)','opacity': '70%'}), href="/page2"),
                                    dcc.Link(html.Button("Location Visualizations",style={'width': '189%','margin-left': '116%','background': 'rgb(0,255,156)','opacity': '70%'}), href="/page4"),]),
                        
                    #1
                    html.Div([
                                dcc.Dropdown(
                                    id="risk_factors",
                                    options=[
                                        {"label": l.capitalize(), "value": l}
                                        for l in risk_suggestions.keys()
                                    ],
                                    value='High blood Pressure'
                                    ),
                                    
                                    html.Div(id = 'suggestions')
                                ]),
                    #2
                    html.Div(children=[
                                    html.Label('Select Risk Factors'),
                                    dcc.Dropdown(get_dropdown_options(),
                                                    multi=True,
                                                    id='corr-factors',
                                                ),
                                html.Div(dcc.Graph(
                                        id='corr-plot',
                                    ),className="graphs"),
                                html.Div(html.P("Write something"),className="writings")
                                    
                                ]),
                    
                    
                    #3
                   
                    #4
                    


                    
                
                ])
#1
@callback(
    Output('corr-plot', 'figure'),
     Input('corr-factors', 'value')
 )
def correlation_plot(cols):
    """Correlation between the selected factors and cardiovascular disease risk.
     """
   
    return px.bar(x=cols, y=compute_importance(cols), title='Correlation',
         labels={'x': 'Risk Factors', 'y':'Correlation'}, width=500)

#2
@callback(
    Output('suggestions','children'),
    Input('risk_factors', 'value')
)
def give_suggestions(factors):
    return risk_suggestions[factors]




#4




if __name__ == '__main__':
    app.layout=layout
    app.run_server(debug=True)