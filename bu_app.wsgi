#! /usr/bin/python3
import sys
import os.path
from bu_app import app as application


this_dir = os.path.dirname(__file__)
sys.path.insert(0, this_dir)


if __name__ == "__main__":
    application.run(debug=True)
