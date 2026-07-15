
#sussy white stuff
#hehe :)
#poop💩





from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from copy import copy

app = Ursina(title="minceraft",icon="icon.png")
window.exit_button.visible = False
window.color = color.rgb(135, 206, 235)
Sky()



# performance tweaks: disable vsync and expose chunk settings
window.vsync = False
window.fps_counter.enabled = True

grass_block_model = load_model('grass_block.obj')
grass_texture = load_texture('texture.png')

paused = False
flying = False
last_space = 0
double_tap = 0.3

class Voxel(Entity):
    def __init__(self, position):
        super().__init__(
            parent=scene,
            position=position,
            model=copy(grass_block_model),
            texture=grass_texture,
            scale=1
        )

        self.collider = BoxCollider(self, center=Vec3(0,0,0), size=Vec3(1,1,1))

    def input(self, key):
        if self.hovered and not paused:
            if key == 'left mouse down':
                destroy(self)
            if key == 'right mouse down':

                Voxel(self.position + mouse.normal)


# lower these values to improve FPS (smaller world = fewer voxels to render)
CHUNK_SIZE = 16  # was 24
MAX_HEIGHT = 3   # was up to 5
for x in range(CHUNK_SIZE):
    for z in range(CHUNK_SIZE):
        for y in range(random.randint(1, MAX_HEIGHT)):
            Voxel((x, y, z))


player = FirstPersonController()
player.position = (12, 10, 12)
player.speed = 6
player.gravity = 1


mouse.locked = True
mouse.sensitivity = Vec2(300,300)


def is_block_at(position):
    for entity in scene.entities:
        if isinstance(entity, Voxel):
            if (
                abs(entity.position.x - position.x) < 0.5 and
                abs(entity.position.z - position.z) < 0.5 and
                abs(entity.position.y - position.y) < 0.5
            ):
                return True
    return False


def can_move_to(start, end):
    if start == end:
        return True

    direction = end - start
    distance = direction.length()
    if distance <= 0:
        return True

    step_size = 0.1
    steps = max(1, int(distance / step_size))
    step = direction / steps

    for i in range(steps + 1):
        point = start + step * i
        if is_block_at(point):
            return False

    return True


def input(key):
    global paused, flying, last_space
    if key == 'v':
        paused = not paused
        mouse.locked = not paused
        application.paused = paused
        player.enabled = not paused

    if key == 'space' and not paused:
        now = time.time()
        if now - last_space < double_tap:
            head_position = Vec3(player.x, player.y + player.height, player.z)
            head_block = raycast(head_position, Vec3(0, 1, 0), distance=1.1, traverse_target=scene, ignore=[player])
            if flying or (player.grounded and not head_block.hit):
                flying = not flying
                player.gravity = 0 if flying else 1
                player.velocity_y = 0
        last_space = now
    if key == 'escape':
        application.quit()


def update():
    if flying and not paused:
        new_y = player.y
        if held_keys['space']:
            new_y += time.dt * 6
        if held_keys['left shift']:
            new_y -= time.dt * 6

        if can_move_to(Vec3(player.x, player.y, player.z), Vec3(player.x, new_y, player.z)):
            player.y = new_y

    if player.y < -30:
        player.position = (12, 12, 12)

app.run()
