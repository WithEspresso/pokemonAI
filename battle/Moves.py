"""
Damage calculation formula:
Damage = ((((2 * Attacker.level) / 5 ) * Move.base_power * Attacker.attack/Defender.defense) / 50) + 2) * Modifier
Modifier = Targets * Weather * Badge * Critical * random * STAB * Type * Burn * other
    Targets:    Not relevant in singles. 1.00.
    Weather:    Fire moves get 2.00 in Sunny Day, 0.50 in Rain Dance,
                Water moves get 0.50 in Sunny Day, 2.00 in Rain Rance
    Critical:   1.50 from Generation VI onwards if critical, 1.00 otherwise.
    Random:     Random integer percentage from 0.85 to 1.00 inclusive.
    STAB:       Same type attack bonus. 1.50, 2.00 if ability is adaptability, 1.00 otherwise.
    Burn:       0.5 if the attacker has been burned and the move is physical and not Facade.
    other:      (This is a long list of really, REALLY specific cases)
                Condition:                                  Multiplier
                Aurora veil is on defender's side,          0.50
                    attacker does not have infiltrate,
                    attack is not a critical hit.
                Move is Body Slam, target is minimized      2.00
                Move is Dragon Slam, target is minimized    2.00
                Move is Earthquake, target is using dig.    2.00
                Move is Flying Press, target is minimized   2.00
                Move is Heat Crash, target is minimized     2.00
                Move is Heavy Slam, target is minimized     2.00
                Light Screen is on defender's side,         0.50
                    attacker does not have infiltrate,
                    attack is not a critical hit,
                    attack is a special attack
                Move is Magnitude, target is using dig.     2.00
                Move is Phantom Force, target is minimized  2.00
                Move is Shadow Force, target is minimized   2.00
                Reflect is on defender's side,              0.50
                    attacker does not have infiltrate,
                    attack is not a critical hit,
                    attack is a physical attack
                Move is Stomp, target is minimized          2.00
                Move is Surf, target is using Dive          2.00
                Move is Whirlpool, target is using Dive     2.00
                Move is a Z-move, target is using protect   0.25

                If the target has Fluffy and the            0.50
                    used move makes contact
                    and is not Fire-type
                If the target has Fluffy and the            2.00
                    used move does not make contact
                    used move is Fire-type
                Target has Filter, used move is             0.75
                    super effective
                Target has Multiscale,is at full health     0.50
                Target has Prism Armor, used move is        0.75
                    super effective
                Target has Shadow Shield                    0.50
                    and is at full health,
                Attacker has Sniper,                        1.50
                    move lands a critical hit
                Target has Solid Rock, used move is         0.75
                    super effective
                Attacker has this ability, used move        2.00
                    is not super effective

                Attacker is holding Expert Belt,            1.20
                    move is super effective
                Attacker is holding Life Orb,               1.33

I excluded information that would involve knowing what the
defender is holding.
"""