## Project: BattleCity
## Module: Map
## Author: Salwan

import os, pickle

class ScoreData(object):
    def __init__(self):
        self.hiScore = 20000
        self.p1Score = 0
        self.p2Score = 0        

    def save(self, filename):
        file = open(filename, "w")
        pickle.dump([self.hiScore, self.p1Score, self.p2Score], file, pickle.HIGHEST_PROTOCOL)
        file.close()

    def load(self, filename):
        try:
            file = open(filename, "rb")
            data = pickle.load(file)
            if len(data) > 0:
                self.hiScore = data[0]
                self.p1Score = data[1]
                self.p2Score = data[2]
            file.close()
        except IOError:
            self.save(filename)
        return self