from copy import copy, deepcopy
skillPoints = int(input("Enter the amount of free skill points").strip())

class Player:
    def __init__(self, skillPoints):
        self.stats = {
                "entre": 30,
                "energy": 30,
                "prod": 10,
                }
        self.STAT_INCREMENTS = {
                "entre": 5,
                "energy": 10,
                "prod": 3,
                }
        self.upgradeCosts = {
                "entre": 1,
                "energy": 1,
                "prod": 1,
                }
        self.skillPoints = skillPoints
        self.PP_VALUE = 0.082

    def increaseLevel(self, skill):
        self.skillPoints -= self.upgradeCosts[skill]
        if self.skillPoints < 0:
            self.skillPoints += self.upgradeCosts[skill]
            raise ValueError
        self.stats[skill] += self.STAT_INCREMENTS[skill]
        self.upgradeCosts[skill] += 1

    def decreaseLevel(self, skill):
        self.stats[skill] -= self.STAT_INCREMENTS[skill]
        self.upgradeCosts[skill] -= 1
        self.skillPoints += self.upgradeCosts[skill]

    def level(self, function, skill, amount):
        count = 0
        try:
            for _ in range(amount):
                function(skill)
                count += 1
        except ValueError:
            if function == self.increaseLevel:
                for _ in range(count):
                    self.decreaseLevel(skill)
            raise ValueError

    def selfWorkIncome(self):
        entre = self.stats["entre"]
        prod = self.stats["prod"]
        return 24 * entre / 100 * prod * self.PP_VALUE

    def employmentIncome(self):
        TAX_RATE = 0.95
        prod = self.stats["prod"]
        energy = self.stats["energy"]
        return 24 * energy / 100 * prod * self.PP_VALUE * TAX_RATE

    def calculateProfit(self):
        selfWorkIncome = self.selfWorkIncome()
        employerIncome = self.employmentIncome()
        prod = self.stats["prod"]
        prodRatio = (prod + 10) / prod
        return selfWorkIncome + employerIncome * prodRatio, prodRatio

class BestResult:
    def __init__(self, income, prodRatio, stats):
        self.income = income
        self.prodRatio = prodRatio
        self.stats = stats

me = Player(skillPoints)
best = BestResult(-float("inf"), 1., {})
for entre in range(11):
    try:
        me.level(me.increaseLevel, "entre", entre)
        for ener in range(11):
            try:
                me.level(me.increaseLevel, "energy", ener)
                for prod in range(11):
                    try:
                        me.level(me.increaseLevel, "prod", prod)
                        income, prodRatio = me.calculateProfit()
                        if income > best.income:
                            best.income = income
                            best.prodRatio = prodRatio
                            best.stats = deepcopy(me.stats)
                        me.level(me.decreaseLevel, "prod", prod)
                    except ValueError:
                        continue
                me.level(me.decreaseLevel, "energy", ener)
            except ValueError:
                continue
        me.level(me.decreaseLevel, "entre", entre)
    except ValueError:
        print("failed")
        continue

print(best.income, best.prodRatio, best.stats)
print(me.PP_VALUE * best.prodRatio)
print(0.087 * best.prodRatio)
