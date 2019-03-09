#!/usr/bin/env python

import os

from flask import Flask, request, jsonify

from src.parser import convertToLaTeX

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/api/convert', methods=['GET'])
def convert():
    if request.method == 'GET':
        asciimath = request.args.get('asciimath')
        if asciimath:
            return jsonify(
                response=convertToLaTeX(asciimath),
                error=None,
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
    app.run(host='0.0.0.0', port=port)
