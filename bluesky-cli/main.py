import getpass
import pprint
import views
from bluesky_session import BlueSkySession
import json

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
    timeline = session.getTimeline(10).json()
    inputtext = input('Enter a command: ')
    if inputtext == 'exit' or inputtext == 'quit':
        break
    if inputtext.startswith('show'):
        number_of_skeets = 1
        split_input = inputtext.split(' ')
        if len(split_input) > 1 and split_input[1].isdigit():
            number_of_skeets = int(split_input[1])
        if number_of_skeets > len(timeline['feed']):
            timeline = session.getTimeline(number_of_skeets).json()
        for i in range(number_of_skeets):
            views.renderSkeet(timeline['feed'][i])
        print('\n')
    if inputtext == "write":
        with open('skeets.json', 'w') as f:
            json.dump(timeline, f)