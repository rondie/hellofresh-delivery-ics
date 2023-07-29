#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler

from config import icsfile

from flask import Flask, send_file


from functions import create_ics, fetch_hf_data, get_deliveries, scheduler


fetch_hf_data()
scheduler.start()

app = Flask(__name__)

@app.route('/' + icsfile, methods=["GET"])
def serve_ics():
    return send_file(
            icsfile,
            as_attachment=True)
