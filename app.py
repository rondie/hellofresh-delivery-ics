#!/usr/bin/env python3

from config import icsfile

from flask import Flask, send_file


from functions import fetch_hf_data, scheduler


fetch_hf_data()
scheduler.start()

app = Flask(__name__)


@app.route('/', methods=["GET"])
def status():
    return ('Jobs<br>' +
            "".join(map(str, scheduler.get_jobs())) +
            '<br><br>File<br><a target="_blank" rel="noopener" \
            target="_blank" href="/' + icsfile + '">ics link</a>')


@app.route('/' + icsfile, methods=["GET"])
def serve_ics():
    return send_file(
            icsfile,
            as_attachment=True)
