import json

class DapperDinoTraits:
    def __init__(self, image, eyes, face, clothes, headwear, background, body, accessory):
        self.image = image
        self.eyes = eyes
        self.face = face
        self.clothes = clothes
        self.headwear = headwear
        self.background = background
        self.body = body
        self.accessory = accessory

    def reprJSON(self):
        return dict(
            image = self.image,
            eyes = self.eyes,
            face = self.face,
            clothes = self.clothes,
            headwear = self.headwear,
            background = self.background,
            body = self.body,
            accessory = self.accessory,
        )
        
class DapperDinoStats:
    def __init__(self, currentAcceleration, currentAgility, currentAttack, currentDefense, currentHealth, currentSpeed):
        self.acceleration = currentAcceleration
        self.agility = currentAgility
        self.attack = currentAttack
        self.defense = currentDefense
        self.health = currentHealth
        self.speed = currentSpeed
        self.totalPoints = currentAcceleration + currentAgility + currentAttack + currentDefense + currentHealth + currentSpeed

    def setMaxStats(self, maxAcceleration, maxAgility, maxAttack, maxDefense, maxHealth, maxSpeed, bonusPoints):
        self.maxAcceleration = maxAcceleration
        self.maxAgility = maxAgility
        self.maxAttack = maxAttack
        self.maxDefense = maxDefense
        self.maxHealth = maxHealth
        self.maxSpeed = maxSpeed
        self.bonusPoints = bonusPoints
    
    def reprJSON(self) -> dict:
        return dict(
            acceleration = DinoStat(self.acceleration, self.maxAcceleration),
            agility = DinoStat(self.agility, self.maxAgility),
            attack = DinoStat(self.attack, self.maxAttack),
            defense = DinoStat(self.defense, self.maxDefense),
            health = DinoStat(self.health, self.maxHealth),
            speed = DinoStat(self.speed, self.maxSpeed),
            bonusPoints = self.bonusPoints
        )

# {
#  "currentValue": 61,
#  "maxValue": 100
# }
class DinoStat:
    def __init__(self, currentValue, maxValue):
        self.currentValue = currentValue
        self.maxValue = maxValue

    def reprJSON(self) -> dict:
        return dict(
            currentValue = self.currentValue,
            maxValue = self.maxValue
        )

    
class DapperDino:
    def __init__(self, dinoNumber, isKarma, originalDinoNumber):
        self.dinoNumber = dinoNumber
        self.isKarma = isKarma
        self.originalDinoNumber = str(originalDinoNumber)

    def setStats(self, acceleration, agility, attack, defense, health, speed):
        self.stats = DapperDinoStats(acceleration, agility, attack, defense, health, speed)

    def setMaxStats(self, maxAcceleration, maxAgility, maxAttack, maxDefense, maxHealth, maxSpeed, bonusPoints):
        self.stats.setMaxStats(maxAcceleration, maxAgility, maxAttack, maxDefense, maxHealth, maxSpeed, bonusPoints)

    def setTraits(self, image, eyes, face, clothes, headwear, background, body, accessory):
        self.traits = DapperDinoTraits(image, eyes, face, clothes, headwear, background, body, accessory)

    def toJson(self) -> str:
        return json.dumps(self.__dict__, cls=DapperDinoEncoder)

# https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
class DapperDinoEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
        