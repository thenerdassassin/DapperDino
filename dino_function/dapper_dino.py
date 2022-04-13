import json

class DapperDino:
    def __init__(self, dinoNumber, isKarma, originalDinoNumber):
        self.dinoNumber = dinoNumber
        self.isKarma = isKarma
        self.originalDinoNumber = originalDinoNumber

    def setStats(self, acceleration, agility, attack, defense, health, speed):
        self.acceleration = acceleration
        self.agility = agility
        self.attack = attack
        self.defense = defense
        self.health = health
        self.speed = speed
        self.totalPoints = acceleration + agility + attack + defense + health + speed

    def toJson(self):
        return json.dumps(self.__dict__)