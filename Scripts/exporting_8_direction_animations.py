import bpy
import os
import math

# ==========================================
# --- EDIT THESE SETTINGS FOR EACH ANIMATION ---
# ==========================================

# The name of your Empty object
object_name = "Erika"

# The base prefix for your files
base_prefix = "erika_bow_walk_"

# The exact frames you want to render
frames_to_render = [1, 7, 12, 17, 22, 27, 32]

# The folder where images will be saved
output_folder_path = "//"

# ==========================================
# --- DON'T TOUCH BELOW UNLESS YOU KNOW WHY ---
# ==========================================

# 1. Setup the output directory and file format
output_dir = bpy.path.abspath(output_folder_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

bpy.context.scene.render.image_settings.file_format = 'PNG'

# 2. Get the Empty object
empty_obj = bpy.data.objects.get(object_name)

if not empty_obj:
    print(f"❌ ERROR: Could not find an object named '{object_name}' in the scene.")
else:
    # Ensure the empty is set to Euler rotation mode so the script can modify it safely
    if empty_obj.rotation_mode != 'XYZ':
        empty_obj.rotation_mode = 'XYZ'

    # 3. Define the directions and their matching Z-rotations based on your setup
    directions = [
        ("SW", 0),
        ("S", 45),
        ("SE", 90),
        ("E", 135),
        ("NE", 180),
        ("N", 225),
        ("NW", 270),
        ("W", 315)
    ]

    # 4. Loop through each direction
    for dir_name, angle_deg in directions:
        
        # Rotate the Empty (convert degrees to radians for Blender)
        empty_obj.rotation_euler[2] = math.radians(angle_deg)
        
        # Force the view layer to update so the render engine sees the new rotation
        bpy.context.view_layer.update()
        
        # 5. Loop through the frames for this direction
        for index, frame in enumerate(frames_to_render):
            
            # Set the current frame
            bpy.context.scene.frame_set(frame)
            
            # Build the file name: base + direction + index + extension
            file_name = f"{base_prefix}{dir_name}_{index + 1}.png"
            
            # Set the output path
            bpy.context.scene.render.filepath = os.path.join(output_dir, file_name)
            
            # Render!
            bpy.ops.render.render(write_still=True)
            print(f"✅ Rendered {dir_name} (Angle {angle_deg}°) - Frame {frame} as {file_name}")

    print("🎉 --- ALL DIRECTIONS RENDER COMPLETE --- 🎉")
    
    # Optional: Reset the Empty back to SW (0 degrees) at the end
    empty_obj.rotation_euler[2] = 0