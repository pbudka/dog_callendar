import os
import sys
import pickle
from pathlib import Path
from gcalendar import Calendar
import datetime
import time
from messages import message, switchLang

class DogWalker:
    # walking dog under 1m ignored
    MIN_WALK = 10
    # other slots
    credentials = calendar = passwStr = state = None
    passw = newPassw = loggedName = exitting = None
    print = None
    pesOut={}

    def __init__(self, calName, printFunc,exitting):
        self.calendar = Calendar('Codi')
        self.print = printFunc
        self.exitting = exitting
        self.loadCredentials()
        self.logout()

    def resetCredentials(self):
        self.credentials = {'P':11, 'R':2, 'B':3, 'M':1}
        self.dumpCredentials()

    def credentialsName(self):
        home_dir = os.path.expanduser('~')
        return os.path.join(home_dir, '.credentials', 'passwords')

    def loadCredentials(self):
        credentials = self.credentialsName()
        if Path(credentials).exists():
            with open(credentials, 'rb') as f:
                self.credentials = pickle.load(f)
        else:
            self.credentials = {'P':11, 'R':2, 'B':3, 'M':1}

    def dumpCredentials(self):
        with open(self.credentialsName(), 'wb') as f:
            pickle.dump(self.credentials, f)

    def userWith(self, password):
        for name, passw in self.credentials.items():
            if passw == password:
                return name

    def walking(self):
        if self.pesOut:
            return list(self.pesOut.keys())[0]
        else:
            return ''

    def calStat(self, dFrom, dTo):
        events = self.calendar.events(dFrom, dTo)
        id = 0
        str=''
        if events:
            for summary, duration in self.calendar.group():
                if summary in {'P','M','B','R'}:
                    s = int(duration.total_seconds())
                    str += '{:s}{:3d}:{:02d} '.format(summary, s // 3600, s % 3600 // 60)
                    id +=1
                    if (id == 2): str +='\n'
            self.print(str,8)
        else:
            self.print('no_record',3)
            
    def processChar(self,ch):
        if self.start(ch) != False: return 
        if self.logging(ch) != False: return 
        if self.logged(ch) != False: return 
        if self.confirmFraud(ch) != False: return 
        if self.newPassword(ch) != False: return 
        if self.confirmPassw(ch) != False: return
        if self.loginAs(ch) != False: return

    def start(self, ch):
        if self.state != 'start':
            return False
        if ch == 0:
            self.passw = 0
            self.state = 'logging'
            self.passwStr = message('type_password')
            self.print(self.passwStr)
        elif ch == 1:
            self.print('week_stat')
            delta = datetime.timedelta(days=7)
            now = datetime.datetime.utcnow()
            self.calStat(now-delta, now)
            self.logout()
        elif ch == 2:
            self.print('month_stat')
            delta = datetime.timedelta(days=30)
            now = datetime.datetime.utcnow()
            self.calStat(now-delta, now)
            self.logout()
        elif self.exitting and ch == 3:
            self.exit()

    def logging(self,ch):
        if self.state != 'logging': return False
        if ch == 0:
            name = self.userWith(self.passw)
            if name == None:
                self.print('wrong_password',2)
                self.logout()
            else:
                self.logon(name)        
        else:
            self.passwStr += '*'
            self.print(self.passwStr)
            self.passw = self.passw * 10 + ch

    def logon(self,name):
        walker = self.walking()
        self.state = 'logged'
        self.loggedName = name
        if walker == '':
            self.print('hi_dog_home',2,self.loggedName)
        else:
            self.print('hi_dog_out',2, self.loggedName, walker)
        if self.loggedName == walker:
            self.print('logged_back')
        elif walker == '':
            self.print('logged_go')
        else:
            self.print('logged_blame',None,walker)    

    def logged(self,ch):
        if self.state != 'logged': return False
        if ch == 1:
            self.OutBackFraud()
        elif ch == 0:
            self.logout()
        elif ch == 2:
            self.passw = 0
            self.state = 'newPassw'
            self.passwStr = message('new_password')
            self.print(self.passwStr)
        elif ch == 3:
            if self.loggedName == 'P':
                self.print('log_as')
                self.state = 'login_as'
            else:
                switchLang()
                self.logout()
     
    def OutBackFraud(self):
        walker = self.walking()
        if self.loggedName == walker:
            dur = int((datetime.datetime.utcnow() - self.pesOut[walker]).total_seconds())
            if dur > self.MIN_WALK:
                self.print('recording',5,walker, dur // 3600, dur % 3600 // 60)
                self.calendar.insert(self.loggedName, self.pesOut[walker], datetime.datetime.utcnow())
            else:
                self.print('no_record',5,walker) 
            self.pesOut.clear()
            self.logout()
        elif walker == '':
            self.pesOut[self.loggedName]=datetime.datetime.utcnow()
            self.logout()
        else: # state != walker
            self.print('blame',None,walker)
            self.state = 'confirm_fraud'

    def loginAs(self,ch):
        if self.state != 'login_as': return False
        if ch == 1:
            self.logon('R')
        elif ch == 2:
            self.logon('B')
        elif ch == 3:
            self.logon('M')
            
    def confirmFraud(self,ch):
        if self.state != 'confirm_fraud': return False
        walker = self.walking()
        if ch == 1:
            self.print('blamed', 2, self.loggedName, walker)
            self.calendar.insert(walker+' x '+self.loggedName, self.pesOut[walker] ,
                                     datetime.datetime.utcnow())
            self.pesOut.clear()
        else:
            self.print('canceled')
        self.logout()

    def newPassword(self,ch):
        if self.state != 'newPassw': return False
        if ch == 0:
            name = self.userWith(self.passw)
            if name == None:
                self.passwStr = message('again_password')
                self.print(self.passwStr)
                self.newPassw = self.passw
                self.passw = 0
                self.state = 'confirm_passw'
            else:
                self.passw = 0
                self.print('wrong_password')
                self.passwStr = message('again_password')
        else:
            self.passwStr += '*'
            self.print(self.passwStr)
            self.passw = self.passw * 10 + ch

    def confirmPassw(self,ch):
        if self.state != 'confirm_passw':
            return False
        if ch == 0:
            if self.newPassw == self.passw:
                self.print('storing_password',3,self.loggedName)
                self.credentials[self.loggedName]=self.passw
                self.dumpCredentials()
            else:
                self.print('wrong_password',3)
            self.logout()              
        else:
            self.passwStr += '*'
            self.print(self.passwStr)
            self.passw = self.passw * 10 + ch

    def logout(self):
        self.loggedName = None
        self.passw = self.newPassw = 0
        self.state='start'
        walker = self.walking()
        if walker:
            self.print('dog_out', None,walker)
        else:                    
            self.print('dog_home')

    def exit(self):
        self.dumpCredentials()
        self.print('bye',4)
        sys.exit(0)
