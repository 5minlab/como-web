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

def read_tos_file(filename, game_name, url):
    line_list = []
    with open(filename, 'rb') as csvfile:
        reader = UnicodeReader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            line = unicode(row[3])
            line_list.append(line)

    def replace_game_name(text):
        src_txt = "Como"
        dst_txt = game_name
        return text.replace(src_txt, dst_txt)

    def replace_url(text):
        src_txt = "http://5minlab.github.io/como-web/tos/"
        dst_txt = url
        return text.replace(src_txt, dst_txt)

    line_list = [replace_game_name(replace_url(line)) for line in line_list]

    return line_list

@app.route('/')
def index():
    return fl.render_template('index.html')

@app.route('/tos/')
def tos_como():
    title = "Como"
    url = "http://5minlab.github.io/como-web/tos/"
    return render_tos(title, url)

@app.route('/tos/brex.html')
def tos_brex():
    title = "Brex"
    url = "http://5minlab.github.io/como-web/tos/brex.html"
    return render_tos(title, url)

@app.route('/tos/hungry-mates.html')
def tos_hungry_mates():
    title = "Hungry Mates"
    url = "http://5minlab.github.io/como-web/tos/hungry-mates.html"
    return render_tos(title, url)

@app.route('/tos/slime-slasher.html')
def tos_slime_slasher():
    title = 'Slime Slasher'
    url = "http://5minlab.github.io/como-web/tos/slime-slasher.html"
    return render_tos(title, url)

def render_tos(title, url):
    privacy_file = os.path.join('data', "150213 Como's Adventure 법률 문서 - Privacy Policy.csv")
    privacy_lines = read_tos_file(privacy_file, title, url)

    tos_file = os.path.join('data', "150213 Como's Adventure 법률 문서 - Terms of Service.csv")
    tos_lines = read_tos_file(tos_file, title, url)

    return fl.render_template('tos.html', privacy_lines=privacy_lines, tos_lines=tos_lines, title=title)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug=True, host='0.0.0.0')
    else:
        if sys.argv[1] == 'freeze':
            freezer.freeze()
        else:
            print("unknown command")
            exit()
