import pygame

from support import import_folder
from settings import weapon_data

class Player(pygame.sprite.Sprite):
    pressed_key: str = ''

    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(*groups)
        # hitbox
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-5, -26)
        # graphics
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.5
        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.weapon_can_switch = True
        self.weapon_switch_time = None
        self.weapon_switch_duration_cooldown = 200

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement
            if keys[pygame.K_UP]:
                self.pressed_key = 'K_UP'
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.pressed_key = 'K_DOWN'
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.pressed_key = 'K_RIGHT'
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.pressed_key = 'K_LEFT'
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            # attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.pressed_key = 'space'
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.pressed_key = 'left_control'
                self.attack_time = pygame.time.get_ticks()

            if keys[pygame.K_q] and self.weapon_can_switch:
                self.pressed_key += 'q '
                self.weapon_can_switch = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) -1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]


    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status += '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.weapon_can_switch:
            if current_time - self.weapon_switch_time >= self.weapon_switch_duration_cooldown:
                self.weapon_can_switch = True

    def animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.pressed_key = 'None'
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

