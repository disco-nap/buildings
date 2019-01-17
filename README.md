# ARIMA Time Series Analysis for Energy Demand Forcasting

by Christina Vavoulis and Julia Napolitano

### Definitions from US Energy Information Administration (EIA)
#### Primary energy
Energy in the form that it is first accounted for in a statistical energy balance, before any transformation to secondary or tertiary forms of energy. For example, coal can be converted to synthetic gas, which can be converted to electricity; in this example, coal is primary energy, synthetic gas is secondary energy, and electricity is tertiary energy. See Primary energy production and Primary energy consumption.
#### Primary energy consumption 
Consumption of primary energy. 
#### Primary energy production
Production of primary energy. 
#### Primary fuels
Fuels that can be used continuously. They can sustain the boiler sufficiently for the production of electricity.
##### source: https://www.eia.gov/opendata/qb.php?category=0
----------------------------------------------------------------------

This particular study analyzes the US total primary energy consumption. The script will work for predicitions of many different datasets within the EIA databases, including:
- List 
- EIA
- Series endings
- Here
- CA monthly generation:
     - series_id = ELEC.GEN.ALL-CA-99.M
     
### In command line interface
- pip install EIA-python
- pip install numpy
- pip install pandas
- pip install requests
