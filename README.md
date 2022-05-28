# CardiovascularHealthDashboard
The Cardiovascular Health Dashboard is an informative and interactive platform for learning and understanding about heart health. The platform contains visualizations of cardiovascular health correlates and provides resources on lifestyle choices that may lower the risk of cardiovascular-related health issues. 

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

## Testing
To test the program, navigate to the root of the repository and run the following:
```bash
pytest -v
```
Where the optional `-v` flag will provide information about individual tests.

To view the code coverage report, navigate to the root of the repository run the following:
```bash
coverage report
```