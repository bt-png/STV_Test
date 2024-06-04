# Import Python standard packages from PyPi [https://pypi.org/]
# If you need to reference in any other standard packages, import them here.
# Added packages should also be added to the 'requirements.txt'
# Use command line 'pip install -r requirements.txt' to install into your virtual environment
import streamlit as st
import numpy as np


# Import local *.py files as reference modules to be utilized in the calculation
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
    # create columns with relative sizes to control the width of the selection box
    col1, col2, col3 = st.columns([1, 10, 20])
    
    # Present a selection to the user to define which calculation should be considered.
    selection = col2.selectbox(
        label='Beam Types',
        options=['Cantilever, End Loaded', 'Cantilever, Intermediate Loaded', 'Cantilever, Uniform Distributed Load'],
        placeholder='Select a Beam and Loading type',
        index=None
    )
    match selection:
        # We are calling the 'CantileverEndLoad' or 'CantileverIntermediateLoad' class object, depending on the selection, which is defined within the 'formulas.py' module
        # By creating a class, we then are able to directly request from it standard items.
        # This makes managing the formulas easier.
        # The inputs to the class can be seen and matched up with the '__init__' definition within
        # the class within formulas.py
        case 'Cantilever, End Loaded':
            beam = formulas.CantileverEndLoad()
        case 'Cantilever, Intermediate Loaded':
            beam = formulas.CantileverIntermediateLoad()
        case 'Cantilever, Uniform Distributed Load':
            beam = formulas.CantileverUniformDistributedLoad()
        case _: # If the selection does not match anything previously, then...
            st.warning('Please choose a Beam and Loading type from the drop down menu!')
            # Since no selection was made, we do not want to continue to process any further code.
            # We can utilize the stop command within streamlit to no longer render any additional text.
            st.stop()

    # Section Header for Results
    st.markdown('### Results')

    # One of the class functions is 'def markdown():'
    # This presents the formulas utilized within this class in mathmatical representation
    # To better engage the end user, try to represent your equations correctly by including a markdown function
    st.markdown(beam.markdown())

    # We can provide a visual break in the data through a hard line, created by 'st.markdown('---')'
    st.markdown('---')

    # By accessing the functions within whichever class module was assigned to 'beam', we can standardize the output results.
    beam.plotDeflection()

    st.markdown('---')
    beam.plotShear()

    st.markdown('---')
    beam.plotMoment()
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
