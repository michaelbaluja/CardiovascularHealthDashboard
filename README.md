# CardiovascularHealthDashboard
The Cardiovascular Health Dashboard is an informative and interactive platform for learning and understanding about heart health. The platform contains visualizations of cardiovascular health correlates and provides resources on lifestyle choices that may lower the risk of cardiovascular-related health issues. 

Link to the dashboard - http://34.221.35.212:8080/

**Disclaimer:** All data, links, and other information on the Cardiovascular Health 
Dashboard are compiled from external sources. This is not medical advice. 
Consult a healthcare professional before incorporating any changes into your
lifestyle or habits.

## Installation and use
### Installation
To install the dashboard code, run the following in your terminal
```bash
git clone https://github.com/michaelbaluja/CardiovascularHealthDashboard.git
cd CardiovascularHealthDashboard
```
It's recommended to set up a Python virtual environment for installing the dependencies needed for this project, which can be done with the following:
```bash
python -m venv cardiovasculardashboard
source cardiovasculardashboard/bin/activate
```
Then the required modules can be installed via:
```bash
pip install -r requirements.txt
```

### Use
To launch the dashboard application, launch the `app.py` file from the root directory.
The application includes a `--debug` argument for running the application in debug mode.
```bash
python app.py # for running without debug mode
python app.py --debug # for running in debug mode
```

The application will then return an IP address for the application. Simply paste
the address in your web browser to load the dashboard.

## Documentation
The full documentation for the dashboard is available on [Read the Docs](https://cardiovascular-health-dashboard.readthedocs.io/en/latest/)

## Testing
To test the program and view the coverage report, navigate to the root of the 
repository and run the following:
```bash
python -m pytest -v --cov=. --cov-report html
```