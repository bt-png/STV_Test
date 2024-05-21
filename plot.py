import streamlit as st
import pandas as pd
import units
import altair as alt


def plot(_title, _xTitle, _yTitle, _xData, _yData, _xMinor=False, _yMinor=False):
    _df = pd.DataFrame({
        'X': [x.to_base_units().magnitude for x in _xData],
        'Y': [y.to_base_units().magnitude for y in _yData]
    })
    _df[str(_xTitle)] = [units.unitdisplay(x, _xMinor) for x in _xData]
    _df[str(_yTitle)] = [units.unitdisplay(y, _yMinor) for y in _yData]
    nearest = alt.selection_point(nearest=True, fields=['X'], on='mouseover', empty=False)
    line = alt.Chart(_df, title=alt.Title(_title, anchor='start', orient='bottom')).mark_line().encode(
        alt.X('X:Q').scale(zero=False).axis(labels=False, title=_xTitle),
        alt.Y('Y:Q').scale(zero=False).axis(labels=False, title=_yTitle),
        alt.Tooltip([str(_xTitle+':N'), str(_yTitle+':N')])
    )
    selectors = alt.Chart(_df).mark_point().encode(
        alt.X('X:Q'),
        alt.Tooltip([str(_xTitle+':N')]),
        opacity=alt.value(0)
    ).add_params(nearest)
    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
    text = line.mark_text(align='left', dx=5, dy=-5).encode(text=alt.condition(nearest, str(_yTitle+':N'), alt.value(' ')))
    rules = alt.Chart(_df).mark_rule(color='gray').encode(x='X:Q').transform_filter(nearest)
    chart = alt.layer(line + selectors + points + rules + text).properties(width=800, height=300).configure_axis(grid=False)
    #st.dataframe(_df)
    st.write(chart)
