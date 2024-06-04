import streamlit as st
import numpy as np
from datetime import datetime
import units  # units.py: No changes to units.py will be accepted, unless use case is fully justified.
from plot import plot  # plot.py: No changes to plot.py will be accepted, unless use case is fully justified.


def check_validity(self, expireDate):
    """Disable calculation if date has passed

    If the calculations are dependent on a code that is frequently changed,
    prevent the results to be shown until the code is updated.
    """
    if datetime.today() > expireDate:
        st.error('This calculation set has expired and requires updating')
        st.warning('Please notify your discipline lead.')
        raise Exception(f'[{self}]')


class CantileverEndLoad():
    """Return the values of deflection, slope, shear, and moment

    Cantilever beam with End Loading
    Fixed at the left and free to the right
    Calculations from Gere, Lindeburg, and Shigley
    """

    def __init__(self):
        check_validity(self, datetime(year=2024, month=12, day=1))
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
        self.F = units.input('Applied Load', def_load, minor=False)

        # Another option to get data from the user is in tabular form, if you need multiple values of the same type.
        # For this, you can use the 'units.table_input()' function. An example string is shown below.
        # Be sure the variable declaration (left of the equals), has the same length as the lists provided for the function label, defaul, and minor inputs.
        # l, v, s = units.table_input(('Conduit Length', 'Voltage Class', 'Speed'), ('1.0 ft', '1.0 V', '12.0 mph'))
        # st.write(l)
        # st.write(v, s)

        # Section Header for input Data
        st.markdown('##### Beam Inputs')
        self.L = units.input('Total length of beam', '25 ft')
        modulus = units.input("Young's Modulus", '27_500_000 lbf/in**2', minor=True)
        inertia = units.input('Second Moment of Area', '209 in**4', True)
        self.EI = modulus * inertia
        # For this example, we want to plot the beam properties over its length
        # So we use the numpy (np) 'linspace' command to create a range of values
        self._x = np.linspace((0*self.L).to_base_units(), self.L.to_base_units(), num=100, endpoint=True)

    def x(self):
        return self._x

    def markdown(self):
        md = """
        |  |  |
        | :--- | --- |
        | Deflection | $ \delta = {Fx^2 \over 6EI} \cdot (3L-x)$ |
        | Slope | $\\theta = -{Fx \over 2EI} \cdot (2L-x)$ |
        | Shear | $V = +F$ |
        | Moment | $M = -F(L-x)$ |
        """
        return md

    def deflection(self, x):
        return -((self.F * x**2)/(6 * self.EI)) * (3 * self.L - x)

    def maxDeflection(self):
        return ((self.F * self.L**3) / (3 * self.EI))

    def slope(self, x):
        return -((self.F * x)/(2 * self.EI))*(2 * self.L - x)

    def maxSlope(self):
        return ((self.F * self.L**2)/(2*self.EI))

    def shear(self):
        return self.F

    def maxShear(self):
        return self.F

    def moment(self, x):
        return -(self.F * (self.L - x))

    def maxMoment(self):
        return -(self.F * self.L)

    def plotDeflection(self):
        # The syntax [do_something_to x for x in xlist], iterates over the xlist,
        # pulling out a single value assigned as x, and does something to it
        # if called for "deflection('12ft')" then we would get a single result for the deflection at '12ft'
        # by iterating over the full list of 'x', we can get a list of corresponding values
        deflection = [self.deflection(x).to_base_units() for x in self._x]

        # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
        # The plot size, unit display, interactivity, and tooltip is handled within this function
        plot('Beam Deflection', 'x', 'y', self._x, deflection, False, True)
        maxd = self.maxDeflection()
        # We can utilize the 'caption' function from streamlit (st) to display information
        st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    def plotShear(self):
        shear = [self.shear().to_base_units() for x in self._x]
        plot('Beam Shear', 'x', 'y', self._x, shear, False, True)
        maxshear = self.maxShear()
        st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    def plotMoment(self):
        moment = [self.moment(x).to_base_units() for x in self._x]
        plot('Beam Moment', 'x', 'y', self._x, moment, False, False)
        maxmoment = self.maxMoment()
        st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment)}')


class CantileverIntermediateLoad():
    """Return the values of deflection, slope, shear, and moment

    Cantilever beam with Intermediate Loading
    Fixed at the left and free to the right
    Calculations common to Gere, Lindeburg, and Shigley
    """
    def __init__(self):
        check_validity(self, datetime(year=2024, month=12, day=1))
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
        self.F = units.input('Applied Load', def_load, minor=False)

        # You can also simply load the default unit in the same step
        self.a = units.input('Distance to Load from Fixed end', '15 feet')

        # Another option to get data from the user is in tabular form, if you need multiple values of the same type.
        # For this, you can use the 'units.table_input()' function. An example string is shown below.
        # Be sure the variable declaration (left of the equals), has the same length as the lists provided for the function label, defaul, and minor inputs.
        # l, v, s = units.table_input(('Conduit Length', 'Voltage Class', 'Speed'), ('1.0 ft', '1.0 V', '12.0 mph'))
        # st.write(l)
        # st.write(v, s)

        # Section Header for input Data
        st.markdown('##### Beam Inputs')
        self.L = units.input('Total length of beam', '25 ft')
        modulus = units.input("Young's Modulus", '27_500_000 lbf/in**2', minor=True)
        inertia = units.input('Second Moment of Area', '209 in**4', True)
        self.EI = modulus * inertia
        # For this example, we want to plot the beam properties over its length
        # So we use the numpy (np) 'linspace' command to create a range of values
        self._x = np.linspace((0*self.L).to_base_units(), self.L.to_base_units(), num=100, endpoint=True)

    def x(self):
        return self._x

    def markdown(self):
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

    def return_max(self, _list):
        _min = min(_list)
        _max = max(_list)
        return _max if abs(_max) > abs(_min) else _min

    def deflection(self, x):
        if x <= self.a:
            return -((self.F * x**2)/(6 * self.EI)) * (3 * self.a - x)
        else:
            return -((self.F * self.a**2)/(6 * self.EI)) * (3 * x - self.a)

    def maxDeflection(self):
        return (((self.F * self.a**2) / (6 * self.EI)) * (3 * self.L - self.a))

    def slope(self, x):
        if x <= self.a:
            return -((self.F * x)/(2 * self.EI))*(2 * self.a - x)
        else:
            return -((self.F * self.a**2)/(2 * self.EI))

    def maxSlope(self):
        _slopes = [self.slope(x).to_base_units() for x in self._x]
        return self.return_max(_slopes)

    def shear(self, x):
        if x <= self.a:
            return self.F
        else:
            return self.F * 0  # Maintains intended units

    def maxShear(self):
        _shear = [self.shear(x).to_base_units() for x in self._x]
        return self.return_max(_shear)

    def moment(self, x):
        if x <= self.a:
            return -(self.F * (self.a - x))
        else:
            return self.F * self.a * 0  # Maintains intended units

    def maxMoment(self):
        _moment = [self.moment(x).to_base_units() for x in self._x]
        return self.return_max(_moment)

    def plotDeflection(self):
        # The syntax [do_something_to x for x in xlist], iterates over the xlist,
        # pulling out a single value assigned as x, and does something to it
        # if called for "deflection('12ft')" then we would get a single result for the deflection at '12ft'
        # by iterating over the full list of 'x', we can get a list of corresponding values
        deflection = [self.deflection(x).to_base_units() for x in self._x]

        # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
        # The plot size, unit display, interactivity, and tooltip is handled within this function
        plot('Beam Deflection', 'x', 'y', self._x, deflection, False, True)
        maxd = self.maxDeflection()
        # We can utilize the 'caption' function from streamlit (st) to display information
        st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    def plotShear(self):
        shear = [self.shear(x).to_base_units() for x in self._x]
        plot('Beam Shear', 'x', 'y', self._x, shear, False, True)
        maxshear = self.maxShear()
        st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    def plotMoment(self):
        moment = [self.moment(x).to_base_units() for x in self._x]
        plot('Beam Moment', 'x', 'y', self._x, moment, False, False)
        maxmoment = self.maxMoment()
        st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment)}')


class CantileverUniformDistributedLoad():
    """Return the values of deflection, slope, shear, and moment

    Cantilever beam with Uniform Distributed Loading
    Fixed at the left and free to the right
    Calculations common to Gere, Lindeburg, and Shigley
    """
    def __init__(self):
        check_validity(self, datetime(year=2024, month=12, day=1))
        # Input Data Caption
        st.markdown('### Input')

        # Section Header for input Data
        st.markdown('##### Load Inputs')

        # Numbers can be requested from the user through the 'units.input()' function
        # You can pre-define the default value, as is done in this first case
        # 'units.load()' is utlizied to pre-define a magnitude and unit
        # many common units are available to be interpreted in string format
        def_load = units.load('120 lbf/ft')

        # Then 'units.input()' creates the input field in the website
        # It handles displaying the title, input box, unit selector drop-down and unit conversions
        # The (minor) field is optional and defaults to False, this determines if
        # inches or feet should be selected, for example.
        self.w = units.input('Applied Distributed Load', def_load, minor=False)

        # Section Header for input Data
        st.markdown('##### Beam Inputs')
        self.L = units.input('Total length of beam', '25 ft')
        modulus = units.input("Young's Modulus", '27_500_000 lbf/in**2', minor=True)
        inertia = units.input('Second Moment of Area', '209 in**4', True)
        self.EI = modulus * inertia
        # For this example, we want to plot the beam properties over its length
        # So we use the numpy (np) 'linspace' command to create a range of values
        self._x = np.linspace((0*self.L).to_base_units(), self.L.to_base_units(), num=100, endpoint=True)

    def x(self):
        return self._x

    def markdown(self):
        md = """
        |  |  |
        | :--- | --- |
        | Deflection | $ \delta = -{\\omega x^2 \over 24EI} \cdot (6L^2-4Lx+x^2)$ |
        | Slope | $\\theta = -{\\omega x \over 6EI} \cdot (3L^2-3Lx+x)$ |
        | Shear | $V = +\\omega (L-x)$ |
        | Moment | $M = -\\omega (L-x)^2/2$ |
        """
        return md

    def return_max(self, _list):
        _min = min(_list)
        _max = max(_list)
        return _max if abs(_max) > abs(_min) else _min

    def deflection(self, x):
        return -((self.w * x**2)/(24 * self.EI)) * (6 * self.L**2 - 4 * self.L * x + x**2)

    def maxDeflection(self):
        _defl = [self.deflection(x).to_base_units() for x in self._x]
        return self.return_max(_defl)

    def slope(self, x):
        return -((self.w * x)/(6 * self.EI)) * (3 * self.L**2 - 3 * self.L * x + x)

    def maxSlope(self):
        _slopes = [self.slope(x).to_base_units() for x in self._x]
        return self.return_max(_slopes)

    def shear(self, x):
        return self.w * (self.L - x)

    def maxShear(self):
        _shear = [self.shear(x).to_base_units() for x in self._x]
        return self.return_max(_shear)

    def moment(self, x):
        return -(self.w * (self.L - x)**2 / 2)

    def maxMoment(self):
        _moment = [self.moment(x).to_base_units() for x in self._x]
        return self.return_max(_moment)

    def plotDeflection(self):
        # The syntax [do_something_to x for x in xlist], iterates over the xlist,
        # pulling out a single value assigned as x, and does something to it
        # if called for "deflection('12ft')" then we would get a single result for the deflection at '12ft'
        # by iterating over the full list of 'x', we can get a list of corresponding values
        deflection = [self.deflection(x).to_base_units() for x in self._x]

        # Since we have two lists of equal length, x and deflection, we plot these by using the 'plot()' function
        # The plot size, unit display, interactivity, and tooltip is handled within this function
        plot('Beam Deflection', 'x', 'y', self._x, deflection, False, True)
        maxd = self.maxDeflection()
        # We can utilize the 'caption' function from streamlit (st) to display information
        st.caption(f'Maximum Deflection = {units.unitdisplay(maxd, minor=True)}')

    def plotShear(self):
        shear = [self.shear(x).to_base_units() for x in self._x]
        plot('Beam Shear', 'x', 'y', self._x, shear, False, True)
        maxshear = self.maxShear()
        st.caption(f'Maximum Shear = {units.unitdisplay(maxshear, minor=True)}')

    def plotMoment(self):
        moment = [self.moment(x).to_base_units() for x in self._x]
        plot('Beam Moment', 'x', 'y', self._x, moment, False, False)
        maxmoment = self.maxMoment()
        st.caption(f'Maximum Moment = {units.unitdisplay(maxmoment)}')
