import json

class DapperDinoTraits:
    def __init__(self, eyes, face, clothes, headwear, background, body, accessory):
        self.eyes = eyes
        self.face = face
        self.clothes = clothes
        self.headwear = headwear
        self.background = background
        self.body = body
        self.accessory = accessory

    def reprJSON(self):
        return dict(
            eyes = self.eyes,
            face = self.face,
            clothes = self.clothes,
            headwear = self.headwear,
            background = self.background,
            body = self.body,
            accessory = self.accessory,
        )
        
class DapperDinoStats:
    def __init__(self, acceleration, agility, attack, defense, health, speed):
        self.acceleration = acceleration
        self.agility = agility
        self.attack = attack
        self.defense = defense
        self.health = health
        self.speed = speed
        self.totalPoints = acceleration + agility + attack + defense + health + speed
    
    def reprJSON(self) -> dict:
        return dict(
            acceleration = self.acceleration,
            agility = self.agility,
            attack=self.attack,
            defense = self.defense,
            health = self.health,
            speed = self.speed
        )

class DapperDino:
    def __init__(self, dinoNumber, isKarma, originalDinoNumber):
        self.dinoNumber = dinoNumber
        self.isKarma = isKarma
        self.originalDinoNumber = str(originalDinoNumber)

    def setStats(self, acceleration, agility, attack, defense, health, speed):
        self.stats = DapperDinoStats(acceleration, agility, attack, defense, health, speed)

    def setTraits(self, eyes, face, clothes, headwear, background, body, accessory):
        self.traits = DapperDinoTraits(eyes, face, clothes, headwear, background, body, accessory)

    def toJson(self) -> str:
        return json.dumps(self.__dict__, cls=DapperDinoEncoder)

# https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
class DapperDinoEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
        