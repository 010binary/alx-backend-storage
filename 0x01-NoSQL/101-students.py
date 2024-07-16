#!/usr/bin/env python3
"""
Python function that returns all students in a collection
"""

def top_students(mongo_collection):
    """
    2 level agg function.
    """
    students = mongo_collection.aggregate([
            {
                "$project":
                    {
                        "name": "$name",
                        "averageScore": {"$avg": "$topics.score"},
                    },
            },
            {
                "$sort":
                    {
                        "averageScore": -1
                    },
            },
    ])
    return students
