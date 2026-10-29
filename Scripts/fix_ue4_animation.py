import bpy

# ========== CONFIG ==========
bones_to_process = ["pelvis", "root"] 
scale_factor = 0.01  # cm a metros

# Aquí definimos el ajuste final para que los pies toquen el suelo.
# Basado en lo que dijiste, restaremos 0.1 en el eje X del pelvis.
explicit_offsets = {
    "pelvis": {"X": -0.1, "Y": 0.0, "Z": 0.0},
    "root":   {"X": 0.0,  "Y": 0.0, "Z": 0.0}
}
# ============================

obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise Exception("Selecciona la armature con la acción asignada")
if not obj.animation_data or not obj.animation_data.action:
    raise Exception("La armature no tiene acción")

act = obj.animation_data.action
print(f"Procesando Action: {act.name}")

def iter_containers(action):
    if hasattr(action, 'layers') and len(action.layers) > 0:
        for layer in action.layers:
            for strip in layer.strips:
                if hasattr(strip, 'channelbags'):
                    for cb in strip.channelbags: yield cb
                else:
                    for slot in action.slots:
                        cb = strip.channelbag(slot)
                        if cb: yield cb
    elif hasattr(action, 'fcurves'):
        yield action

# 1) Borrar canales a nivel OBJETO
removed = 0
for container in iter_containers(act):
    for fc in list(container.fcurves):
        if not fc.data_path.startswith('pose.bones'):
            container.fcurves.remove(fc)
            removed += 1
print(f"[1] Canales de objeto borrados: {removed}")

# 2) Escalar (cm -> m), Recentrar y Offset
axes_map = {0: "X", 1: "Y", 2: "Z"}
for container in iter_containers(act):
    for fc in list(container.fcurves):
        for bone_name in bones_to_process:
            path = f'pose.bones["{bone_name}"].location'
            if fc.data_path == path and fc.keyframe_points:
                axis_name = axes_map[fc.array_index]

                # A) Escalar (0.01)
                for kp in fc.keyframe_points:
                    kp.co.y           *= scale_factor
                    kp.handle_left.y  *= scale_factor
                    kp.handle_right.y *= scale_factor

                # B) Recentrar (el primer frame a 0)
                first_kp = min(fc.keyframe_points, key=lambda k: k.co.x)
                shift_needed = -first_kp.co.y

                # C) Añadir offset extra (el -0.1)
                offset = explicit_offsets.get(bone_name, {}).get(axis_name, 0.0)
                total_shift = shift_needed + offset

                # Aplicar el desplazamiento total a todos los frames
                if total_shift != 0:
                    for kp in fc.keyframe_points:
                        kp.co.y           += total_shift
                        kp.handle_left.y  += total_shift
                        kp.handle_right.y += total_shift

                fc.update()
                print(f"[2] {bone_name}.{axis_name}: escalado y desplazado (shift: {total_shift:+.4f})")

print("¡Listo! Todo procesado en un solo paso.")