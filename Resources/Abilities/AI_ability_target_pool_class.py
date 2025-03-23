## Among Myth and Wonder
## AI_ability_target_pool_class

import random


class AI_Target_Pool():
    # Keeps positions of unit targets for abilities
    # As sets of ints: (int, int)
    def __init__(self, priority_1, priority_2=None, priority_3=None):
        self.priority_1 = priority_1
        self.priority_2 = priority_2
        self.priority_3 = priority_3

    def pick_targets(self, b):
        counter = 1
        while counter <= b.total_targets:
            if self.priority_1:
                pick = random.choice(self.priority_1)
                self.priority_1.remove(pick)
                b.ability_targets.append(pick)

            elif self.priority_2:
                pick = random.choice(self.priority_2)
                self.priority_2.remove(pick)
                b.ability_targets.append(pick)

            elif self.priority_3:
                pick = random.choice(self.priority_3)
                self.priority_3.remove(pick)
                b.ability_targets.append(pick)

            else:
                break

            counter += 1
