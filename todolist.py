# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
num_to_day = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}

class task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while 1:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    i = int(input())
    print("")
    if i==0:
        print("Bye!")
        break
    elif i == 1:
        rows = session.query(task).filter(task.deadline == datetime.today()).all()
        print("Today "+ str(datetime.today().day)+" "+datetime.today().strftime('%b')+":")
        if len(rows) == 0:
            print("Nothing to do!")
            print("")
            continue
        for j in range(len(rows)):
            print(str(j+1)+". "+repr(rows[j]))
    elif i == 2:
        rows = session.query(task).filter(task.deadline - datetime.today().date() < timedelta(days=7)).all()
        for j in range(7):
            day = datetime.today() + timedelta(days=j)
            print(num_to_day[day.weekday()]+" "+str(day.day) +" "+day.strftime('%b')+":")
            count = 0
            for row in rows:
                if row.deadline == day.date():
                    count +=1
                    print(str(count)+". "+repr(row))
            if count==0:
                print("Nothing to do!")
            print("")
    elif i == 3:
        rows = session.query(task).order_by(task.deadline).all()
        count = 0
        print("All tasks:")
        if len(rows)==0:
            print("Nothing to do!\n")
            continue
        for row in rows:
            count += 1
            month = row.deadline.strftime('%b')
            day = row.deadline.day
            print("{}. {}. {} {}".format(str(count),row.task,day,month))
        print("")
    elif i == 4:
        rows = session.query(task).filter(task.deadline < datetime.today()).order_by(task.deadline).all()
        count = 0
        if len(rows)==0:
            print("No missed tasks")
        else:
            print("Missed tasks:")
            for row in rows:
                count += 1
                month = row.deadline.strftime('%b')
                day = row.deadline.day
                print("{}. {}. {} {}".format(str(count),row.task,day,month))
        print("")
    elif i == 5:
        new_task = input("Enter task\n")
        new_deadline = input("Enter dealine\n")
        deadline = datetime(int(new_deadline[0:4]),int(new_deadline[5:7]),int(new_deadline[8:]))
        rows = session.query(task).all()
        new_row = task(id =len(rows)+1, task=new_task, deadline = deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print("")
    elif i == 6:
        rows = session.query(task).order_by(task.deadline).all()
        count = 0
        if len(rows) == 0:
            print("Nothing to delete")
        else:
            print("Chose the number of the task you want to delete:")
            for row in rows:
                count += 1
                month = row.deadline.strftime('%b')
                day = row.deadline.day
                print("{}. {}. {} {}".format(str(count),row.task,day,month))
            number = int(input())
            session.delete(rows[number-1])
            session.commit()
            print("The task has been deleted!")
        print("")
