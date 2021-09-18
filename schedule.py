from preferences import *

HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
BLOCKS_PER_HOUR = 4

class Schedule:
    def __init__(self, start_date, end_date):
        self.days = self.generate_blank_schedule(start_date, end_date)
        self.tasks = []

    def generate_blank_schedule(self, start_date, end_date):
        delta = datetime.timedelta(days = 1)
        days = {}
        while start_date <= end_date:
            days[start_date] = Day()
            start_date += delta
        return days

    def add_task(self, task):
        self.tasks.append(task)
        for day, day_schedule in self.days.items():
            if day < task.start_date:
                continue
            if day > task.due_date:
                break
            is_time_available, start_time = day_schedule.find_time_for_task(task)

            if is_time_available:
                hour, block = start_time
                day_schedule.schedule_task(task, hour, block)
                return
    
    def account_sleep(self, energy_preferences):
        task = Task('sleep', 5, 60)
        for time, block_energy in enumerate(energy_preferences):
            if block_energy == 0:
                for day_schedule in self.days.values():
                    day_schedule.schedule_task(task, time, 0)

    def display_schedule(self):
        for day, day_schedule in self.days.items():
            print(day_schedule.times)

class Day:
    def __init__(self):
        self.times = [[None] * BLOCKS_PER_HOUR for _ in range(HOURS_PER_DAY)]

    def get_open_times(self):
        open_times = [set() for _ in range(HOURS_PER_DAY)]
        for i in range(HOURS_PER_DAY):
            for j in range(BLOCKS_PER_HOUR):
                if not self.times[i][j]:
                    open_times[i].add(j)
        return open_times

    def find_time_for_task(self, task):
        start_time = (0, 0)
        curr_duration = 0
        open_times = self.get_open_times()
        restart_time = False
        for i, hour in enumerate(open_times):
            for block in [0, 1, 2, 3]:
                if curr_duration >= task.duration:
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

    def schedule_task(self, task, hour, block):
        minutes_per_block = MINUTES_PER_HOUR / BLOCKS_PER_HOUR
        for i in range(int(task.duration // minutes_per_block)):
            self.times[hour][block] = task.name
            if block >= BLOCKS_PER_HOUR - 1:
                hour += 1
                block = 0
            else:
                block += 1

class Task:
    def __init__(self, name, priority, duration, difficulty=0, start_date=None, due_date=None):
        self.name = name
        self.priority = priority
        self.difficulty = difficulty
        self.start_date = start_date
        self.due_date = due_date
        self.duration = duration

sleep_start = datetime.time(0,0,0)
sleep_end = datetime.time(7,30,0)
pref = Preferences([3,3,3,3,3,3], sleep_start, sleep_end)

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 1, 4)
test_schedule = Schedule(start_date, end_date)
test_task = Task('testing', 1, 75, 1, datetime.date(2020, 1, 2), datetime.date(2020, 1, 3))
test_schedule.add_task(test_task)
test_schedule.account_sleep(pref.get_energy_pref())
test_schedule.display_schedule()
