#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple http server for testing/debugging the web-UI

open http://localhost:8080/
add the following query params for TX and/or 900Mhz testing
    isTx
    sx127x
"""

from external.bottle import route, run, response, request
from external.wheezy.template.engine import Engine
from external.wheezy.template.ext.core import CoreExtension
from external.wheezy.template.loader import FileLoader

net_counter = 0
isTx = False
sx127x = False

def apply_template(mainfile):
    global isTx, sx127x
    engine = Engine(
        loader=FileLoader(["html"]),
        extensions=[CoreExtension("@@")]
    )
    template = engine.get_template(mainfile)
    data = template.render({
            'VERSION': 'testing (xxxxxx)',
            'PLATFORM': '',
            'isTX': isTx,
            'sx127x': sx127x
        })
    return data

@route('/')
def index():
    global net_counter, isTx, sx127x
    net_counter = 0
    isTx = 'isTx' in request.query
    sx127x = 'sx127x' in request.query
    response.content_type = 'text/html; charset=latin9'
    return apply_template('index.html')

@route('/elrs.css')
def elrs():
    response.content_type = 'text/css; charset=latin9'
    return apply_template('elrs.css')

@route('/scan.js')
def scan():
    response.content_type = 'text/javascript; charset=latin9'
    return apply_template('scan.js')

@route('/mui.js')
def mui():
    response.content_type = 'text/javascript; charset=latin9'
    return apply_template('mui.js')

@route('/hardware.html')
def hradware_html():
    response.content_type = 'text/html; charset=latin9'
    return apply_template('hardware.html')

@route('/hardware.js')
def hardware_js():
    response.content_type = 'text/javascript; charset=latin9'
    return apply_template('hardware.js')

@route('/config')
def options():
    response.content_type = 'application/json; charset=latin9'
    return {
        "options": {
            'uid': [1,2,3,4,5,6],
            'wifi-on-interval': 60,
            "tlm-interval": 240,
            "fan-runtime": 30,
            "no-sync-on-arm": False,
            "uart-inverted": True,
            "unlock-higher-power": False,
            "rcvr-uart-baud": 400000,
            "rcvr-invert-tx": False,
            "lock-on-first-connection": True,
            "domain": 1,
            "button-colors": [-1,255*256],
            "button-actions": [
                {
                    "button": 1,
                    "is-long-press": False,
                    "count": 3,
                    "action": "bind"
                },
                {
                    "button": 1,
                    "is-long-press": True,
                    "count": 0,
                    "action": "inc-power"
                },
                {
                    "button": 2,
                    "is-long-press": False,
                    "count": 2,
                    "action": "vtx-channel"
                },
                {
                    "button": 2,
                    "is-long-press": True,
                    "count": 0,
                    "action": "send-vtx"
                }
            ]
        },
        "config": {
            "ssid":"ConnectedNetwork",
            "mode":"STA",
            "modelid":255,
            "pwm":[512,1536,2048,3584,4608],
            "product_name":
            "Generic ESP8285 + 5xPWM 2.4Ghz RX",
            "lua_name":"ELRS+PWM 2400RX",
            "reg_domain":"ISM2G4"
        },
        "button-funcs": ["bind", "inc-power", "vtx-channel", "send-vtx", "vtx-band", "wifi"]
    }

@route('/networks.json')
def mode():
    global net_counter
    net_counter = net_counter + 1
    if (net_counter > 3):
        return '["Test Network 1", "Test Network 2", "Test Network 3", "Test Network 4", "Test Network 5"]'
    return '[]'

if __name__ == '__main__':
    run(host='localhost', port=8080)
