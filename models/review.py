#!/usr/bin/python3

"""
The module that creates Review class
"""

from .base_model import BaseModel


class Review(BaseModel):
    """
    A class that manages the public class attributes of Review
    """
    place_id = ""
    user_id = ""
    text = ""
