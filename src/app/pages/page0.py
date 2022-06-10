from dash import dcc, html, callback


yes_no_options = ['Yes', 'No']
layout = html.Div(
    children=[
        html.Div(
            className='HeartBeat',
            children=[
                html.P(
                    'CAN YOU PROVIDE HIGH BP, LOW BP,CHOLESTEROL AND GLUCOSE LEVEL VALUES?',
                    style={
                        'text-align': 'center',
                        'color': '#555',
                        'font-size': 'x-large'
                    }
                ),
                html.Div(
                    children=dcc.Link(
                        html.Button(
                            'Yes',
                            style={
                                'margin-bottom': '2rem',
                                'width': '30%',
                                'margin-left': '34%'
                            }
                        ),
                        href='/page3'
                    ),
                ),
                html.Div(
                    dcc.Link(
                        html.Button(
                            'No',
                            style={
                                'margin-bottom': '2rem',
                                'width': '30%',
                                'margin-left': '34%'
                            }
                        ),
                        href='/page1'
                    )
                ),
                html.P(
                    'Provision of all information is completely voluntary. If you wish to keep the detailed information private, please use the general model. We do not share or store your data at any point.',
                    style={
                        'top': ' 110%',
                        'position': ' absolute',
                        'text-align': 'center'
                    }
                )
            ]
        )
    ]
)
