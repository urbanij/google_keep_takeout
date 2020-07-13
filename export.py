# Mon 13 Jul 2020 19:08:05 CEST

import json
import sys
import os
import datetime 

root_folder = 'Keep'

notes = os.listdir(root_folder)
notes = [filename for filename in notes if '.json' in filename]


for filename in notes:
    print("### {} ".format(filename.replace('.json','')))
    with open("{}/{}".format(root_folder, filename), 'r') as json_file:
        data = json.load(json_file)



    date_time = datetime.datetime.fromtimestamp(data['userEditedTimestampUsec']/1_000_000)

    date_time_nice_format = date_time.strftime("%A %B %d, %Y, %I:%M:%S %p")

    print("Last edited: {}".format(date_time_nice_format))

    #print(data)

    if data['title'] != '': print("Title: {}".format(data['title']))

    if ('textContent' in data):
        print(data['textContent'])
    elif ('listContent' in data):
        #print(data['listContent'])
        for i in data['listContent']:
            tick = '+' if i['isChecked'] == True else ' '
            print("- [{}] {}".format(tick, i['text']))

    for _ in range(3): print()
