# https://developers.google.com/apis-explorer/#p/
# https://console.developers.google.com/apis/library?project=annular-system-132020
# https://developers.google.com/google-apps/calendar/quickstart/python
from __future__ import print_function
import httplib2
import os
import sys
import operator
# import dateutil.parser

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import time

class Calendar:
    """ Works with named google calendar """
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'
    calendar = None
    _calendarId = None
    _events = None

    def __init__(self,name):
        credentials = self._getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.calendar = discovery.build('calendar', 'v3', http=http)
        self.useCalendar(name)

    def useCalendar(self,name):
        """ switch to work with calendar NAME """
        return self._calendarId(name) != None

    def _getCredentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def _getCalendarId(self,name):
        l = self.calendar.calendarList().list().execute()
        for i in l.get('items',[]):
            if (i['summary'] == name):
                return i['id'];

    def _calendarId(self,name):
        self._calendarId = None
        for i in range(5):
            try:
                self._calendarId = self._getCalendarId(name)
            except:
                time.sleep(2)
                tb = sys.exc_info()[2]
                print(tb)
            else:
                return self._calendarId

    def events(self, fromDate, toDate):
        """ return events between FROMDATE and TODATE.
        Parameters can be string or date or datetime (see comment in insert). """
        if isinstance(toDate,str): tdt= self.str2time(toDate)
        else: tdt= toDate
        if isinstance(fromDate,str): fdt= self.str2time(fromDate)
        else: fdt= fromDate
        toDateS = self.time2str(tdt)
        fromDateS = self.time2str(fdt)
        eventsResult = self.calendar.events().list(
            calendarId=self._calendarId,
            timeMin=fromDateS, timeMax=toDateS,
            singleEvents=True, orderBy='startTime').execute()
        self._events = eventsResult.get('items', [])
        return self._events

    def group(self,events = None):
        """ groups EVENTS by 'summary' and agregates duration """
        groups = {}
        if(events==None): ev=self._events
        else: ev=events
        for event in ev:
            start = self.str2time(event['start'].get('dateTime', event['start'].get('date')))
            finish = self.str2time(event['end'].get('dateTime', event['end'].get('date')))
            duration = finish - start
            title = event['summary']
            if title in groups:
                groups[title] += duration
            else:
                groups[title] = duration
        return reversed(sorted(groups.items(), key=operator.itemgetter(1)))

    def str2time(self,strDate):
        try:
            return datetime.datetime.strptime(strDate[0:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.datetime.strptime(strDate[0:10], "%Y-%m-%d")

    def time2str(self,time):
        return time.isoformat() + 'Z' # 'Z' indicates UTC time

    def insert(self,title, fromTime, toTime):
        """ return events between FROMTIME and TOTIME.
        Parameters can be string or date or datetime.
        String can represent date: '2016-07-07' or datetime: '2016-07-07T00:00:00' """
        if isinstance(fromTime,str): fdt= self.str2time(fromTime)
        else: fdt= fromTime
        if isinstance(toTime,str): tdt= self.str2time(toTime)
        else: tdt= toTime
        self.calendar.events().insert(
            calendarId = self._calendarId,
            supportsAttachments=False,
            body = {"end": {"dateTime": self.time2str(tdt)},
                    "start": {"dateTime": self.time2str(fdt)},
                    "summary": title}).execute()

def main():
    """ main
    """
    calendar = Calendar('domaci')
    events = calendar.events('2016-04-01','2016-06-07')
    if (events != False):
        for summary, duration in calendar.group():
            print(duration,summary)
            
    delta = datetime.timedelta(hours=1, minutes=50, seconds=600)
    now = datetime.datetime.utcnow()
    calendar.insert('robin', now , now+delta)
        

if __name__ == '__main__':
    main()
