import streamlit as st
from pint import UnitRegistry


ureg = UnitRegistry()
# ureg.autoconvert_to_preferred = True
ureg.autoconvert_offset_to_baseunit = True
ureg.default_format = '.3f'

gravity = ureg('standard_gravity')


def get_UnitRegistry():
    return ureg


def load(str):
    """Returns a quantity value with magnitude and unit.
    
    This function takes in a string formatted unit and converts it
    to a quantity value with base units, enabling conversion.
    Available string inputs include '3 feet', '12.25 lbf', '3.4*10^3 Nm', ...etc

    A warning will be thrown if the string input cannot be recognized.
    """

    try:
        return ureg.Quantity(str)
    except Exception:
        pass


def unitdisplay(val, minor=False):
    """Returns the quantity in both US Customary and SI base units.

    This function will display a formatted text string containing units of measure.
    val = quantity (created by functions .load or .input)
    minor = boolean (display as major unit (ft/m) or minor unit (in/mm). default=False)
    """
    match val.dimensionality:
        case '[length]':  # Length
            if minor:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('in')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('mm')))
                    )
            else:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('ft')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('m')))
                    )
        case '[temperature]':  # Temperature
            if 'delta' in str(val.units):
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('delta_degF')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('delta_degC')))
                )
            else:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('degF')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('degC')))
                )
        case '1/[temperature]':  # Temp Coefficient
            return (
                '{:.3f~P}'.format(val.to(ureg.Unit('1/delta_degF')))
                + ' | ' +
                '{:.3f~P}'.format(val.to(ureg.Unit('1/delta_degC')))
            )
        case '[length]**2':  # Area
            if minor:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('in**2')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('mm**2')))
                    )
            else:
                return (
                    '{:.4f~P}'.format(val.to(ureg.Unit('ft**2')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('m**2')))
                    )
        case '[length]**4':  # Second Moment of Area
            if minor:
                return (
                    '{:.0f~P}'.format(val.to(ureg.Unit('in**4')))
                    + ' | ' +
                    '{:.0f~P}'.format(val.to(ureg.Unit('mm**4')))
                    )
            else:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('ft**4')))
                    + ' | ' +
                    '{:.1f~P}'.format(val.to(ureg.Unit('m**4')))
                    )
        case '[length]/[time]':  # Velocity
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('ft/s')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('m/s')))
                    )
            else:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('mile_per_hour')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('kilometer_per_hour')))
                    )
        case '[mass]/[length]':  # Mass / Length
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lb/in')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('kg/mm')))
                    )
            else:
                return (
                    '{:.4f~P}'.format(val.to(ureg.Unit('lb/ft')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('kg/m')))
                    )
        case '[length]*[mass]/[time]**2':  # Force
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lbf')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('N')))
                    )
            else:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('kip')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('kN')))
                    )
        case '[length]**2*[mass]/[time]**2':  # Force*Length
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lbf*in')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('N*mm')))
                    )
            else:
                return (
                    '{:.3f~P}'.format(val.to(ureg.Unit('kip*ft')))
                    + ' | ' +
                    '{:.3f~P}'.format(val.to(ureg.Unit('kN*m')))
                    )
        case '[mass]/[time]**2':  # Force / Length
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lbf/in')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('N/mm')))
                    )
            else:
                return (
                    '{:.4f~P}'.format(val.to(ureg.Unit('lbf/ft')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('N/m')))
                    )
        case '[mass]/[length]/[time]**2':  # Pressure
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lbf/in**2')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('N/mm**2')))
                    )
            else:
                return (
                    '{:.4f~P}'.format(val.to(ureg.Unit('lbf/ft**2')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('N/m**2')))
                    )
        case '[mass]/[length]**3':  # Density
            if minor:
                return (
                    '{:.2f~P}'.format(val.to(ureg.Unit('lb/in**3')))
                    + ' | ' +
                    '{:.2f~P}'.format(val.to(ureg.Unit('kg/mm**3')))
                    )
            else:
                return (
                    '{:.4f~P}'.format(val.to(ureg.Unit('lb/ft**3')))
                    + ' | ' +
                    '{:.4f~P}'.format(val.to(ureg.Unit('kg/m**3')))
                    )
        case '':  # Dimensionless
            return val
        case _:
            return val.dimensionality


def availableUnits(val):
    match val:
        case '[length]':
            return ('foot', 'inch', 'meter', 'mm')
        case '[temperature]':
            return ('degree_Fahrenheit', 'degC', 'delta_degree_Fahrenheit', 'delta_degree_Celsius')
        case '1/[temperature]':
            return ('1/delta_degree_Fahrenheit', '1/delta_degC')
        case '[length]**2':
            return ('foot**2', 'inch**2', 'meter**2', 'mm**2')
        case '[length]**4':
            return ('foot**4', 'inch**4', 'meter**4', 'mm**4')
        case '[length]/[time]':
            return ('mile_per_hour', 'fts', 'kph', 'mps')
        case '[mass]/[length]':
            return ('pound/foot', 'pound/inch', 'kilogram/meter', 'kilogram/mm')
        case '[length]*[mass]/[time]**2':
            return ('force_pound', 'N')
        case '[mass]/[time]**2':
            return ('lbf_ft', 'lbf_in', 'N_m', 'N_mm')
        case '[mass]/[length]/[time]**2':
            return ('lbf/ft**2', 'force_pound/inch**2', 'N/m**2', 'N/mm**2')
        case '[mass]/[length]**3':
            return ('pound/foot**3', 'lb/in**3', 'kilogram/meter**3', 'kg/mm**3')
        case '':
            pass
        case _:
            pass


def input(label, default, minor=False):
    """Returns a quantity value from a user input field.

    This function creates a streamlit number input field to update the quantity. The unit of measure is
    fixed based on the default values units. Magnitude or base unit may be changed by the user.
    label = string (input field text string)
    default = quantity | str (set by .load)
    minor = boolean (display as major unit (ft/m) or minor unit (in/mm). default=False)
    """
    col1, col2, col21, col3 = st.columns([2, 3, 2, 3])
    col1.write('<div style="text-align:right">'+label+'</div>', unsafe_allow_html=True)

    if type(default) == str:
        _default = load(default)
    else:
        _default = default
    magnitude = col2.number_input(label=label, label_visibility='collapsed', value=_default.magnitude)
    if _default.dimensionality == '':
        unittype = _default.units
    else:
        try:
            idx = availableUnits(_default.dimensionality).index(_default.units)
        except Exception:
            col2.warning(f'{_default.dimensionality}, {_default.units}')
            raise Exception
        unittype = col21.selectbox(
            label=label, label_visibility='collapsed', options=availableUnits(_default.dimensionality), index=idx
            )
    val = ureg.Quantity(magnitude, unittype)
    col3.caption(unitdisplay(val, minor))
    return val
