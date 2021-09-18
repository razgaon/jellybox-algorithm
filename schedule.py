from preferences import *

HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
BLOCKS_PER_HOUR = 4
MINUTES_PER_BLOCK = 60
BLOCK_LENGTH = 15

class Schedule:

    def __init__(self, schedule_start_date, schedule_end_date, preferences, events = [], tasks = []):
        '''
        Initialize a Schedule object
        
        Inputs:
        * start_date (datetime obj): the starting date for the schedule
        * end_date (datetime obj): the ending date for the schedule
        * preferences (dictionary): sleep and energy preferences
        * eveent
        '''
        self.days = self.generate_blank_schedule(schedule_start_date, schedule_end_date)
        self.sleep_start = preferences[0]['sleep_start']
        self.sleep_end = preferences[0]['sleep_end']
        self.preferences = Preferences(preferences[0]['energy_levels'], preferences[0]['sleep_start'], preferences[0]['sleep_end'])
        self.events = events #deepcopy
        self.tasks = tasks #deepcopy
        self.initialize_tasks()

    def initialize_tasks(self):
        for task in self.tasks:
            print(task)
            task_obj = Task(task["name"], task["chunks"], task["priority"], task["duration"], task["difficulty"], task["start_date"], task["end_date"])
            self.add_task(task_obj)

    def generate_blank_schedule(self, start_date, end_date):
        '''
        Generate a blank schedule
        
        Input:
        * start_date (datetime obj): the starting date for the schedule
        * end_date (datetime obj): the ending date for the schedule
        
        Output:
        * days (dict): dictionary mapping datetime objects to Day objects 
        '''
        delta = datetime.timedelta(days = 1)
        days = {}
        curr_date = start_date
        while curr_date <= end_date:
            days[curr_date] = Day(curr_date)
            curr_date += delta
        return days

    # def account_sleep(self):
    #     '''
    #     Block out time for sleep in the schedule
    #     '''
    #     event = Event('sleep', 6, 0, None, self.sleep_start, self.sleep_end) ##fix to include date
    #     for time, block_energy in enumerate(self.preferences.energy_preferences):
    #         if block_energy == 0:
    #             for day_schedule in self.days.values():
    #                 day_schedule.schedule_event(event, time, 0)
    #                 self.events.append(event)
    
    def sort_tasks(self):
        '''
        Sort tasks by formula
        '''
        tasks = []
        for task in self.tasks:
            num = .6 * task.priority + .4 * task.difficulty
            tasks.append((task, num))
        tasks.sort(key=lambda x:x[1])
        
        self.tasks = []
        for task in tasks:
            self.tasks.append(task[0])
    
    def sort_events(self):
        '''
        Sort events by formula
        '''
        events = []
        for event in self.events:
            num = .6 * event.priority + .4 * event.difficulty
            tasks.append((event, num))
        event.sort(key=lambda x:x[1])
        
        self.events = []
        for event in events:
            self.events.append(event[0])

    def add_task(self, task, hasSorted = False):
        '''
        Add a task into the schedule
        
        Input:
        * task (Task obj): task information
        '''
        block_size = MINUTES_PER_BLOCK if task.chunks else task.duration
        self.tasks.append(task)
        remaining_duration = task.duration
        for day, day_schedule in self.days.items():
            if day < task.start_date:
                continue
            if day > task.due_date:
                break
            
            while remaining_duration > 0:
                curr_duration = block_size if remaining_duration >= block_size else remaining_duration
                is_time_available, start_time = day_schedule.find_time_for_task(curr_duration)

                if not is_time_available:
                    break 

                if is_time_available:
                    remaining_duration -= curr_duration
                    hour, block = start_time
                    event = day_schedule.schedule_event(task, hour, block, curr_duration)
                    self.events.append(event)

            if remaining_duration == 0:
                return
        
        #not able to add
        if hasSorted == False:
            self.sort_tasks()
            hasSorted = True
            for task in self.tasks:
                self.add_task(task, hasSorted)
        else:
            return 'cannot add task!'
    
    def account_sleep(self):
        '''
        Block out time for sleep in the schedule
        
        Input:
        * energy_preferences (list): energy preferences (0 - least to 5 - most) for every hour in the day
        '''
        task = Task('sleep', 5, 60)
        for time, block_energy in enumerate(self.preferences.energy_preferences):
            if block_energy == 0:
                for day_schedule in self.days.values():
                    event = day_schedule.schedule_event(task, time, 0, task.duration)
                    self.events.append(event)

    def display_schedule(self):
        '''
        Display the schedule as a 2D list
        '''
        for day, day_schedule in self.days.items():
            print(day_schedule.times)

class Day:
    def __init__(self, date):
        '''
        Initialize a Day object

        Inputs:
        * date (date obj): date that object represents
        '''
        self.date = date
        self.times = [[None] * BLOCKS_PER_HOUR for _ in range(HOURS_PER_DAY)]

    def get_open_times(self):
        '''
        Get all available time blocks

        Inputs: None

        Output:
        * open_times (list): a list of 24 sets, one for each hour, containing the timeblocks within that hour that are 
        available; 0 = first fifteen minutes, 1 = second fifteen minutes, etc.
        '''
        open_times = [set() for _ in range(HOURS_PER_DAY)]
        for i in range(HOURS_PER_DAY):
            for j in range(BLOCKS_PER_HOUR):
                if not self.times[i][j]:
                    open_times[i].add(j)
        return open_times

    def find_time_for_task(self, duration):
        '''
        Finds first time block in which task can be scheduled

        Inputs: 
        * task (Task obj): task that is to be scheduled

        Output:
        * boolean representing whether or not a time block in which task can be fit is available
        * tuple in form (hour, block) denoting first hour and 15-minute block within that hour during which 
        the task can be scheduled; defaults to (0, 0) if not possible
        '''
        start_time = (0, 0)
        curr_duration = 0
        open_times = self.get_open_times()
        restart_time = False
        for i, hour in enumerate(open_times):
            for block in [0, 1, 2, 3]:
                if curr_duration >= duration:
                    return True, start_time
                if block in hour:
                    if restart_time:
                        start_time = (i, block)
                        restart_time = False
                    curr_duration += 15
                else:
                    curr_duration = 0
                    restart_time = True
        return False, (0, 0)

    def time_plus(self, time, timedelta):
        start = datetime.datetime(
            2000, 1, 1,
            hour=time.hour, minute=time.minute, second=time.second)
        end = start + timedelta
        return end.time()

    def schedule_event(self, task, hour, block, duration):
        '''
        Insert given task into schedule starting at designated hour and block.

        Inputs:
        * task (Task obj): the task to be scheduled
        * hour (int): the hour from 0 to 23 during which the task should be started
        * block (int): the block (0, 1, 2, etc) during the hour in which the task should be started

        Output: void
        '''
        date = self.date
        start_time = datetime.time(hour, block * BLOCK_LENGTH, 0)
        end_time = self.time_plus(start_time, datetime.timedelta(minutes = duration))
        minutes_per_block = MINUTES_PER_HOUR / BLOCKS_PER_HOUR
        for i in range(int(duration // minutes_per_block)):
            self.times[hour][block] = task.name
            if block >= BLOCKS_PER_HOUR - 1:
                hour += 1
                block = 0
            else:
                block += 1

        return Event(task.name, task.priority, task.difficulty, date, start_time, end_time)

class Task:
    def __init__(self, name, chunks = False, priority=1, duration=60, difficulty=0, start_date = None, due_date=None):
        '''
        Initializes a Task object

        Inputs:
        * name (str): name of task
        * chunks (boolean): can it be divided into chunks of time
        * priority (int): number from 1 (lowest) to 5 (highest) indicating priority level of task
        * duration (int): estimated time to complete task in minutes
        * difficulty (int): number from 1 (lowest) to 5 (highest) indicating difficulty of task
        * start_date (datetime obj): first day on which task can be completed
        * due_date (datetime obj): last day on which task can be completed
        '''
        self.name = name
        self.chunks = chunks
        self.priority = priority
        self.difficulty = difficulty
        self.start_date = start_date
        self.due_date = due_date
        self.duration = duration

class Event:
    def __init__(self, name, priority, difficulty=0, date=None, start_time=None, end_time=None):
        '''
        Initializes a Event object

        Inputs:
        * name (str): name of task
        * priority (int): number from 1 (lowest) to 5 (highest) indicating priority level of task
        * difficulty (int): number from 1 (lowest) to 5 (highest) indicating difficulty of task
        * date (date obj): the date it will be completed on
        * start_time (time obj): start time of event
        * end_time (time obj): end time of event
        '''
        self.name = name
        self.priority = priority
        self.difficulty = difficulty
        self.date = date
        self.start_time = start_time
        self.end_time = end_time


if __name__ == "__main__":
    preferences = [{
        'energy_levels' : [3,3,3,3,3,3],
        'sleep_start': datetime.time(0,0,0),
        'sleep_end': datetime.time(7,30,0),
    }]

    events = [
        {
            'name' : "pset", 
            'priority' : 1, 
            'difficulty' : 3, 
            'date': datetime.date(2020, 1, 4),
            'start_time' : datetime.time(8,0,0), 
            'end_time' : datetime.time(11,0,0)
        }
    ]

    tasks = [
        {
            'name' : "pset", 
            'chunks': False,
            'priority' : 1, 
            'difficulty' : 3, 
            'duration': 180,
            'start_date' : datetime.date(2020, 1, 4), 
            'end_date' : datetime.date(2020, 1, 6)
        },
        {
            'name' : "hw", 
            'chunks': True,
            'priority' : 5, 
            'difficulty' : 4, 
            'duration': 180,
            'start_date' : datetime.date(2020, 1, 4), 
            'end_date' : datetime.date(2020, 1, 6)
        }
    ]

    start_date = datetime.date(2020, 1, 3)
    end_date = datetime.date(2020, 1, 7)
    test_schedule = Schedule(start_date, end_date, preferences, events, tasks)
    print('hi')
    test_schedule.account_sleep()
    test_task = Task('testing', True, 1, 75, 1, datetime.date(2020, 1, 2), datetime.date(2020, 1, 3))
    test_schedule.add_task(test_task)
    test_schedule.display_schedule()
