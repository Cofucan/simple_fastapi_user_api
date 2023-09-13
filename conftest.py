#!/bin/python3
"""This module sets the current folder as the working directory"""
import sys
import os

# Get the absolute path of the project's root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add the root directory to the Python path
sys.path.insert(0, ROOT_DIR)
