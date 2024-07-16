#!/usr/bin/env python3
"""
Python function that inserts a new document (row in the db
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new row, remember kwargs spread the content
    """
    return mongo_collection.insert_one(kwargs).inserted_id
