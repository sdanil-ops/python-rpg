DEBUG: bool = True
WIDTH: int = 1920
HEIGHT: int = 1080
FPS: int = 60
TILESIZE: int = 64

game_status = 'pre alpha'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'graphics/weapon/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'graphics/weapon/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics/weapon/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 10, 'graphic': 'graphics/weapon/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'graphics/weapon/sai/full.png'}
}

camera_borders = {
    'left': 600, 'right': 600, 'top': 300, 'bottom': 300
}
