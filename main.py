# Import Python standard packages from PyPi [https://pypi.org/]
# If you need to reference in any other standard packages, import them here.
# Added packages should also be added to the 'requirements.txt'
# Use command line 'pip install -r requirements.txt' to install into your virtual environment
import streamlit as st
import numpy as np


# Import local *.py files as reference modules to be utilized in the calculation
# 
import units  # units.py: No changes to units.py will be accepted, unless use case is fully justified.
from plot import plot  # plot.py: No changes to plot.py will be accepted, unless use case is fully justified.
import formulas  # formulas.py: Revise as necessary for your numerical calculations.


# This is the one your looking for to update for your calculation.
def run():
    st.markdown('### Input')
    st.markdown('##### Load Inputs')
    def_load = units.load('1200 lbf')
    load = units.input('Applied Load', def_load, minor=False)
    distance = units.input('Distance to Load from Fixed end', '15 feet')

    st.markdown('##### Beam Inputs')
    length = units.input('Total length of beam', '25 ft')
    modulus = units.input("Young's Modulus", '27_500_000 lbf/in**2', minor=True)
    inertia = units.input('Second Moment of Area', '209 in**4', True)

    st.markdown('### Results')
    beam = formulas.CantileverIntermediateLoad(load, length, modulus, inertia, distance)
    x = np.linspace((0*length).to_base_units(), length.to_base_units(), num=100, endpoint=True)
    st.markdown(beam.markdown())
    
    st.markdown('---')
    deflection = [beam.deflection(_x).to_base_units() for _x in x]
    plot('Beam Deflection', 'x', 'y', x, deflection, False, True)
    maxd = beam.maxDeflection()
    st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    st.markdown('---')
    shear = [beam.shear(_x).to_base_units() for _x in x]
    plot('Beam Shear', 'x', 'y', x, shear, False, True)
    maxshear = beam.maxShear()
    st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    maxslope = beam.maxSlope()

    st.markdown('---')
    moment = [beam.moment(_x).to_base_units() for _x in x]
    plot('Beam Moment', 'x', 'y', x, moment, False, True)
    maxmoment = beam.maxMoment()
    st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment, minor=True)}')


# Don't revise. Changes to your calculation title and instructions should be made within the 'information.md' file.
def setup():
    with open('information.md', 'r') as f:
        header = f.read()
    #header = eval(header)
    st.write(header)
    run()


# Don't revise. Run setup() if this file is the entry 
if __name__ == '__main__':
    st.set_page_config(
        page_title='STV_Test Calculation Set',
        layout='wide'
    )
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        setup()
