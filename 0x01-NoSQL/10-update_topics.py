#!/usr/bin/env python3
"""
Python function that changes topic of the params
"""


def update_topics(mongo_collection, name, topics):
    """
    Change the topic of the passed params
    """
    return mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
    )
