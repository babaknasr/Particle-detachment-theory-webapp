# -*- coding: utf-8 -*-
"""

"""

from wtforms import Form, FloatField, validators
from math import pi
import functools

# def check_T(form, field):
#     """Form validation: failure if T > 30 periods."""
#     if field.data != None and form.w.data != None:
#         w = form.w.data
#         T = field.data
#         period = 2*pi/w
#         if T > 30*period:
#             num_periods = int(round(T/period))
#             raise validators.ValidationError(
#                 'Cannot plot as much as %d periods! T<%.2f' %
#                 (num_periods, 30*period))

def check_interval(form, field, min_value=None, max_value=None):
    """For validation: failure if value is outside an interval."""
    if field.data != None:
        failure = False
        if min_value is not None:
            if field.data < min_value:
                failure = True
        if max_value is not None:
            if field.data > max_value:
                failure = True
        if failure:
            raise validators.ValidationError(
                '%s=%s not in [%s, %s]' %
                (field.name, field.data,
                 '-infty' if min_value is None else str(min_value),
                 'infty'  if max_value is None else str(max_value)))

def form_input_interval(min_value=None, max_value=None):
    """Flask-compatible interface to check_interval."""
    return functools.partial(
        check_interval, min_value=min_value, max_value=max_value)

def form_input_positive(form, field):
    if field.data <= 0.0:
        raise validators.ValidationError('Must be a positive number')


class InputForm(Form):
    E1 = FloatField(
        label="Particle Young's modulus (Pa)", default=6.9E9,
        validators=[validators.InputRequired(), form_input_positive, validators.NumberRange(1E-3, None)])
    E2 = FloatField(
        label="Substrate Young's modulus (Pa)", default=6.9E9,
        validators=[validators.InputRequired(), form_input_interval(1E-3,None)])
    Wa = FloatField(
        label='Thermodynamic Work of Adhesion (J/m2)', default=0.4,
        validators=[validators.InputRequired(), form_input_positive] )
    Deltac = FloatField(
        label='Roughness parameter [Delta_c]', default=1,
        validators=[validators.InputRequired(), form_input_positive, form_input_interval(0,10)] )
    
    
