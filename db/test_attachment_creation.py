#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from test_resources import DefaultTestObject

TestData = DefaultTestObject()


@pytest.mark.django_db
def test_attachment_filename():
    """Create the same attachment with different file names and make sure the multiple file names are handled correctly."""
    attachment = TestData.create_attachment('test.xml')
    attachment.save()
    assert attachment.filename == 'test.xml'
    attachment = TestData.create_attachment('bingo.txt')
    attachment.save()
    assert attachment.filename == 'test.xml|||bingo.txt'


@pytest.mark.django_db
def test_duplicate_attachment_filenames_1():
    attachment = TestData.create_attachment('test.xml')
    attachment.save()
    assert attachment.filename == 'test.xml'

    # make sure duplicate attachment names are handled correctly
    attachment = TestData.create_attachment('test.xml')
    attachment.save()
    assert attachment.filename == 'test.xml'


@pytest.mark.django_db
def test_duplicate_attachment_filenames_2():
    attachment = TestData.create_attachment('test.xml')
    attachment.save()
    assert attachment.filename == 'test.xml'

    attachment = TestData.create_attachment('bingo.txt')
    attachment.save()
    assert attachment.filename == 'test.xml|||bingo.txt'

    attachment = TestData.create_attachment('test.xml')
    attachment.save()
    assert attachment.filename == 'test.xml|||bingo.txt'


@pytest.mark.django_db
def test_attachment_first_seen_and_modified():
    attachment1 = TestData.create_attachment('test.xml')
    attachment1.save()
    attachment2 = TestData.create_attachment('bingo.txt')
    attachment2.save()
    assert attachment1.first_seen == attachment2.first_seen
    assert attachment1.modified != attachment2.modified
    assert attachment1.modified < attachment2.modified
