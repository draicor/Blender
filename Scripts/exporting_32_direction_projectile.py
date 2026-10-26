import bpy
import os
import math

# ==========================================
# --- EDIT THESE SETTINGS FOR EACH PROJECTILE ---
# ==========================================

# The name of your Empty object
object_name = "Arrow"

# The base prefix for your files
base_prefix = "projectile_arrow_"

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

    # 3. Define the Z-rotations
    angles = [
        0, -11.25, -22.5, -33.75, -45,
        -56.25, -67.5, -78.75, -90,
        -101.25, -112.5, -123.75, -135,
        -146.25, -157.5, -168.75, -180,
        -191.25, -202.5, -213.75, -225,
        -236.25, -247.5, -258.75, -270,
        -281.25, -292.5, -303.75, -315,
        -326.25, -337.5, -348.75 # no need for the last one since it loops
    ]

    # 4. Loop through each angle
    for index, angle_deg in enumerate(angles):
        
        # Rotate the Empty (convert degrees to radians for Blender)
        empty_obj.rotation_euler[2] = math.radians(angle_deg)
        
        # Force the view layer to update so the render engine sees the new rotation
        bpy.context.view_layer.update()
        
        # Build the file name: base + index + extension + padding
        file_name = f"{base_prefix}{index + 1:02d}.png"
        
        # Set the output path
        bpy.context.scene.render.filepath = os.path.join(output_dir, file_name)
        
        # Render!
        bpy.ops.render.render(write_still=True)
        print(f"✅ Rendered (Angle {angle_deg}°) - as {file_name}")
            
            

    print("🎉 --- ALL ANGLE RENDERS COMPLETE --- 🎉")
    
    # Optional: Reset the Empty back to SW (0 degrees) at the end
    empty_obj.rotation_euler[2] = 0