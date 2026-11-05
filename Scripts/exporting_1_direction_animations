import bpy
import os
import math

# ==========================================
# --- EDIT THESE SETTINGS FOR EACH ANIMATION ---
# ==========================================

# The name of your Empty object
object_name = "Erika"

# The base prefix for your files, ends with _
# Example: "erika_bow_death_"
base_prefix = "erika_bow_death_"

# The exact frames you want to render
frames_to_render = [8, 13, 31, 40, 45, 49, 53, 63]

# --- Direction for THIS animation ---
# Name that will appear in the file (e.g., "SW", "S", "SE", ...)
direction_name = "SW"

# Z angle in degrees for that direction
# Based on your setup: SW=0, S=45, SE=90, E=135, NE=180, N=225, NW=270, W=315
direction_angle = 0

# The folder where images will be saved ("//" = next to the .blend file)
output_folder_path = "//"

# ==========================================
# --- DON'T TOUCH BELOW UNLESS YOU KNOW WHY ---
# ==========================================

# 1. Set up the output directory and file format
output_dir = bpy.path.abspath(output_folder_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

bpy.context.scene.render.image_settings.file_format = 'PNG'

# 2. Get the Empty object
empty_obj = bpy.data.objects.get(object_name)

if not empty_obj:
    print(f"❌ ERROR: Could not find an object named '{object_name}' in the scene.")
else:
    # Make sure the Empty is in Euler rotation mode so the script can modify it safely
    if empty_obj.rotation_mode != 'XYZ':
        empty_obj.rotation_mode = 'XYZ'

    # 3. Rotate the Empty to the chosen direction
    empty_obj.rotation_euler[2] = math.radians(direction_angle)
    bpy.context.view_layer.update()

    # 4. Loop through the frames
    for index, frame in enumerate(frames_to_render):

        bpy.context.scene.frame_set(frame)

        # Build the file name: prefix + direction + index + extension
        file_name = f"{base_prefix}{direction_name}_{index + 1}.png"

        bpy.context.scene.render.filepath = os.path.join(output_dir, file_name)

        bpy.ops.render.render(write_still=True)
        print(f"✅ Rendered {direction_name} (Angle {direction_angle}°) - Frame {frame} as {file_name}")

    print(f"🎉 --- DIRECTION {direction_name} COMPLETE --- 🎉")

    # Optional: reset the Empty back to 0 degrees at the end
    empty_obj.rotation_euler[2] = 0