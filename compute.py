# -*- coding: utf-8 -*-
"""

"""
from math import *
from numpy import exp, cos, linspace
import bokeh.plotting as plt
from bokeh.models import HoverTool
# import os, re
import matlab.engine


def bokeh_ver():
    from bokeh import __version__ as ver
    return ver

def compute_usc(E1, E2, Wa, Deltac):
    eng = matlab.engine.start_matlab()
    # Need to run the addmypath to add costum Path to MATLAB
    # Important: Add 'nargout=0' for function with no output. by default the nargout=1 for python.
    eng.addmypath(nargout=0)

    # Assign global variable in MATLAB engine
    eng.setGlobalvar('theory_isprogressbar', 0, nargout=0)

    pm = 'Glass'
    sm = 'Glass'
    mm = 'Air'
    pref = 'Paper1' #'Soltani(1994)'
    sref = 'Paper1' #'Tsai(1991)'
    cref = 'Paper1' #'Soltani(1994)'
    const = eng.matprop([pm,pref],[sm,sref],[],cref)
    theory = {'smooth':1, 'rough':1, 'rough_bumpy':0, 
          'sublayer':0, 'burst':1, 
          'roll':1, 'slide':0, 'lift':0, 
          'jkr':1, 'dmt':0,'tpl':0,
          'freevelocity':'None', 'Dh':[], 
          'roughness':{'Deltac':Deltac, 'betap':.02, 'n_u':1, 'Nbump':10, 'alpha': pi/6}, 
          'assumption':{'nldrag':1, 'liftforce':0, 'gravityforce':0},
          'minsize':1e-6,
          'maxsize':100e-6,
          'function':2,
         }
    
    const['E1'] = E1
    const['E2'] = E2
    const['Wa'] = Wa
    theory['const'] = const
    
    Result = eng.theory_calculation(theory,nargout=4)

    # plotting
    line_type = ['solid', 'dashed', 'dotted', 'dotdash', 'dashdot']

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select,hover"
    p = plt.figure(title='Particle Detachment models', tools=TOOLS,
               x_axis_type='log', y_axis_type='log',
               x_axis_label='Particle diameter (\u03BCm)', y_axis_label='Critical shear velocity (m/s)')

    for i in range(len(Result[2])):
        print('i=',i)
        x = Result[0][0]
        y = Result[1][i]
        p.line(x, y, legend=Result[2][i]+', '+Result[3][i], line_width=2, line_dash=line_type[i])
        p.select(dict(type=HoverTool)).tooltips = {'x':'$x', 'y':'$y'}
        p.legend.click_policy='hide'

    from bokeh.embed import components
    script, div = components(p)
    print('bokeh ver: ',bokeh_ver())

    head1 = """
<link rel="stylesheet"
 href="http://cdn.pydata.org/bokeh/release/bokeh-""" 
    head2 = """.min.css"
 type="text/css" />
<script type="text/javascript"
 src="http://cdn.pydata.org/bokeh/release/bokeh-"""
    head3 = """.min.js">
</script>
<script type="text/javascript">
Bokeh.set_log_level("info");
</script>
"""
    head = head1 + bokeh_ver() + head2 + bokeh_ver() + head3

    return head, script, div
