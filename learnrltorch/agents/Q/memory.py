# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:24:57 2020

@author: valentin
"""

import torch

class Memory():
    
    def __init__(self, max_memory_len=1000):
        try:
            assert type(max_memory_len) is int   
        except AssertionError:
            raise TypeError("Memory() argument must be an integer, "
                            f"not '{type(max_memory_len)}'")
        try:
            assert (max_memory_len > 0)
        except AssertionError:
            raise ValueError("Trying to create memory with negative"
                             " maximum length : {max_memory_len}")
            
        self.max_memory_len = max_memory_len
        self.memory_len = 0
        self.MEMORY_KEYS = ('observation', 'actions', 'rewards', 'done',
                            'next_observation')
        self.datas = {key: None for key in self.MEMORY_KEYS}
        
    def remember(self, observation, action, reward, done, next_observation):
        for val, key in zip((observation, action, reward, done, 
                             next_observation), self.MEMORY_KEYS):
            batched_val = torch.unsqueeze(val, dim=0)
            if self.memory_len == 0:
                self.datas[key] = batched_val
            else:
                self.datas[key] = torch.cat((self.datas[key], batched_val), 
                                            dim=0)
            self.datas[key] = self.datas[key][-self.max_memory_len:]
        self.memory_len = len(self.datas[self.MEMORY_KEYS[0]])

    def sample(self, sample_size, method='random'):
        if method == 'random':
            indicies = torch.randperm(self.memory_len)[:sample_size]
            datas = [torch.gather(self.datas[key], 0, indicies) 
                     for key in self.MEMORY_KEYS]
        elif method == 'last':
            datas = [self.datas[key][-sample_size:] 
                     for key in self.MEMORY_KEYS]
        else:
            raise NotImplementedError(f'Unknown sampling method {method}')
        return datas
    
    def __len__(self):
        return self.memory_len
    
    def __dict__(self):
        return self.datas
    
    def __str__(self):
        return str(self.datas)
    
    def __repr__(self):
        return repr(self.datas)