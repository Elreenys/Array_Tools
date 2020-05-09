# -*- coding: utf-8 -*-
import bpy
from bpy.types import Panel, AddonPreferences

from . import cfg

# ---------------------------- Panel --------------------------------
class UIPANEL_PT_def(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Array Tools"


class UIPANEL_PT_trans(UIPANEL_PT_def):
    """Panel containing the settings for translation, scale and rotation array"""
    bl_label = "Array Tools"

    @classmethod
    def poll(cls, context):

        return (context.object is not None and len(context.selected_objects) > 0 and (context.object.mode == 'OBJECT'))

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        my_prop = scn.arraytools_prop

        row = layout.row()
        row.operator('scene.at_op')
        row = layout.row()
        if not my_prop.already_start:
            row.alignment = 'CENTER'
            row.label(text="~ Click to begin ~")
        else:
            row.prop(my_prop, 'is_copy')
            row.prop(my_prop, 'count')
            row = layout.row(align=True)
            row.scale_y = 0.7
            row.alignment = 'CENTER'
            row.operator('scene.at_select_all')
            row.alignment = 'LEFT'
            row.operator('scene.at_modifiers')
            box = layout.box()
            box.label(text="Translation")
            col = box.column()
            split = col.split()
            split.prop(my_prop, 'tr_offset')
            split.prop(my_prop, 'tr_global')

            row = layout.row()
            row.prop(my_prop, 'at_pivot')

            box = layout.box()
            box.label(text="Scaling (%)")
            col = box.column()
            split = col.split()
            split.prop(my_prop, 'sc_offset')
            split.prop(my_prop, 'sc_global')

            box = layout.box()
            split = box.split(factor=0.6)
            if scn.unit_settings.system_rotation == 'DEGREES':
                split.label(text="Rotation (Degrees)")
            else:
                split.label(text="Rotation (Radians)")
            row = split.row()
            row.prop(my_prop, 'rot_axis', expand=True)

            split = box.split(factor=0.08)

            col = split.column(align=True)
            col.label(text='')
            col.operator('scene.x360', text='X')
            col.operator('scene.y360', text='Y')
            col.operator('scene.z360', text='Z')

            col = split.column()
            col.prop(my_prop, 'rot_offset')
            col = split.column()
            col.prop(my_prop, 'rot_global')

            box = layout.box()
            row = box.row()
            row.scale_y = 1.5
            row.operator('scene.at_done')
            row.operator('scene.at_cancel')

            row = box.row()
            row.scale_y = 0.3
            row.alignment = 'CENTER'
            row.label(text="~ Transforms are NOT applied ~")


class UIPANEL_PT_rows(UIPANEL_PT_def):
    """Panel containing the row options"""
    bl_parent_id = 'UIPANEL_PT_trans'
    bl_label = 'Rows Options'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        my_prop = context.scene.arraytools_prop

        if my_prop.already_start:
            row = layout.row()
            row.prop(my_prop, 'count')
            row.prop(my_prop, 'row')
            row = layout.row()

            row.scale_y = 0.8
            row.prop(my_prop, 'align', icon_only=True, expand=True)
            row.prop(my_prop, 'alter')
            row = layout.row()

            row.alignment = 'CENTER'
            row.scale_x = 1.5
            row.scale_y = 0.6
            row.label(text=" - Offset Settings -")
            row.scale_x = 0.8
            row.operator('scene.at_reset_second')

            layout.use_property_split = True

            col = layout.column()
            row = col.row(align=True)
            row.prop(my_prop, 'tr_second')
            col = layout.column()
            row = col.row(align=True)
            row.prop(my_prop, 'sc_second')
            col = layout.column()
            row = col.row(align=True)
            row.prop(my_prop, 'rot_second')

            row = layout.row()
            row.scale_y = 0.5
            row.label(text="Total : " + my_prop.total + "    |    current Row : " + my_prop.erow)        


class UIPANEL_PT_options(UIPANEL_PT_def):
    """Panel containing the random options"""
    bl_parent_id = 'UIPANEL_PT_trans'
    bl_label = 'Random Options'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        my_prop = context.scene.arraytools_prop

        layout.enabled = my_prop.already_start
        row = layout.row()
        row.alignment = 'CENTER'
        row.prop(my_prop, 'at_seed')
        row = layout.row()
        row.prop(my_prop, 'at_mode', expand=True)
        row = layout.row()
        if my_prop.at_mode == 'SIM':
            row.prop(my_prop, 'at_is_tr')
            row = layout.row()
            row.prop(my_prop, 'tr_rand')
            row = layout.row()
            row.prop(my_prop, 'at_is_sc')
            row = layout.row()
            row.prop(my_prop, 'sc_rand')
            row = layout.row()
            row.prop(my_prop, 'at_is_rot')
            row = layout.row()
            row.prop(my_prop, 'rot_rand')
        else:
            row.label(text='  ')
            row.label(text='X')
            row.label(text='Y')
            row.label(text='Z')
            row = layout.row()
            row.prop(my_prop, 'at_is_tr')
            row.scale_x = 0.5
            row.scale_y = 0.7
            row.operator('scene.at_reset_tr')
            row.operator('scene.fill_tr')
            row = layout.row()
            row.prop(my_prop, 'tr_min')
            row = layout.row()
            row.prop(my_prop, 'tr_max')
            row = layout.row()

            row.prop(my_prop, 'at_is_sc')
            row.scale_x = 0.5
            row.scale_y = 0.7
            row.operator('scene.at_reset_sc')
            row.operator('scene.fill_sc')
            row = layout.row()
            row.alignment = "CENTER"
            row.scale_y = 0.7
            row.prop(my_prop, 'sc_all')
            row = layout.row(align=True)
            row.label(text='min:')
            row.prop(my_prop, 'sc_min_x', text='')
            row.prop(my_prop, 'sc_min_y', text='')
            row.prop(my_prop, 'sc_min_z', text='')
            row = layout.row(align=True)
            row.label(text='max:')
            row.prop(my_prop, 'sc_max_x', text='')
            row.prop(my_prop, 'sc_max_y', text='')
            row.prop(my_prop, 'sc_max_z', text='')

            row = layout.row()
            row.prop(my_prop, "at_is_rot")
            row.scale_x = 0.5
            row.scale_y = 0.7
            row.operator('scene.at_reset_rot')
            row.operator('scene.fill_rot')
            row = layout.row()
            row.prop(my_prop, 'rot_min')
            row = layout.row()
            row.prop(my_prop, 'rot_max')

        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="___________________________")
        box = layout.box()
        row = box.row()
        row.prop(my_prop, 'at_nb_mask')
        row = box.row()
        row.operator('scene.at_mask')
        row.operator('scene.at_reset_mask')

panels = (UIPANEL_PT_options, UIPANEL_PT_rows, UIPANEL_PT_trans)

# ---------------------------- Preferences --------------------------
def update_category(self, context):
    """Update the tab category of the addon"""
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:       
                bpy.utils.unregister_class(panel)
        prefs = context.preferences.addons[__package__].preferences
    
        UIPANEL_PT_def.bl_category = prefs.category
        for panel in reversed(panels):
            bpy.utils.register_class(panel)
        
    except Exception as e:
        print("\nError in updating category tab")
        pass


class ArrayToolsPrefs(AddonPreferences):
    bl_idname = __package__

    category: bpy.props.StringProperty(
        name="Category",
        default="Array Tools",
        update=update_category
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 0.2
        row.alignment = 'CENTER'
        row.label(text=" ~ Choose the tab name for the addon. ~")
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text = "Tab Name: ")
        row.alignment = 'LEFT'
        row.prop(self, 'category', text='')

