import streamlit as st
import numpy as np
from datetime import datetime

def check_validity(self, expireDate):
    """Disable calculation if date has passed
    
    If the calculations are dependent on a code that is frequently changed,
    prevent the results to be shown until the code is updated.
    """
    if datetime.today() > expireDate:
        st.error('This calculation set has expired and requires updating')
        st.warning('Please notify your discipline lead.')
        #raise Exception(f'[{self}]')


class CantileverEndLoad():
    """Return the values of deflection, slope, shear, and moment

    Cantilever beam with End Loading
    Fixed at the left and free to the right
    Calculations from Gere, Lindeburg, and Shigley
    """
    
    def __init__(self, F, L, E, I):
        check_validity(self, datetime(year=2024, month=6, day=1))
        self.F = F
        self.L = L
        self.EI = E * I
    
    def markdown(self):
        md = """
        |  |  |
        | :--- | --- |
        | Deflection | $ \delta = {Fx^2 \over 6EI} \cdot (3L-x)$ |
        | Slope | $\\theta = -{Fx \over 2EI} \cdot (2L-x)$ |
        | Shear | $V = +F$ |
        | Moment | $M = -F(L)$ |
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
    
    def moment(self, x):
        return -(self.F * (self.L - x))
    
    def maxMoment(self):
        return -(self.F * self.L)


class CantileverIntermediateLoad():
    """Return the values of deflection, slope, shear, and moment

    Cantilever beam with Intermediate Loading
    Fixed at the left and free to the right
    Calculations common to Gere, Lindeburg, and Shigley
    """
    def __init__(self, F, L, E, I, a):
        check_validity(self, datetime(year=2024, month=6, day=1))
        self.F = F
        self.L = L
        self.EI = E * I
        self.a = a
        self._x = np.linspace((0*self.L).to_base_units(), self.L.to_base_units(), num=100, endpoint=True)
    
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
