import bpy

def all_modifier_names_icons_types():
    """List of tuples of the names, icons and types of all modifiers."""
    mods_enum = bpy.types.Modifier.bl_rna.properties['type'].enum_items

    all_mod_names = [modifier.name for modifier in mods_enum]
    all_mod_icons = [modifier.icon for modifier in mods_enum]
    all_mod_types = [modifier.identifier for modifier in mods_enum]

    all_mods_zipped = list(zip(all_mod_names, all_mod_icons, all_mod_types))
    return all_mods_zipped

def all_modifier_object_slots():
    """List of all modifiers with object slots"""
    modifier_dict = {
        "ARRAY": [("Offset Object", "offset_object"), ("Start Cap", "start_cap"), ("End Cap", "end_cap")],
        "CURVE": [("Object", "object")],
        "MIRROR": [("Mirror Object", "mirror_object")],
        "SCREW": [("Axis Object", "object")]
        }
    return modifier_dict
