import bpy
object_modifiers = bpy.context.active_object.modifiers
for each in object_modifiers:
    print(type(each.type))