HOURS_PER_DAY = 24
BLOCKS_PER_HOUR = 4

class Schedule:
    def __init__(self):
        self.weeks = []

    def add_task(self):
        pass

class Week(Schedule):
    def __init__(self):
        self.days = []

class Day(Week):
    def __init__(self):
        self.ordered_times = [0] * HOURS_PER_DAY * BLOCKS_PER_HOUR

class Task:
    def __init__(self, priority, start_date, difficulty, due_date):
        self.priority = priority
        self.difficulty = difficulty
        self.start_date = start_date
        self.due_date = due_date


def add_task_to_schedule(task, schedule):
    pass
        
