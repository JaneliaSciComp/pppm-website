''' ppp_responder.py
    PatchPerPix Match REST API and site
'''
# PATCHED: Configurator dependency removed - pppm_bodies.json is loaded from the
# local file baked into the image; the configurator fallback (and its `CONFIG`
# dict, `call_responder`, and `requests` import) have been removed.

from datetime import datetime, timedelta
import inspect
import json
import os
import sys
from time import time
import traceback
from flask import (Flask, render_template, request,
                   send_file, jsonify)
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_swagger import swagger
import pymysql.cursors
import pymysql.err

# *****************************************************************************
# * Classes                                                                   *
# *****************************************************************************
class InvalidUsage(Exception):
    ''' Return an error response
    '''
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        ''' Build error response
        '''
        retval = dict(self.payload or ())
        retval['rest'] = {'error': self.message}
        return retval


class CustomJSONEncoder(JSONEncoder):
    ''' Define a custom JSON encoder
    '''
    def default(self, obj):   # pylint: disable=E0202, W0221
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%a, %-d %b %Y %H:%M:%S')
            if isinstance(obj, timedelta):
                seconds = obj.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                return "%02d:%02d:%.2f" % (hours, minutes, seconds)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

__version__ = '1.1.0'  # PATCHED: configurator dependency removed
app = Flask(__name__, template_folder='templates')
app.json_encoder = CustomJSONEncoder
app.config.from_pyfile("config.cfg")
CORS(app, supports_credentials=True)
START_TIME = ''
BODIES = dict()


# *****************************************************************************
# * Flask                                                                     *
# *****************************************************************************


@app.before_request
def before_request():
    ''' Set transaction start time and increment counters.
        If needed, initilize global variables.
    '''
    # pylint: disable=W0603
    global START_TIME, BODIES
    try:
        path = 'pppm_bodies.json'
        with open(path) as handle:
            BODIES = json.load(handle)
    except Exception as err:
        return render_template('error.html', urlroot=request.url_root,
                               message='Could not read %s: %s' \
                               % ('path', str(err)))
    START_TIME = time()
    if request.method == 'OPTIONS':
        result = initialize_result()
        return generate_response(result)
    return None


# ******************************************************************************
# * Utility functions                                                          *
# ******************************************************************************


def receive_payload(result):
    ''' Get a request payload (form or JSON).
        Keyword arguments:
          result: result dictionary
        Returns:
          payload dictionary
    '''
    pay = dict()
    if not request.get_data():
        return pay
    try:
        if request.form:
            result['rest']['form'] = request.form
            for i in request.form:
                pay[i] = request.form[i]
        elif request.json:
            result['rest']['json'] = request.json
            pay = request.json
    except Exception as err:
        temp = "{2}: An exception of type {0} occurred. Arguments:\n{1!r}"
        mess = temp.format(type(err).__name__, err.args, inspect.stack()[0][3])
        raise InvalidUsage(mess, 500)
    return pay


def check_missing_parms(ipd, required):
    ''' Check for missing parameters
        Keyword arguments:
          ipd: request payload
          required: list of required parameters
    '''
    missing = ''
    for prm in required:
        if prm not in ipd:
            missing = missing + prm + ' '
    if missing:
        raise InvalidUsage('Missing arguments: ' + missing)


def initialize_result():
    ''' Initialize the result dictionary
        Returns:
          decoded partially populated result dictionary
    '''
    result = {"rest": {'requester': request.remote_addr,
                       'url': request.url,
                       'endpoint': request.endpoint,
                       'error': False,
                       'elapsed_time': '',
                       'row_count': 0,
                       'pid': os.getpid()}}
    return result


def generate_response(result):
    ''' Generate a response to a request
        Keyword arguments:
          result: result dictionary
        Returns:
          JSON response
    '''
    result['rest']['elapsed_time'] = str(timedelta(seconds=(time() - START_TIME)))
    return jsonify(**result)


def generate_navbar(active):
    ''' Generate the web navigation bar
        Keyword arguments:
          active: name of active nav
        Returns:
          Navigation bar
    '''
    nav = '''
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
    '''
    for heading in ['Search', 'Instructions']:
        nav += '<li class="nav-item active">' if heading == active else '<li class="nav-item">'
        link = ('/' + heading[:-1] + 'list').lower()
        link = ('/' + heading).lower()
        nav += '<a class="nav-link" href="%s">%s</a>' % (link, heading)
        nav += '</li>'
    nav += '</ul></div></nav>'
    return nav


def dlink(text, dtype):
    url = BODIES[text][dtype].replace('/nrs/kainmueller/PatchPerPixMatch',
                                      app.config['CONTENT_HOST'])
    return "<a href='%s'>%s</a>" % (url, 'Download ' + dtype)


# *****************************************************************************
# * Web content                                                               *
# *****************************************************************************


@app.route('/download/<string:body>')
def download(body):
    ''' Downloadable content
    '''
    bodyid = body.split('-', 1)[0]
    bodyid = bodyid.split('_')[-1]
    dtype = 'pdf' if 'pdf' in body else 'spreadsheet'
    filepath = BODIES[bodyid][dtype]
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as err:
        return render_template('error.html', urlroot=request.url_root,
                               title='Download error', message=err)


@app.route('/')
@app.route('/search')
def show_search_form():
    '''
    Search form
    Show the search form.
    ---
    tags:
      - Search
    responses:
      200:
          description: Search form
      500:
          description: Error
    '''
    return render_template('search.html', urlroot=request.url_root,
                           navbar=generate_navbar('Search'))


@app.route('/run_search', methods=['OPTIONS', 'POST'])
def run_search():
    '''
    Search body IDs
    Search body IDs.
    ---
    tags:
      - Search
    responses:
      200:
          description: Body ID table
      500:
          description: Error
    '''
    result = initialize_result()
    ipd = receive_payload(result)
    check_missing_parms(ipd, ['key_type', 'key_text'])
    body_list = ipd['key_text'].split()
    good_body = dict()
    result['data'] = 'No bodies were found'
    for body in body_list:
        if body in BODIES:
            good_body[body] = BODIES[body]
    if good_body:
        result['data'] = '''
        <table id="bodies" class="tablesorter standard">
        <thead>
        <tr><th class="sorter-digit">Body ID</th><th>Neuron</th><th>PDF</th><th>Spreadsheet</th></tr>
        </thead>
        <tbody>
        '''
        template = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
        for body, undef in sorted(good_body.items(), key=lambda item: int(item[0])):
            result['data'] += template % (body, good_body[body]['neuron'],
                                          dlink(body, 'pdf'), dlink(body, 'spreadsheet'))
        result['data'] += '</tbody></table>'
    return generate_response(result)


@app.route('/instructions')
def show_instructions_form():
    ''' Show the instructions form
    '''
    rfile = open(app.config['README'], "r")
    readme = rfile.read()
    rfile.close()
    return render_template('instructions.html', urlroot=request.url_root,
                           navbar=generate_navbar('Instructions'),
                           readme=readme)


# *****************************************************************************
# * Endpoints                                                                 *
# *****************************************************************************

@app.route('/help')
def show_swagger():
    ''' Show Swagger docs
    '''
    return render_template('swagger_ui.html')


@app.route("/spec")
def spec():
    ''' Show specification
    '''
    return get_doc_json()


@app.route('/doc')
def get_doc_json():
    ''' Show documentation
    '''
    swag = swagger(app)
    swag['info']['version'] = __version__
    swag['info']['title'] = "PatchPerPix Match"
    return jsonify(swag)

@app.route("/stats")
def stats():
    '''
    Show stats
    Show uptime/requests statistics
    ---
    tags:
      - Configuration
    responses:
      200:
          description: Stats
      400:
          description: Stats could not be calculated
    '''
    result = initialize_result()
    try:
        result['stats'] = {"version": __version__,
                           "python": sys.version,
                           "pid": os.getpid()}
        return generate_response(result)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        traceback.print_tb(ex.__traceback__)
        print(result)
        raise InvalidUsage('Error: %s' % (message,))


# *****************************************************************************


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
