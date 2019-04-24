
from flaskext.mysql import MySQL
from flask import Flask
import pandas as pd
import numpy as np


def Movies():
    

    movies = [
        {
            'id':1,
            'title':'Harry Potter 1: shenme gui stone',
            'description': 'It is about Harry Potter',
            'author': 'JK Rolling',
            'create_date': '1999-01-01'

        },
        
        {
            'id':2,
            'title':'Harry Potter 2: the big-ass snake',
            'description': 'It is about Harry Potter again',
            'author': 'JK Rolling',
            'create_date': '2000-01-01'

        }


    ]

    return movies