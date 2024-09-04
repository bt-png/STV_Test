import streamlit as st
import pandas as pd
import pint_xarray  # accessor via Dataset.pint
from pint import UnitRegistry
import xarray as xr


testing = False

ureg = UnitRegistry()
# ureg.autoconvert_to_preferred = True
ureg.autoconvert_offset_to_baseunit = True
ureg.default_format = '.3f'

gravity = ureg('standard_gravity')
pi = ureg('pi')
e = ureg('eulers_number')


def unit_round(val, roundval, units):
    return round((val.to(units)/roundval.to(units)),0)*roundval


def unit_round_down(val, roundval, units):
    return int(round(val.to(units).magnitude/roundval.to(units).magnitude, 0))*roundval


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
    try:
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
                    '{:.6f~P}'.format(val.to(ureg.Unit('1/megadelta_degF')))
                    + ' | ' +
                    '{:.6f~P}'.format(val.to(ureg.Unit('1/megadelta_degC')))
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
                        '{:.6f~P}'.format(val.to(ureg.Unit('in**4')))
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
                        '{:.3f~P}'.format(val.to(ureg.Unit('mph')))
                        + ' | ' +
                        '{:.3f~P}'.format(val.to(ureg.Unit('kph')))
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
                return val
    except Exception:
        return '{:}'.format(val)


def availableUnits(val):
    match val.dimensionality:
        case '[length]':
            return ('foot', 'inch', 'meter', 'millimeter')
        case '[temperature]':
            return ('degree_Fahrenheit', 'degC', 'delta_degree_Fahrenheit', 'delta_degree_Celsius')
        case '1/[temperature]':
            return ('1/delta_degree_Fahrenheit', '1/megadelta_degree_Fahrenheit', '1/delta_degree_Celsius', '1/megadelta_degree_Celsius')
        case '[length]**2':
            return ('foot**2', 'inch**2', 'meter**2', 'millimeter**2')
        case '[length]**4':
            return ('foot**4', 'inch**4', 'meter**4', 'millimeter**4')
        case '[length]/[time]':
            return ('mph', 'ft/s', 'kph', 'm/s')
        case '[mass]/[length]':
            return ('pound/foot', 'pound/inch', 'kilogram/meter', 'kilogram/millimeter')
        case '[length]*[mass]/[time]**2':
            return ('force_pound', 'N')
        case '[mass]/[time]**2':
            return ('lbf_ft', 'lbf_in', 'newton_meter', 'newton_millimeter')
        case '[mass]/[length]/[time]**2':
            return ('lbf/ft**2', 'force_pound/inch**2', 'newton/meter**2', 'newton/millimeter**2')
        case '[mass]/[length]**3':
            return ('pound/foot**3', 'lb/in**3', 'kilogram/meter**3', 'kg/millimeter**3')
        case '':
            return (str(val.units), ' ')
        case _:
            return (str(val.units), ' ')


def columns():
    return st.columns([2, 3, 2, 3])


def inputcolumns():
    return st.columns([2, 3, 2, 3])


def selectioncolumns():
    return st.columns([2, 5, 3])


def selection(label: str, options: list) -> str:
    """Returns a string value from a user input drop down selection.

    This function creates a streamlit selectbox input field to update the selection.
    label = string (input field text string)
    options = list (available selections)
    """
    cols = selectioncolumns()
    cols[0].write('<div style="text-align:right">'+label+'</div>', unsafe_allow_html=True)
    return cols[1].selectbox(label, options, label_visibility="collapsed")


def output(label: str, val: UnitRegistry.Unit, strformat=None, minor=False):
    cols = selectioncolumns()
    cols[0].write('<div style="text-align:right">'+label+'</div>', unsafe_allow_html=True)
    if strformat is None:
        cols[1].write(unitdisplay(val, minor))
    else:
        cols[1].write(strformat.format(val))


def input(label: str, default: str | UnitRegistry.Quantity, minor: bool = False) -> UnitRegistry.Quantity:
    """Returns a quantity value from a user input field.

    This function creates a streamlit number input field to update the quantity. The unit of measure is
    fixed based on the default values units. Magnitude or base unit may be changed by the user.
    label = string (input field text string)
    default = quantity | str (set by .load)
    minor = boolean (display as major unit (ft/m) or minor unit (in/mm). default=False)
    """
    cols = inputcolumns()
    cols[0].write('<div style="text-align:right">'+label+'</div>', unsafe_allow_html=True)

    if type(default) is str:
        _default = load(default)
    else:
        _default = default
    try:
        magnitude = cols[1].number_input(label=label, label_visibility='collapsed', value=_default.magnitude)
    except Exception:
        pass

    if _default.dimensionality == '':
        unittype = _default.units
    else:
        try:
            st.write(_default.units) if testing else None
            idx = availableUnits(_default).index(_default.units)
            st.write(idx)  if testing else None
        except Exception:
            idx = 0
        unittype = cols[2].selectbox(
            label=label, label_visibility='collapsed', options=availableUnits(_default), index=idx
            )
    val = ureg.Quantity(magnitude, unittype)
    cols[3].caption(unitdisplay(val, minor))
    return val


def table_input(
        label: list | str,
        default: list | str | UnitRegistry.Quantity,
        minor: list | bool = False,
        selection: list | str = False
        ) -> list | UnitRegistry.Quantity:
    """Returns a list of quantity values from the user.

    This function creates a streamlit data_editor to receive free values. The unit of measure is
    set based on the default values units and should be in a list form, matching the length of the 'label' list.  
    Magnitude or base unit may be changed by the user through the generated drop down and table.  
    # Example  
    length, voltage, speed = units.table_input(  
        label=('label for ft input', 'Voltage', 'Speed'),  
        default=('1 ft', '1 V', '1 mph'),  
        minor=(True, False, False)  
        )  

    # Inputs  
    label = list of strings (names for each column of the dataframe)  
    default = quantity | str (set by .load, with the same shape as the label list)  
    minor = list of boolean (display as major unit (ft/m) or minor unit (in/mm). default=False)
    selection = list of selection strings
    * If selection is provided, this will be the first return variable
    """
    _quantity = [load(val) for val in default]
    _magnitude = [load(val).magnitude for val in default]
    _cols = st.columns(len(label))
    _vals = {}
    for c, lbl, val in zip(_cols, label, _quantity):
        try:
            idx = availableUnits(val).index(val.units)
        except Exception:
            idx = 0
        _vals[lbl] = (c.selectbox(lbl, options=availableUnits(val), index=idx))
    _df_magnitude = pd.DataFrame([_magnitude], columns=label)
    if selection:
        _df_magnitude.insert(0, 'Selection', selection[0])
        result = st.data_editor(_df_magnitude, num_rows='dynamic', hide_index=True, column_config={
            'Selection': st.column_config.SelectboxColumn(options=selection)
        })
    else:
        result = st.data_editor(_df_magnitude, num_rows='dynamic', hide_index=True)
    _ds = xr.Dataset(result)
    ds = _ds.pint.quantify(_vals)
    if selection:
        label = ('Selection',) + label
        return [ds[v].data for v in label]
    else:
        return [ds[v].data for v in label]
