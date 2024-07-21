from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']
        
        #movement
        self.direction = vector()
        self.speed = 250
        
        #graphics
        self.frame_index, self.frames = 0, frames
        self.facing_direction = facing_direction
        
        #sprite_setup
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
        
        self.y_sort = self.rect.centery
        
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]
        
    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x !=0:
                if self.direction.x > 0:
                    self.facing_direction = 'right'
                else:
                    self.facing_direction = 'left'
            if self.direction.y !=0:
                if self.direction.y > 0:
                    self.facing_direction = 'down'
                else:
                    self.facing_direction = 'up'
        return f'{self.facing_direction}{'' if moving else '_idle'}'
        

class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
        super().__init__(pos, frames, groups, facing_direction)
        self.collision_sprites = collision_sprites
        
    def collisions(self, axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
            
        
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_UP]:
            input_vector.y -= 1
            print('up')
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
            print('down')
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            print('left')
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            print('right')
        self.direction = input_vector.normalize() if input_vector else input_vector
    
    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')
        
        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')
    
    def update (self, dt):
        self.y_sort = self.rect.centery
        self.input()
        self.move(dt)
        self.animate(dt)
        
class Character(Entity):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(pos, frames, groups, facing_direction)
    