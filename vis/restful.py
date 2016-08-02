import os
import subprocess
import mimetypes
from json import dumps
import flask
from flask_responses import json_response, xml_response, auto_response


app = flask.Flask(__name__)

fst = lambda x_y: x_y[0]
get_mime_info = lambda x: mimetypes.guess_type('fake.%s' % x)
get_mime = lambda x: fst(get_mime_info(x))


def get_suffix(accept):
    best = accept.best_match(['text/plain', 'text/html', 'application/json'])
    if best == 'text/plain':
        return 'txt'
    if best == 'text/html':
        return 'html'
    else:
        return 'json'


def render_appropriate(template, context, accept):
    suffix = get_suffix(accept)
    template_name = '%s.%s' % (template, suffix)
    return flask.render_template(template_name, **context)


@app.route('/', methods=['GET'])
def home():
    return render_appropriate('home', {}, flask.request.accept_mimetypes)


@app.route('/', methods=['POST'])
def query():
    extension = flask.request.form.get('image')
    if extension is not None:
        #return json_response({"image_url": extension, "caption" : "none"}, status_code=200)
        subprocess.call('th eval.lua -model ../Public/model_id1-501-1448236541_cpu.t7 -image_folder vis/uploaded/ -num_images 1 -gpuid -1 -result_folder vis/', shell=True, cwd="../")
    else:
        return flask.redirect(flask.url_for('home'))
    
    
@app.route('/result', methods=['POST'])
def query2():
    image = flask.request.form.get('image')
    caption = flask.request.form.get('caption')
    if image is not None:
        return json_response({"image_url": image, "caption" : caption}, status_code=200)
    else:
        return flask.redirect(flask.url_for('home'))


@app.route('/<extension>')
def doit_baby(extension):
    render = lambda x, y: '%s' % (x if x else y)
    default = flask.request.args.get('default', 'unknown')
    context = {'extension': extension,
               'mime': render(get_mime(extension), default)}
    return render_appropriate('mime', context, flask.request.accept_mimetypes)


if __name__ == '__main__':
    mimetypes.init()
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host='0.0.0.0', port=port, debug=debug)
