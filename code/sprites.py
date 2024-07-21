from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()
        
class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class CollidableSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(0, -self.rect.height*.8)
        
class MonsterPatchSprite(Sprite):
    def __init__(self, pos, surf, groups, biome):        
        self.biome = biome
        super().__init__(pos, surf, groups, WORLD_LAYERS['main'] if self.biome != 'sand' else WORLD_LAYERS['bg'])
        self.y_sort -= 40
        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frame_index = 0
        self.frames = frames
        super().__init__(pos, frames[self.frame_index], groups, z)
        
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
    def update(self, dt):
        self.animate(dt)

