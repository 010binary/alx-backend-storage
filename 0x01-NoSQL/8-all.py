#!/usr/bin/env python3
"""
my first pyScript without pymongo
"""

def list_all(mongo_collection):
    """
    getting a list of all doc in a collection
    """
    return [doc for doc in mongo_collection.find()]
