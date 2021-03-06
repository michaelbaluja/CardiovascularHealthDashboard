from dash import dcc, html

from .defaults import gender_options, yes_no_option_exercise, yes_no_options


def user_input_template(
        cn: str,
        p_text: str,
        **dropdown_kwargs: dict
) -> html.Div:
    """Template for user input field.

    Parameters
    ----------
    cn : str
        className for html.Div object.
    p_text : str
        Input paragraph text.

    Returns
    -------
    html.Div
        Element containing paragraph titling and input field.
    """

    return html.Div(
        className=cn,
        children=[
            html.P(p_text),
            dcc.Input(**dropdown_kwargs)
        ]
    )


def user_dropdown_template(
        cn: str,
        p_text: str,
        **dropdown_kwargs: dict
) -> html.Div:
    """Template for user input dropdown.

    Parameters
    ----------
    cn : str
        className for html.Div object.
    p_text : str
        Input paragraph text.

    Returns
    -------
    html.Div
        Element containing paragraph titling and input dropdown.
    """

    return html.Div(
        className=cn,
        children=[
            html.P(p_text),
            dcc.Dropdown(**dropdown_kwargs)
        ]
    )


def user_age(div_className: str) -> html.Div:
    """Input section for age.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_input_template
    """

    return user_input_template(
        div_className,
        'Age',
        className='app-input',
        id='age',
        type='number',
        min=18,
        step=1
    )


def user_gender(div_className: str) -> html.Div:
    """Dropdown selection for gender.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_dropdown_template
    """

    return user_dropdown_template(
        div_className,
        'Gender',
        id='genderdrop',
        options=gender_options,
    )


def user_height(div_className: str) -> html.Div:
    """Input section for height.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_input_template
    """

    return user_input_template(
        div_className,
        'Height (Inches)',
        className='app-input',
        id='height',
        type='number',
        min=0,
        step=1
    )


def user_weight(div_className: str) -> html.Div:
    """Input section for weight.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_input_template
    """

    return user_input_template(
        div_className,
        'Weight (Pounds)',
        className='app-input',
        id='weight',
        type='number',
        min=0,
        step=1
    )


def user_smoke(div_className: str) -> html.Div:
    """Dropdown selection for smoking status.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_dropdown_template
    """

    return user_dropdown_template(
        div_className,
        'Do you smoke?',
        id='smoke',
        options=yes_no_options
    )


def user_drink(div_className: str) -> html.Div:
    """Dropdown selection for drinkning status.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_dropdown_template
    """

    return user_dropdown_template(
        div_className,
        'Do you drink?',
        id='drink',
        options=yes_no_options
    )


def user_exercise(div_className: str) -> html.Div:
    """Dropdown selection for activity status.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_download_template
    """

    return user_dropdown_template(
        div_className,
        'Do you exercise regularly?',
        id='exercise',
        options=yes_no_option_exercise
    )


def user_low_bp(div_className: str) -> html.Div:
    """Input section for low blood pressure level.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_input_template
    """

    return user_input_template(
        div_className,
        'Low BP level',
        className='app-input',
        id='lowbp',
        type='number',
        min=20,
        step=1
    )


def user_high_bp(div_className: str) -> html.Div:
    """Input section for high blood pressure level.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_input_template
    """

    return user_input_template(
        div_className,
        'High BP level',
        className='app-input',
        id='highbp',
        type='number',
        min=50,
        step=1
    )


def user_cholesterol(div_className: str) -> html.Div:
    """Dropdown selection for cholesterol level.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_download_template
    """

    return user_dropdown_template(
        div_className,
        'Cholesterol level',
        id='cholesterol',
        options=[
            'Normal(<200mg/dL)',
            'Above Normal(200~239mg/dL)',
            'Abnormal(>240mg/dL)'
        ]
    )


def user_glucose(div_className: str) -> html.Div:
    """Dropdown selection for glucose level.

    Parameters
    ----------
    div_className : str
        className attribute of template Div.

    Returns
    -------
    html.Div

    See Also
    --------
    user_dropdown_template
    """

    return user_dropdown_template(
        div_className,
        'Glucose level',
        className='app-input',
        id='glucose',
        options=[
            'Normal(<99mg/dL)',
            'Above Normal(100~125mg/dL)',
            'Abnormal (>126mg/dL)'
        ]
    )
