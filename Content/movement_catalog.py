## Miracle battles

# List composition: [list of directions from where movement is wasted]
waste_movement_dict = {"Earth rampart" : ["NW", "W", "SW"],
                       "Palisade" : ["W"],
                       "Palisade_ruins" : ["W"],
                       "Palisade_bottom" : ["W"],
                       "Palisade_bottom_ruins" : ["W"],
                       "Palisade_gates" : [],
                       "Palisade_gates_ruins" : []}

block_movement_dict = {"Earth rampart" : [],
                       "Palisade" : ["NW", "W", "SW"],
                       "Palisade_ruins" : ["NW", "SW"],
                       "Palisade_bottom" : ["NW", "W", "SW"],
                       "Palisade_bottom_ruins" : ["NW", "SW"],
                       "Palisade_gates" : ["NW", "W", "SW"],
                       "Palisade_gates_ruins" : ["NW", "SW"]}

gates_pass_dict = ["Palisade_gates"]

walls_block_dict = ["Palisade", "Palisade_bottom"]

