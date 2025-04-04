## Among Myth and Wonder
## save_game

import pickle


def save_current_game(filename):
    print("save_current_game() " + str(filename))
    data = {}
    data["filename"] = filename
    with open('data.svfl', 'wb') as file:  # Savefile = svfl
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
