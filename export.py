"""
Mon 13 Jul 2020 19:08:05 CEST

Export Google Keep notes to a txt file.

After obtaining your Google Keep data from https://takeout.google.com/
unzip the folder and cd into it.

Copy this file in that folder and run, e.g.
    python export.py > exported.txt

, alternatively feel free to edit this file to achieve what fits best for you.

"""


import json
import sys
import os
import datetime 



class Note:
    """docstring for Note"""
    def __init__(self, filename, data):
        self._name = filename.replace('.json', '')
        self._title = data['title']
        self._raw_date = data['userEditedTimestampUsec']
        self._date = datetime.datetime.fromtimestamp(self._raw_date/1_000_000)
        self._isList = True if 'listContent' in data else False
        if not self._isList:
            self._content = data['textContent'] 
        else:
            tmp = ""
            for i in data['listContent']:
                tick = '+' if i['isChecked'] == True else ' '
                tmp += "- [{}] {}\n".format(tick, i['text'])
            self._content = tmp


    def _format_date(self):
        # e.g.: Tuesday November 03, 2015, 03:20:51 PM
        # tnx https://strftime.org/
        return self._date.strftime("%A %B %d, %Y, %I:%M:%S %p")

    def __repr__(self):
        ans = ""
        ans += "### {}\n".format(self._name)
        ans += "Last edited: {}\n".format(self._format_date())
        if self._title != '': ans += "Title: {}\n".format(self._title)
        ans += self._content
        return ans




if __name__ == '__main__':

    root_folder = 'Keep'

    notes = os.listdir(root_folder)
    notes = [filename for filename in notes if '.json' in filename]

        
    notes_list = []
    for filename in notes:
        with open("{}/{}".format(root_folder, filename), 'r') as json_file:
            data = json.load(json_file)

        notes_list.append(Note(filename, data))

    del notes

    sorted_notes = sorted(notes_list, key=lambda x: x._raw_date, reverse=True)

    [print("{}\n\n\n".format(i)) for i in sorted_notes]

