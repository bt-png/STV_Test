# Import Python standard packages from PyPi [https://pypi.org/]
# If you need to reference in any other standard packages, import them here.
# Added packages should also be added to the 'requirements.txt'
# Use command line 'pip install -r requirements.txt' to install into your virtual environment
import streamlit as st
import numpy as np


# Import local *.py files as reference modules to be utilized in the calculation
import units  # units.py: No changes to units.py will be accepted, unless use case is fully justified.
from plot import plot  # plot.py: No changes to plot.py will be accepted, unless use case is fully justified.
import formulas  # formulas.py: Revise as necessary for your numerical calculations.


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# This is the section your looking for to update your calculation.
# -----------------------------------------------------------------------------------------------------------
# Python will read in this section line by line and perform the action
# The order in which you arrange will directly correlate to what is printed to the webapp
# The calculation header, description, assumptions, etc. have already been loaded in at this point
# from within the 'information.md' file.
def run():
    # Input Data Caption
    st.markdown('### Input')

    # Section Header for input Data
    st.markdown('##### Load Inputs')

    # Numbers can be requested from the user through the 'units.input()' function
    # You can pre-define the default value, as is done in this first case
    # 'units.load()' is utlizied to pre-define a magnitude and unit
    # many common units are available to be interpreted in string format
    def_load = units.load('1200 lbf')

    # Then 'units.input()' creates the input field in the website
    # It handles displaying the title, input box, unit selector drop-down and unit conversions
    # The (minor) field is optional and defaults to False, this determines if
    # inches or feet should be selected, for example.
    load = units.input('Applied Load', def_load, minor=False)

    # You can also simply load the default unit in the same step
    distance = units.input('Distance to Load from Fixed end', '15 feet')

    # Another option to get data from the user is in tabular form, if you need multiple values of the same type.
    # For this, you can use the 'units.table_input()' function. An example string is shown below.
    # Be sure the variable declaration (left of the equals), has the same length as the lists provided for the function label, defaul, and minor inputs.
    # l, v, s = units.table_input(('Conduit Length', 'Voltage Class', 'Speed'), ('1.0 ft', '1.0 V', '12.0 mph'))
    # st.write(l)
    # st.write(v, s)

    # Section Header for input Data
    st.markdown('##### Beam Inputs')
    length = units.input('Total length of beam', '25 ft')
    modulus = units.input("Young's Modulus", '27_500_000 lbf/in**2', minor=True)
    inertia = units.input('Second Moment of Area', '209 in**4', True)

    # Section Header for Results
    st.markdown('### Results')
    # We are calling the 'CantileverIntermediateLoad' class object which is defined within the 'formulas.py' module
    # By creating a class, we then are able to directly request from it standard items.
    # This makes managing the formulas easier.
    # The inputs to the class can be seen and matched up with the '__init__' definition within
    # the class within formulas.py
    beam = formulas.CantileverIntermediateLoad(load, length, modulus, inertia, distance)

    # One of the class functions is 'def markdown():' within 'CantileverIntermediateLoad' with in 'formulas.py'
    # This presents the formulas utilized within this class in mathmatical representation
    # To better engage the end user, try to represent your equations correctly by including a markdown function
    st.markdown(beam.markdown())

    # For this example, we want to plot the beam properties over its length
    # So we use the numpy (np) 'linspace' command to create a range of values
    x = np.linspace((0*length).to_base_units(), length.to_base_units(), num=100, endpoint=True)

    # We can provide a visual break in the data through a hard line, created by 'st.markdown('---')'
    st.markdown('---')

    # We are pulling the 'deflection' from the 'CantileverIntermediateLoad' class, which we have
    # previously assigned the name 'beam'
    # The syntax [do_something_to x for x in xlist], iterates over the xlist,
    # pulling out a single value assigned as x, and does something to it
    # if called for "beam.deflection('12ft')" then we would get a single result for the deflection at '12ft'
    # by iterating over the full list of 'x', assigned above, we can get a list of corresponding values
    deflection = [beam.deflection(_x).to_base_units() for _x in x]

    # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
    # The plot size, unit display, interactivity, and tooltip is handled within this function
    plot('Beam Deflection', 'x', 'y', x, deflection, False, True)
    maxd = beam.maxDeflection()

    # We can utilize the 'caption' function from streamlit (st) to display information
    st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    st.markdown('---')
    shear = [beam.shear(_x).to_base_units() for _x in x]
    plot('Beam Shear', 'x', 'y', x, shear, False, True)
    maxshear = beam.maxShear()
    st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    st.markdown('---')
    moment = [beam.moment(_x).to_base_units() for _x in x]
    plot('Beam Moment', 'x', 'y', x, moment, False, False)
    maxmoment = beam.maxMoment()
    st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment)}')


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
