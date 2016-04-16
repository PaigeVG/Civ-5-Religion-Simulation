
# coding: utf-8

# In[1]:

import random
from hex_functs import *
from collections import defaultdict


# In[2]:

religion_stats = {  'long_reach':  {'distance': 13, 'pressure': 6},
                    'fast_spread': {'distance':  10, 'pressure': 9},
                    'vanilla':     {'distance':  10, 'pressure': 6},
                    'atheist':     {'distance':  10, 'pressure': 0},
                 }


# In[14]:

class City:
    def __init__(self, name, x=0, y=0, z=0, initial_population=5, holy_city=None):
        self.name = name
        self.position = Hex(x, y, z)
        self.citizens = defaultdict(lambda:0)
        self.pressures = defaultdict(lambda:0)
        self.reachable_cities = set()
        self.holy_city = holy_city
        self.main_religion = 'atheist'
        
        self._initialize_atheists(initial_population)
        self._set_main_religion()

    def send_pressures(self):
        self._set_main_religion()
        
        if self.main_religion != 'atheist':
            for city in self.reachable_cities:
                city._receive_pressure(self.main_religion)

    def update(self):
        if self.holy_city:
            self.pressures[self.holy_city] += 30
        self._flip_citizens()
                
    def _receive_pressure(self, religion):
        self.pressures[religion] += religion_stats[religion]['pressure']

    def _total_citizens(self):
        return sum(self.citizens.values())
    
    def _initialize_atheists(self, population):
        self.citizens['atheist'] = population
    
    def _flip_citizens(self):
        for religion in self.pressures:
            while self.pressures[religion] >= 100:
                self.pressures[religion] -= 100
                
                if self.citizens[religion] < self._total_citizens():
                    self._flip_a_citizen(religion)
    
    def _set_main_religion(self):
        old_religion = self.main_religion
        largest_religion = max(self.citizens, key = self.citizens.get)
        
        if self.citizens[largest_religion] > self._total_citizens() / 2:
            self.main_religion = largest_religion
        else:
            self.main_religion = None    
        
        if old_religion != self.main_religion:
            self._update_reachable_cities()
                    
    def _flip_a_citizen(self, religion):
        self.citizens[religion] += 1
        
        if self.citizens['atheist']  > 0:
            self.citizens['atheist'] -= 1
        else:
            self.citizens[self._other_valid_religion(religion)] -= 1
    
    def _other_valid_religion(self, religion):
        religion_names = list(self.citizens.keys())
        religion_names.remove('atheist')
        religion_names.remove(religion)
        
        for religion in religion_names:
            if self._has_no_followers(religion):
                religion_names.remove(religion)
                
        return random.choice(religion_names)

    def _has_no_followers(self, religion):
        return self.citizens[religion] == 0
    
    def _update_reachable_cities(self, cities):
        self.reachable_cities = set()
        if self.main_religion == 'atheist':
            return None
        else:
            for city in cities:
                distance = hex_distance(self.position, city.position)
                religion_reach = religion_stats[self.main_religion]['distance']
                if distance <= religion_reach and city != self:
                    self.reachable_cities.add(city)

# In[ ]:



