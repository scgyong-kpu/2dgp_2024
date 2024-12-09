class Info:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

weapon = Info(
    range_increase = 1.2,
    power_increase = 1.2,
    interval_decrease = 0.8,
    arrow=Info(
        fmt='res/weapon/bow_%d.png',
        costs = [150, 300, 450],
        interval = 2.0,
        power = 50,
        range = 250,
        block = 3,
        bullet_speed = 300,
    ),
    ice=Info(
        fmt='res/weapon/ice_sword_%d.png',
        costs = [200, 400, 600],
        interval = 3.0,
        power = 20,
        range = 300,
        block = 3,
        bullet_speed = 200,
    ),
    fire=Info(
        fmt='res/weapon/fire_thrower_%d.png',
        costs = [230, 500, 1000],
        interval = 6.0,
        power = 30,
        range = 350,
        block = 3,
        bullet_speed = 160,
    ),
)

stages = [
    Info(
        map=1, interval=(3.0, 1.0), gold=300,
    ),
]