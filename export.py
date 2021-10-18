"""
MODIFIED BY CACTUS
THANKS TO THE ORIGINAL AUTHOR
"""
"""
Mon 13 Jul 2020 19:08:05 CEST

Export Google Keep notes to a markdown file.

After obtaining your Google Keep data from https://takeout.google.com/
unzip the folder and cd into it.

Copy this file in that folder and run:
    python export.py > exported.md

or, if you prefer a simple txt file:
    python export.py > exported.txt

"""

import os
import json
import datetime
import pathlib


PRINT_RAW = False
PRINT_PRETTY_JSON = True


PRINT_DATE = True
RIGHT_ALIGN_DATE = True


class Note:
    def __init__(self, filename, data):
        self._name = filename.replace('.json', '')
        self._title = data['title']
        self._raw_date = data['userEditedTimestampUsec']
        self._date = datetime.datetime.fromtimestamp(self._raw_date/1_000_000)
        self._isTrashed = data['isTrashed']
        self._isArchived = data['isArchived']
        self._isList = True if 'listContent' in data else False
        if self._isList:
            tmp = ""
            for i in data['listContent']:
                tick = 'x' if i['isChecked'] else ' '
                tmp += "- [{}] {}\n".format(tick, i['text'])
            self._content = tmp; del tmp
        else:
            self._content = data['textContent'] 

    def _format_date(self):
        # return a date of this type: Tuesday November 03, 2015, 03:20:51
        return self._date.strftime("%A %B %d, %Y, %H:%M") # https://strftime.org/

    def isTrashed(self):
        return self._isTrashed

    def __repr__(self):
        ans  = "## {} {}\n".format(self._name, "(Archived)" if self._isArchived else "")
        
        if PRINT_DATE:
            if RIGHT_ALIGN_DATE: 
                ans += "<div style='text-align: right'>"

            ans += "Last edited: {}\n".format(self._format_date())

            if RIGHT_ALIGN_DATE: 
                ans += "</div>\n"

        ans += "\n"

        if self._title != '': 
            ans += "Title: {}\n".format(self._title)
        
        ans += self._content
        return ans




if __name__ == '__main__':

    root_folder = pathlib.Path('Keep')
    notes = [filename for filename in os.listdir(root_folder) if '.json' in filename]

    notes_list = []
    for filename in notes:
        with open(pathlib.Path("{}/{}".format(root_folder, filename)), 'r') as json_file:
            data = json.load(json_file)
            
            if PRINT_RAW:
                if PRINT_PRETTY_JSON:
                    print(json.dumps(data, indent=4, sort_keys=True)); print()
                else:
                    print("{}\n\n".format(data))

        note = Note(filename, data)
        if not note.isTrashed():
            notes_list.append(note)

    del notes


    #sorted_notes = sorted(notes_list, key=lambda x: x._raw_date, reverse=True)
    sorted_notes = sorted(sorted(notes_list, key=lambda x : x._isArchived), key=lambda x : x._raw_date, reverse = True)  
    

    f = open('Google Keep Notes Archive.md','w')
    print("# Google Keep Notes Archive", file = f)
    print("###### Total notes = {}  – sorted by (Last update, archived/not archived)\n\n".format(len(sorted_notes)), file = f)
    for i in sorted_notes:
        print("{}\n".format(i), file = f)
        print("---\n\n", file = f)