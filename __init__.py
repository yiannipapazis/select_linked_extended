# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
bl_info = {
    "name": "Select Linked Extended",
    "author": "Yianni Papazis",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Select Linked"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_category = "Select Linked"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        # Big render button
        layout.label(text="Big Button:")
        self.layout.menu(select_links_extended.bl_idname)
        row = layout.row()
        row.scale_y = 3.0
        row.operator("wm.myop")

class find_object_sockets(bpy.types.Operator):
    bl_idname = "my_operator.my_class_name"
    bl_label = "Object Sockets"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        modifiers = bpy.context.active_object.modifiers
        for each in modifiers:
            print(each)
        return {"FINISHED"}

class make_links_extended(bpy.types.Menu):
    bl_label = "Extended"
    bl_idname = "OBJECT_MT_make_links_extended"

    def draw(self, context):
        layout = self.layout

        # layout.operator("wm.open_mainfile")
        # layout.operator("wm.save_as_mainfile").copy = True
        
        modifiers = bpy.context.active_object.modifiers
        for mod in modifiers:
            layout.label(text=mod.type, icon='MODIFIER')
        
        
        active_object = bpy.context.active_object
        selection_list = bpy.context.selected_objects
        object_data = active_object.data.name
        if active_object.type == "CURVE":
            layout.label(text="Curves", icon='CURVE_DATA')
            print(selection_list)
            if len(selection_list) >= 1:
                layout.operator('object.link_curve', text='Taper Object').taper_object = True
                layout.operator('object.link_curve', text='Bevel Object').bevel_object = True
            # bpy.data.curves[object_data]
class select_links_extended(bpy.types.Menu):
    bl_label = "Select Linked Extended"
    bl_idname = "OBJECT_MT_select_linkes_extended"

    def draw(self, context):
        layout = self.layout

        # layout.operator("wm.open_mainfile")
        # layout.operator("wm.save_as_mainfile").copy = True
        layout.operator_menu_enum("object.select_linked", "type", text = "Select Linked")        
        modifiers = bpy.context.active_object.modifiers
        for mod in modifiers:
            layout.separator()
            layout.label(text=mod.name, icon='MODIFIER')
            if mod.type=="MIRROR":
                bpy.data.objects[mod.mirror_object].select_set(True)
                layout.operator('view3d.view_selected', text = mod.mirror_object.name, icon = "OBJECT_DATA")

        active_object = bpy.context.active_object
        selection_list = bpy.context.selected_objects
        object_data = active_object.data.name
        if active_object.type == "CURVE":
            layout.label(text="Curves", icon='CURVE_DATA')
            print(selection_list)
            if len(selection_list) >= 1:
                layout.operator('object.link_curve', text='Taper Object').taper_object = True
                layout.operator('object.link_curve', text='Bevel Object').bevel_object = True
            # bpy.data.curves[object_data]

def add_menu_item(self, context):
    layout = self.layout
    layout.menu(make_links_extended.bl_idname)


    
class link_curve(bpy.types.Operator):
    bl_idname = "object.link_curve"
    bl_label = "Link Curve"
    bl_options = {"REGISTER", "UNDO"}
    taper_object = bpy.props.BoolProperty(name="Taper Object")
    bevel_object = bpy.props.BoolProperty(name="Bevel Object")
    
    def execute(self, context):

        selection_list = bpy.context.selected_objects
        active_object = bpy.context.active_object
        for each in selection_list:
            if self.taper_object: bpy.data.curves[each.data.name].taper_object = active_object
            if self.bevel_object: bpy.data.curves[each.data.name].bevel_object = active_object        
        return {'FINISHED'}

class EdgeToCurve2DOperator(bpy.types.Operator):
    bl_idname = "object.edge_to_curve_2d"
    bl_description = "Description that shows in blender tooltips"
    bl_label = "Edge To Curve 2D"

    def execute(self, context):
        # seperate selected edge to curve
        bpy.ops.mesh.duplicate()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='CURVE')

        selected_objects = bpy.context.selected_objects
        print(len(selected_objects))
        # bpy.ops.object.select
        # convert edge to 2d

        # add profile curve

        return {'FINISHED'}

classes = (
    LayoutDemoPanel,
    find_object_sockets,
    link_curve,
    make_links_extended,
    select_links_extended

)


def register():    
    # lets add the menu
    bpy.types.VIEW3D_MT_make_links.append(add_menu_item)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    bpy.types.VIEW3D_MT_make_links.remove(add_menu_item)
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == "__main__":
    register()