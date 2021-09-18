import datetime 

#time blocks for each hour in a day
time_blocks = []
for num in range(24):
    time_blocks.append((datetime.time(num,0,0), datetime.time(num,59,59))) 

class Preferences:

    def __init__(self, energy_preferences, sleep_start, sleep_end):
        '''
        Initialize a Preferences object
        
        Inputs:
        * energy_preferences (list): energy preferences for early morning, late morning, afternoon, early evening, late evening, and night
        * sleep_start (datetime obj): the starting time for sleep
        * sleep_end (datetime obj): the ending time for sleep
        '''
        self.sleep_start = sleep_start
        self.end_start = sleep_end

        #list of preferences for energy by early morning (4 - 8), late morning (8 - 12), afternoon (12 - 4), early evening (4 - 8), late evening (8 - 12), night (12 - 4)
        #on a scale from 0 to 5
        energies = []
        for pref in energy_preferences:
            energies.append(pref)
            energies.append(pref)
            energies.append(pref)
            energies.append(pref)
        self.energy_preferences = energies
        
        for i in range(len(time_blocks)):
            if (sleep_start <= time_blocks[i][1]) and  (sleep_end >= time_blocks[i][0]):
                self.energy_preferences[i] = 0

    def get_energy_pref(self):
        '''
        Get a energy preferences
        
        Output:
        * energy_preferences (list): energy preferences on an hourly basis for a day
        '''
        return self.energy_preferences

if __name__ == "__main__":
    start = datetime.time(0,0,0)
    end = datetime.time(7,30,0)
    pref = Preferences([3,3,3,3,3,3], start, end)
    print(pref.get_energy_pref())