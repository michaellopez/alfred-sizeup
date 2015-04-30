#!/usr/bin/python
# encoding: utf-8

from __future__ import unicode_literals, print_function
import sys
import re
from os import listdir
from os.path import isfile, join

from workflow import Workflow, ICON_WARNING


icons_path = 'icons'
actions = [f for f in listdir(icons_path) if isfile(join(icons_path, f))]


def key_for_item(item):
    return '{}'.format(item['title'])


def main(wf):
    items = []
    for action in actions:
        uid = re.sub(r'align-|@2x.png', r'', action)
        title = re.sub(r'(upper|lower|next|prev|space)', r'\1 ', uid)
        #print('else if mode = "{0}" then\n\tdo action {1}'.format(uid, title.title()))
        items.append({'title': title.title(), 'valid': True, 'uid': uid, 'arg': uid, 'icon': join(icons_path, action)})

    query = None

    if len(wf.args):
        query = wf.args[0].strip()

    if query:
        items = wf.filter(query, items, key_for_item)

    if items:
        for item in items:
            wf.add_item(**item)
    else:
        wf.add_item('No items', icon=ICON_WARNING)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(normalization='NFD')
    sys.exit(wf.run(main))
