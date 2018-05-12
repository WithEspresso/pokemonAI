"""
-Type Advantage
-Current Pokemon’s Status(Paralysis, sleep, burn, poision)
-Opposing Pokemon’s Status
-Current Pokemon’s Stats(HP, Attack, Defense, Special Attack, Special Defense, Speed should be scaled properly by increase or decreases in stages occurring in battle, i.e. Intimidate, Swords Dance)
-Opposing Pokemon’s Stats
-Current Pokemon’s Movesets
-Opposing Pokemon’s Expected/Predicted moveset(Don’t think we need to fear a gimmicky Pokemon set because sets a pre-generated in random battles?)
-Switching at the worst case scenario of being K.O’d and choosing the Pokemon that will take the least amount of damage from that predicted move.(Not always good, switching a Pokemon like Dragonite into Heatran to avoid damage from an ice type move, only to get hit by an Earthquake next turn. Might work if we make Heatran switch again do to the fear of a possibility of Earthquake, but if switch to Dragonite again will create endless looping. Also, threat of over-prediction as well as needing to take into account entry hazards.)

"""


class GameState:

    friendly_team = list()
    enemy_team = list()
    active_pokemon = None
    enemy_active_pokemon = None

    def __init__(self):
        pass

