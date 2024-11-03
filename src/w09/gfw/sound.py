import pico2d

_sounds = {}

def music(file):
    return load(file, pico2d.load_music)

def sfx(file): # sfx = Sound Effect
    return load(file, pico2d.load_wav)

def load(file, func):
    global _sounds
    if file in _sounds:
        return _sounds[file]

    sound = func(file)
    _sounds[file] = sound
    return sound

def unload(file):
    global _sounds
    if file in _sounds:
        del _sounds[file]

