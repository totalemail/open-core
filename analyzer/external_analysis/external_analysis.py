#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submit email for analysis by external engines."""

import os

import zmq

from utility import utility

EXTERNAL_ANALYSIS_ENDPOINT = 'tcp://{}'.format(os.environ.get('EXTERNAL_ANALYSIS_ENDPOINT'))


def analyze_externally(email_object):
    """Submit the given email object to external sources."""
    if not utility.is_running_locally():
        context = zmq.Context()

        # Socket to send messages on
        sender = context.socket(zmq.PUSH)
        sender.connect(EXTERNAL_ANALYSIS_ENDPOINT)

        data = {'route': 'analysis', 'text': """{}""".format(email_object.full_text), 'id': email_object.id}

        sender.send_json(data, zmq.NOBLOCK)


def find_network_data(text, item_id, item_type, email_id):
    """Send the text to the analysis server to parse network data from it."""
    if not utility.is_running_locally():
        context = zmq.Context()

        # Socket to send messages on
        sender = context.socket(zmq.PUSH)
        sender.connect(EXTERNAL_ANALYSIS_ENDPOINT)

        sender.send_json(
            {
                'route': 'network_data',
                'type': item_type,
                'text': """{}""".format(text),
                'id': item_id,
                'email_id': email_id,
            },
            zmq.NOBLOCK,
        )
