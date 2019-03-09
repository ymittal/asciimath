#!/usr/bin/env python

import os

from flask import (Flask,
                   request,
                   jsonify,
                   render_template,
                   send_from_directory)

from src.parser import convertToLaTeX

app = Flask(__name__, template_folder="frontend")


@app.route('/')
def home():
    return render_template('emailmath.html')


@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.template_folder, path)


@app.route('/api/convert', methods=['GET'])
def convert():
    if request.method == 'GET':
        asciimath = request.args.get('asciimath')
        if asciimath is not None:
            return jsonify(
                latex=convertToLaTeX(asciimath),
                error=False,
            ), 200

        return jsonify(
            error=True,
            error_message='No AsciiMath query param found'
        ), 400

    return jsonify(
        error=True,
        error_message='Only GET request allowed'
    ), 405


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
