#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import flask as fl
from flask_frozen import Freezer
import os
import sys
import csv
import codecs
import cStringIO

app = fl.Flask(__name__)
freezer = Freezer(app)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
        
def read_tos_file(filename):
    line_list = []
    with open(filename, 'rb') as csvfile:
        reader = UnicodeReader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            line = unicode(row[3])
            line_list.append(line)
    return line_list

    
@app.route('/tos/')
def hello():
    privacy_file = os.path.join('data', "150213 Como's Adventure 법률 문서 - Privacy Policy.csv")
    privacy_lines = read_tos_file(privacy_file)
    
    tos_file = os.path.join('data', "150213 Como's Adventure 법률 문서 - Terms of Service.csv")
    tos_lines = read_tos_file(tos_file)
    
    title = "Como"
    return fl.render_template('tos.html', privacy_lines=privacy_lines, tos_lines=tos_lines, title=title)
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug=True)
    else:
        if sys.argv[1] == 'freeze':
            freezer.freeze()
        else:
            print("unknown command")
            exit()