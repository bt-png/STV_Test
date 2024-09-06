# Import Python standard packages from PyPi [https://pypi.org/]
# If you need to reference in any other standard packages, import them here.
# Added packages should also be added to the 'requirements.txt'
# Use command line 'pip install -r requirements.txt' to install into your virtual environment
import streamlit as st
import numpy as np
import pandas as pd

# Import local *.py files as reference modules to be utilized in the calculation
import units  # units.py: No changes to units.py will be accepted, unless use case is fully justified.
from plot import plot  # plot.py: No changes to plot.py will be accepted, unless use case is fully justified.
# import formulas  # formulas.py: For this simple 'SingleCalc' we will be writing the information directly on this page.


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# This is the section your looking for to update your calculation.
# -----------------------------------------------------------------------------------------------------------
# Python will read in this section line by line and perform the action
# The order in which you arrange will directly correlate to what is printed to the webapp
# The calculation header, description, assumptions, etc. have already been loaded in at this point
# from within the 'information.md' file.

# The script is setup to start in the ```run``` procedure. However, we will first create our own procedures that we will use in our calculation.
# In the ```MultiCalc``` example, these would be contained within their associated class objects within the formulas module.
def markdown():
    md = """
    The formula for wire resistance is:

    $R_{wire} = 2 \cdot L_{wire} \cdot R_{length}$
    
    The formula for voltage at the load is:

    $V_{load} = V_{source} - I_{wire} \cdot R_{wire}$
    """
    return md


def voltage_at_load(input_voltage, resistance, current):
    """
    Calculate the voltage at the load after the voltage drop across the wire.
    
    :param input_voltage: Voltage at the source (in volts)
    :param resistance: Total resistance of the wire (in ohms)
    :param current: Current flowing through the wire (in amperes)
    
    :return: Voltage at the load (in volts)
    """
    # Calculate the voltage drop (Ohm's Law: V_drop = I * R)
    voltage_drop = current * resistance
    
    # Calculate the voltage at the load
    voltage_at_load = input_voltage - voltage_drop
    
    return voltage_at_load

def parse_csv(file_path):
    """
    Parses a CSV file containing wire resistance data into a pandas DataFrame.
    Assumes the first line of the CSV contains column headers.
    
    :param file_path: Path to the CSV file (default is 'wire_resistance.csv')
    :return: A pandas DataFrame with the inferred column names from the file
    """
    try:
        # Read the CSV file, letting pandas infer the column names from the first row
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an issue parsing the file.")

def return_max(_list):
    _min = min(_list)
    _max = max(_list)
    return _max if abs(_max) > abs(_min) else _min


# Now that we have all the functions setup we intend to utilize, lets look into how we want the input/results rendered on the website.
# For this, we are utilizing streamlit.
def run():
    # Input Data Caption
    st.markdown('### Input')

    # Section Header for input Data
    st.markdown('##### Source Inputs')
    def_sourceDC = units.load('24 volts')
    source_voltage = units.input('Source DC', def_sourceDC, minor=False)

    st.markdown('##### Load Inputs')
    def_loadAmps = units.load('2 A')
    load_current = units.input('Current Draw', def_loadAmps, minor=False)
    
    # Section Header for input Data
    st.markdown('##### Wire Inputs')
    
    # Load the wire characteristics into a dataframe
    wire_df = parse_csv('wire_resistance.csv')

    # Create a dropdown (selectbox) using Streamlit
    selected_awg = st.selectbox(
        'Select the wire gauge size:', 
        wire_df['awg'],
        index=10
    )

    # Filter the DataFrame to get the row where 'awg' equals the selected_awg
    selected_row = wire_df[wire_df['awg'] == selected_awg]
    # Extract the 'r_25c' value for the selected AWG
    wire_resistivity = units.load(str(selected_row['r_25c'].values[0]) + ' ohm/kft')

    wire_length = units.input('Length of wire', '300 ft', minor=False)
    
    total_resistance = 2 * wire_length * wire_resistivity / units.load('1000 ft/kft')
    st.caption(f'Wire Resistance = {units.unitdisplay(total_resistance, minor=False)}') 

    # Section Header for Results
    st.markdown('### Results')

    # Lets present the formulas we want to utilize using markdown notation.
    # Visit 'https://www.upyesp.org/posts/makrdown-vscode-math-notation/' for information
    st.markdown(markdown())

    # We can provide a visual break in the data through a hard line, created by 'st.markdown('---')'
    st.markdown('---')
    
    load_voltage = voltage_at_load(source_voltage, total_resistance, load_current)
    st.text(f'Voltage at load = {units.unitdisplay(load_voltage, minor=False)}')
    # The syntax [do_something_to x for x in xlist], iterates over the xlist,
    # pulling out a single value assigned as x, and does something to it
    # if called for "beam.deflection('12ft')" then we would get a single result for the deflection at '12ft'
    # by iterating over the full list of 'x', assigned above, we can get a list of corresponding values
    # Notice here that we have to be careful not to assign our variable name the same as our function name.
    #deflection = [calcDeflection(F=load, E=modulus, I=inertia, a=distance, x=_x).to_base_units() for _x in x]

    # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
    # The plot size, unit display, interactivity, and tooltip is handled within this function
    # If you compare the "SingleCalc" to the "MultiCalc", you will notice that by using the Class object, we only need
    # to define the input variables once. Since the object stores the data, we then can simply just call out the methods we want to utilize.
    # However, in this example we need to provide the variables each time.
    #plot('Beam Deflection', 'x', 'y', x, deflection, False, True)
    #maxd = maxDeflection(F=load, L=length, E=modulus, I=inertia, a=distance)

    # We can utilize the 'caption' function from streamlit (st) to display information
    #st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    #st.markdown('---')
    #shear = [calcShear(F=load, a=distance, x=_x).to_base_units() for _x in x]
    #plot('Beam Shear', 'x', 'y', x, shear, False, True)
    #maxshear = return_max(shear)
    #st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    #st.markdown('---')
    #moment = [calcMoment(F=load, a=distance, x=_x).to_base_units() for _x in x]
    #plot('Beam Moment', 'x', 'y', x, moment, False, False)
    #maxmoment = return_max(moment)
    #st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment)}')


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------


# Don't revise. Changes to your calculation title and instructions should be made within the 'information.md' file.
def setup():
    # This is where the markdown information for the calculation title, description, etc is loaded in.
    with open('information.md', 'r') as f:
        header = f.read()
    st.write(header)
    run()


# Don't revise. Run setup() if this file is the entry
if __name__ == '__main__':
    st.set_page_config(
        page_title='STV_Test Calculation Set',
        layout='wide'
    )
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        setup()
