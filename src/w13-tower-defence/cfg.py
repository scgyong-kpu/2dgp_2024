import pickle

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
        map=1, interval=(3.0, 1.0), gold=300, castle=1000
    ),
]

flies = [
    Info(file='res/fly_1.png', fps=3, speed=(5,10), rate=5,  bbox=(-20,-20,20,20), life=900, power=50, cool_time=2.0),
    Info(file='res/fly_2.png', fps=3, speed=(10,30), rate=10, bbox=(-20,-20,20,20), life=300, power=25, cool_time=2.0),
    Info(file='res/fly_3.png', fps=3, speed=(20,30), rate=15, bbox=(-20,-20,20,20), life=200, power=15, cool_time=2.0),
    Info(file='res/fly_4.png', fps=2, speed=(30,40), rate=25, bbox=(-20,-20,20,20), life=150, power=10, cool_time=2.0),
    Info(file='res/fly_5.png', fps=1, speed=(30,40), rate=35, bbox=(-20,-20,20,20), life=80, power=5, cool_time=2.0),
]

def new_cfg():
    return Info(weapon=weapon, stages=stages, flies=flies)

FILENAME = 'cfg.pickle'

try:
    with open(FILENAME, 'rb') as f:
        cfg = pickle.load(f)
    print(f'{cfg.weapon.arrow.range=}')
except Exception as e:
    cfg = new_cfg()
    print(f'{FILENAME} not open: {e}')

def save():
    cfg = new_cfg()
    with open(FILENAME, 'wb') as f:
        pickle.dump(cfg, f)


