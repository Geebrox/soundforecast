#Package that will be used for randomizing numbers
from random import randrange

#Class that creates a list that contains sound from ./sounds folder according weather condition
class ConditionList:
    def __init__(self, condition, max_sounds):
        self.condition = condition
        self.list = []
        for i in range(max_sounds):
            self.list.append("sounds/" + str(condition) +
                             "/" + str(i) + ".mp3")

#Class that creates a full list of conditions with its sounds list using above class
#Class also contains some helpful functions that returns the path for sound folder according your needs
class Sounds:
    def __init__(self):
        max_list = [1, 5, 3, 5, 2, 3, 2, 2, 11, 13, 3, 6, 6, 7, 7, 7, 3, 2, 7, 3, 1, 4,
                    1, 1, 4, 13, 2, 2, 2, 2, 2, 4, 3, 5, 5, 3, 3, 5, 6, 6, 2, 3, 13, 13, 1, 6, 9, 6]
        self.sounds_list = []
        for i in range(len(max_list)):
            tempCondition = ConditionList(i, max_list[i])
            self.sounds_list.append(tempCondition)

    def getSoundForCondition(self, condition):
        tempList = self.sounds_list[condition].list
        return tempList[randrange(len(tempList))]

    def getRandomSound(self):
        random_condition = randrange(len(self.sounds_list))
        return self.getSoundForCondition(random_condition)
