import bpy
from math import radians
from mathutils import Quaternion, Vector

armature_name = "erika"
#bone_name = "mixamorig:LeftForeArm"
#offset = Quaternion(Vector((0, 1, 0)), radians(45))
bone_name = "mixamorig:LeftArm"
offset = Quaternion(Vector((1, 0, 0)), radians(-5))

armature = bpy.data.objects.get(armature_name)
if not armature:
    print(f"ERROR: No se encontró el objeto '{armature_name}'")
elif not armature.animation_data or not armature.animation_data.action:
    print(f"ERROR: '{armature_name}' no tiene una Action asignada (¿está en NLA?)")
else:
    action = armature.animation_data.action
    path = f'pose.bones["{bone_name}"].rotation_quaternion'

    # Recoger F-Curves: soporta legacy y slotted actions (Blender 4.4+)
    fcurves = []
    try:
        fcurves = [fc for fc in action.fcurves if fc.data_path == path]
    except AttributeError:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        if fc.data_path == path:
                            fcurves.append(fc)

    if not fcurves:
        print(f"ERROR: No se encontraron F-Curves para {path}")
        print("Revisa que el hueso esté en Quaternion (no Euler) y que el nombre sea exacto.")
    else:
        fcurve_dict = {fc.array_index: fc for fc in fcurves}
        if len(fcurve_dict) != 4:
            print(f"ADVERTENCIA: se esperaban 4 canales (W,X,Y,Z), hay {len(fcurve_dict)}")
        else:
            frames = sorted({kp.co.x for fc in fcurves for kp in fc.keyframe_points})
            for frame in frames:
                w, x, y, z = [fcurve_dict[i].evaluate(frame) for i in range(4)]
                new_q = Quaternion((w, x, y, z)) @ offset
                for i in range(4):
                    for kp in fcurve_dict[i].keyframe_points:
                        if abs(kp.co.x - frame) < 0.001:
                            delta = new_q[i] - kp.co.y
                            kp.co.y = new_q[i]
                            kp.handle_left.y += delta
                            kp.handle_right.y += delta
            for fc in fcurves:
                fc.update()
            print(f"Listo: {len(frames)} keyframes rotados -5° en X local.")