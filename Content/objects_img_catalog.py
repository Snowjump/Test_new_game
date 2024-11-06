## Among Myth and Wonder

# This catalog lists what image use for objects depending on current season in terrain
# corresponds to lists in terrain_seasons

# 1 - Oak
oak_seasons = {"Early Winter": "oak_winter",
               "Winter": "oak_winter",
               "Melting Spring": "oak_early_spring",
               "Spring": "oak_spring",
               "Summer": "oak_summer",
               "Autumn": "oak_autumn"}

# 2 - Birch
birch_seasons = {"Early Winter": "birch_early_spring",
                 "Winter": "birch_winter",
                 "Melting Spring": "birch_early_spring",
                 "Spring": "birch_summer",
                 "Summer": "birch_summer",
                 "Autumn": "birch_autumn"}

# 3 - Pine
pine_seasons = {"Early Winter": "pine_winter",
                "Winter": "pine_winter",
                "Melting Spring": "pine_spring",
                "Spring": "pine_spring",
                "Summer": "pine_summer",
                "Autumn": "pine_autumn"}

# Dictionary catalog

object_calendar = {"Oak": oak_seasons,
                   "Birch": birch_seasons,
                   "Pine": pine_seasons}


object_variations = {"Oak": 1,
                     "Birch": 3,
                     "Pine": 3}
