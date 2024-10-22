# Import Python standard packages from PyPi [https://pypi.org/]
# If you need to reference in any other standard packages, import them here.
# Added packages should also be added to the 'requirements.txt'
# Use command line 'pip install -r requirements.txt' to install into your virtual environment
import streamlit as st
import numpy as np


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
    |  |  | |
    | :--- | --- | --- |
    | Deflection | $ \delta = {Fx^2 \over 6EI} \cdot (3a-x)$ | $(0 \leq x \leq a)$ |
    | | $ \delta = {Fa^2 \over 6EI} \cdot (3x-a)$ | $(a \leq x \leq L)$ |
    | Slope | $\\theta = -{Fx \over 2EI} \cdot (2a-x)$ | $(0 \leq x \leq a)$ |
    | | $\\theta = -{Fa^2 \over 2EI}$ | $(a \leq x \leq L)$ |
    | Shear | $V = +F$ | $(0 \leq x \leq a)$ |
    | | $V = 0$ | $(a \leq x \leq L)$ |
    | Moment | $M = -F(a-x)$ | $(0 \leq x \leq a)$ |
    | | $M = 0$ | $(a \leq x \leq L)$ |
    """
    return md


def calcDeflection(F, E, I, a, x):
    if x <= a:
        return -((F * x**2)/(6 * E * I)) * (3 * a - x)
    else:
        return -((F * a**2)/(6 * E * I)) * (3 * x - a)


def maxDeflection(F, L, E, I, a):
    return (((F * a**2) / (6 * E * I)) * (3 * L - a))


def calcShear(F, a, x):
    if x <= a:
        return F
    else:
        return F * 0  # Maintains intended units


def calcMoment(F, a, x):
        if x <= a:
            return -(F * (a - x))
        else:
            return F * a * 0  # Maintains intended units


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

    # Lets present the formulas we want to utilize using markdown notation.
    # Visit 'https://www.upyesp.org/posts/makrdown-vscode-math-notation/' for information
    st.markdown(markdown())

    # For this example, we want to plot the beam properties over its length
    # So we use the numpy (np) 'linspace' command to create a range of values
    x = np.linspace((0*length).to_base_units(), length.to_base_units(), num=100, endpoint=True)

    # We can provide a visual break in the data through a hard line, created by 'st.markdown('---')'
    st.markdown('---')

    # The syntax [do_something_to x for x in xlist], iterates over the xlist,
    # pulling out a single value assigned as x, and does something to it
    # if called for "beam.deflection('12ft')" then we would get a single result for the deflection at '12ft'
    # by iterating over the full list of 'x', assigned above, we can get a list of corresponding values
    # Notice here that we have to be careful not to assign our variable name the same as our function name.
    deflection = [calcDeflection(F=load, E=modulus, I=inertia, a=distance, x=_x).to_base_units() for _x in x]

    # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
    # The plot size, unit display, interactivity, and tooltip is handled within this function
    # If you compare the "SingleCalc" to the "MultiCalc", you will notice that by using the Class object, we only need
    # to define the input variables once. Since the object stores the data, we then can simply just call out the methods we want to utilize.
    # However, in this example we need to provide the variables each time.
    plot('Beam Deflection', 'x', 'y', x, deflection, False, True)
    maxd = maxDeflection(F=load, L=length, E=modulus, I=inertia, a=distance)

    # We can utilize the 'caption' function from streamlit (st) to display information
    st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    st.markdown('---')
    shear = [calcShear(F=load, a=distance, x=_x).to_base_units() for _x in x]
    plot('Beam Shear', 'x', 'y', x, shear, False, True)
    maxshear = return_max(shear)
    st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    st.markdown('---')
    moment = [calcMoment(F=load, a=distance, x=_x).to_base_units() for _x in x]
    plot('Beam Moment', 'x', 'y', x, moment, False, False)
    maxmoment = return_max(moment)
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
