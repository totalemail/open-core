#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages

from db.models import Header

MAX_SUBJECTS_DISPLAYED = 10


class IndexView(TemplateView):
    """Base search page."""

    def get(self, request):
        """Handle get requests."""
        template_name = 'vote/vote-index.html'

        headers = Header.objects.all()[:100]
        subject_data = []

        for header in headers:
            if header.subject != 'N/A':
                subject_data.append({'subject': header.subject, 'link': '/{}'.format(header.link), 'id': header.id})

        if len(subject_data) > MAX_SUBJECTS_DISPLAYED:
            selected_subjects = random.sample(subject_data, MAX_SUBJECTS_DISPLAYED)
        else:
            selected_subjects = subject_data

        return render(request, template_name, {"subjects": json.dumps(selected_subjects)})
