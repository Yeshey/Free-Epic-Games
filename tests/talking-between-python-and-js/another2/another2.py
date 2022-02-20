#!/usr/bin/python
from bottle import run, route, request, response
import subprocess

@route('/', method='POST')
def index():
    command = request.POST['command']
    result = subprocess.check_output(['batchfile.bat', command], shell=True)

    response.set_header('Access-Control-Allow-Origin', '*')
    return result

run(host='localhost', port=8080, reloader=True)