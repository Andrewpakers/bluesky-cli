import getpass
import pprint
import views
from bluesky_session import BlueSkySession
import json
from model import createSkeet

is_logged_in = False
username = ''
password = ''


views = views.viewsRenderer()
views.renderLogo()
timeline = None

while True:
    if not is_logged_in:
        print("Please log in")
        username = input("Username: ")
        try:
            password = getpass.getpass()
        except Exception as error:
            print('ERROR', error)
        session = BlueSkySession(username=username, password=password)
        is_logged_in = True
        timeline = session.getTimeline(5)
        # print(pprint.pprint(timeline.json()['feed']))
    rawTimeline = session.getTimeline(10).json()
    timeline = []
    for rawSkeet in rawTimeline['feed']:
        timeline.append(createSkeet(rawSkeet))
    inputtext = input('Enter a command: ')
    if inputtext == 'exit' or inputtext == 'quit':
        break
    if inputtext.startswith('show'):
        number_of_skeets = 1
        split_input = inputtext.split(' ')
        if len(split_input) > 1 and split_input[1].isdigit():
            number_of_skeets = int(split_input[1])
        if number_of_skeets > len(timeline):
            rawTimeline = session.getTimeline(number_of_skeets).json()
            timeline = []
            for rawSkeet in rawTimeline['feed']:
                timeline.append(createSkeet(rawSkeet))
        for i in range(number_of_skeets):
            views.renderSkeet(timeline[i])
        print('\n')
    if inputtext == "write":
        formattedSkeets = []
        for skeet in timeline['feed']:
            formattedSkeets.append(createSkeet(skeet))
        with open('newSkeets.json', 'w') as f:
            json.dump(formattedSkeets, f)
    if inputtext.startswith('dump'):
        split_input = inputtext.split(' ')
        if len(split_input) > 1:
            if split_input[1] == 'timeline':
                with open('timeline.json', 'w') as f:
                    json.dump(timeline, f)
            elif split_input[1] == 'rawTimeline':
                with open('rawTimeline.json', 'w') as f:
                    json.dump(rawTimeline, f)
        else:
            with open('timeline.json', 'w') as f:
                json.dump(timeline, f)