from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Define basic properties for different types of blocks
block_properties = {
    'bedrock': {'color': color.black},
    'grass': {'color': color.lime},
    'dirt': {'color': color.brown},
    'stone': {'color': color.gray}
}

# Player controller setup
player = FirstPersonController()

# Custom AI for dynamic terrain generation
class DynamicTerrainAI:
    def __init__(self, scale=0.1, height=10):
        self.scale = scale
        self.height = height
        self.seed = random.randint(1, 100)

    def get_elevation(self, x, z):
        # Fixed elevation for a flat terrain simulation
        return 1  # Always returns 1 for simplicity, replace with more dynamic logic if needed

    def determine_block_type(self, y, max_height):
        if y == 0:
            return 'bedrock'
        elif y == max_height - 1:
            return 'grass'
        elif y > 1:
            return 'stone'
        else:
            return 'dirt'

# Initialize the AI
terrain_ai = DynamicTerrainAI()

# Entity to represent the blocks in the world
class Voxel(Button):
    def __init__(self, position=(0,0,0), block_type='bedrock'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_properties[block_type]['color'],
            highlight_color=color.white,
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                # AI chooses block type dynamically based on position and elevation
                new_type = terrain_ai.determine_block_type(int(self.position.y) + 1, terrain_ai.height)
                Voxel(position=self.position + mouse.normal, block_type=new_type)
            elif key == 'left mouse down':
                destroy(self)

# Generate flat terrain with layers of bedrock, stone, and grass
def generate_terrain():
    max_height = 5  # Adjust this for deeper layers
    for z in range(20):
        for x in range(20):
            for y in range(max_height):
                block_type = terrain_ai.determine_block_type(y, max_height)
                Voxel(position=(x, y, z), block_type=block_type)

generate_terrain()

app.run()
