#!/usr/bin/env python3

from config import icsfile

from flask import Flask, render_template, send_file


from functions import debug, fetch_hf_data, read_ics, scheduler


fetch_hf_data()
scheduler.start()

app = Flask(__name__)


@app.route('/', methods=["GET"])
def status():
    return render_template('status.html',
                           debug=debug,
                           jobs="".join(map(str, scheduler.get_jobs())),
                           icsfile=icsfile,
                           ics=read_ics(icsfile)
                           )


@app.route('/' + icsfile, methods=["GET"])
def serve_ics():
    return send_file(
            icsfile,
            as_attachment=True)
