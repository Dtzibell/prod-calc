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
        self.skillPoints += self.upgradeCosts[skill] - 1
        self.stats[skill] -= self.STAT_INCREMENTS[skill]
        self.upgradeCosts[skill] -= 1

    def level(self, function, skill, amount):
        for _ in range(amount):
            function(skill)

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

me = Player(22*4 - 21)
best = BestResult(-float("inf"), 1., {})
for entre in range(10):
    try:
        me.level(me.increaseLevel, "entre", entre)
        for ener in range(10):
            try:
                me.level(me.increaseLevel, "energy", ener)
                for prod in range(10):
                    try:
                        me.level(me.increaseLevel, "prod", prod)
                        income, prodRatio = me.calculateProfit()
                        if income > best.income:
                            best.income = income
                            best.prodRatio = prodRatio
                            best.stats = me.stats
                        me.level(me.decreaseLevel, "prod", prod)
                    except ValueError:
                        pass
                me.level(me.decreaseLevel, "energy", ener)
            except ValueError:
                pass
        me.level(me.decreaseLevel, "entre", entre)
    except ValueError:
            pass

print(best.income, best.prodRatio, me.stats)
print(me.PP_VALUE * best.prodRatio)
print(0.087 * best.prodRatio)
