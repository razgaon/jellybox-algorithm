import datetime 

time_blocks = []
for num in range(24):
    time_blocks.append((datetime.time(num,0,0), datetime.time(num,59,59))) 

class Preferences:

    def __init__(self, energy_preferences, sleep_start, sleep_end):
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
        return self.energy_preferences

if __name__ == "__main__":
    start = datetime.time(0,0,0)
    end = datetime.time(7,30,0)
    pref = Preferences([3,3,3,3,3,3], start, end)
    print(pref.get_energy_pref())