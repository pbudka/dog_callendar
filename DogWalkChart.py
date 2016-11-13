from graphics import *
import datetime
import time
from gcalendar import Calendar

def weekBarChart():
    calendar = Calendar('Codi')
    names = {'P':[0,'yellow'],'M':[1,'green'],'B':[2,'blue'],'R':[3,'red']}
    startDate = calendar.str2time('2016-06-20')
    week = datetime.timedelta(days=7)
    now = datetime.datetime.utcnow()
    x= 0
    maxY=0.0
    win = GraphWin("WeekBarChart P M B R", 1000, 600)
    while(startDate < now):
        events = calendar.events(startDate, startDate+week)
        print(startDate)
        Text(Point(x+1,-1),startDate.strftime("%d.%b")).draw(win)
        startDate += week
        if events:
            for name, duration in calendar.group():
                if name in names:
                    d = duration.total_seconds() / 3600
                    if d > maxY: maxY = d
                    offset = names[name][0]
                    rec = Rectangle(Point(x+offset,0),Point(x+offset+1,d))
                    rec.setFill(names[name][1])
                    rec.draw(win)
        x = x + len(names) + 0.5
    dx = x / 10
    dy = maxY / 10 
    win.setCoords(-dx,-dy-2,x+dx,maxY+dy)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done
    
if __name__ == "__main__":
    weekBarChart()
