import datetime 

time_blocks = {
        'a' : (datetime.time(0,0,0), datetime.time(3,59,59)),
        'b' : (datetime.time(4,0,0), datetime.time(7,59,59)),
        'c' : (datetime.time(8,0,0), datetime.time(11,59,59)),
        'd' : (datetime.time(12,0,0), datetime.time(15,59,59)),
        'e' : (datetime.time(16,0,0), datetime.time(19,59,59)),
        'f' : (datetime.time(20,0,0), datetime.time(23,59,59))
    }

class Preferences:

    def __init__(self, energy_preferences, sleep_start, sleep_end):
        self.sleep_start = sleep_start
        self.end_start = sleep_end

        #list of preferences for energy by 4 hour time blocks
        #on a scale from 0 to 5
        self.energy_preferences = energy_preferences
        
        for i, block in enumerate(time_blocks):
            if (sleep_start <= time_blocks[block][1]) and  (sleep_end >= time_blocks[block][0]):
                self.energy_preferences[i] = 0

    def get_energy_pref(self):
        return self.energy_preferences

if __name__ == "__main__":
    start = datetime.time(0,0,0)
    end = datetime.time(7,30,0)
    pref = Preferences([3,3,3,3,3,3], start, end)
    print(pref.get_energy_pref())