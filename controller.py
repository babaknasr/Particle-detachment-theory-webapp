# -*- coding: utf-8 -*-
"""

"""

from model import InputForm
from flask import Flask, render_template, request
from compute import compute_usc

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index0():
	return('<a href="/detachment_usc">Particle detachment model</a>')

@app.route('/detachment_usc', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        for field in form:
            # Make local variable (name field.name)
            # exec('%s = %s' % (field.name, field.data))  # exec not work in python 3 !!!!
            # result = compute_usc(E1, E2, Wa, Deltac)
            print(field.name, field.data)
        result = compute_usc(form.E1.data, form.E2.data, form.Wa.data, form.Deltac.data)
        # print(result)
    else:
        result = None

    return render_template('view.html', form=form,
                           result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    