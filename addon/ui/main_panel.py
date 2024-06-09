import bpy
from .. import utils


class PowerSavePanel(bpy.types.Panel):
    bl_idname = 'POWERSAVE_PT_PowerSavePanel'
    bl_category = 'PowerSave'
    bl_label = 'PowerSave'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        prefs = utils.common.prefs()

        layout = self.layout
        column = layout.column()

        powersave_draw(self, column)


def popover(self, context):
    layout = self.layout.row(align=False)
    panel = PowerSavePanel.bl_idname
    icon = utils.ui.get_icon()
    layout.popover(panel, text='', icon_value=icon)


def powersave_draw(self, column: bpy.types.UILayout):
    prefs = utils.common.prefs()
    filepaths = bpy.context.preferences.filepaths

    box = column.box().column()
    if hasattr(bpy.types, 'HOPS_OT_powersave'):
        box.operator('hops.powersave', text='PowerSave (hops)')
    else:
        box.operator('powersave.powersave')
    box.prop(prefs, 'powersave_name', text='')

    column.separator()

    box = column.box().column()
    flow = box.grid_flow(align=True)
    flow.operator('powersave.load_previous', text='', icon='REW')
    flow.operator('powersave.load_next', text='', icon='FF')
    box.operator('powersave.open_project_folder')

    column.separator()

    box = column.box().column()
    box.prop(prefs, 'use_autosave')
    col = box.column()
    col.enabled = prefs.use_autosave
    col.prop(prefs, 'autosave_interval')
    row = col.row(align=True)
    row.prop(prefs, 'autosave_format', text='')
    if prefs.autosave_format == 'CUSTOM':
        op = row.operator('preferences.addon_show', icon='PREFERENCES', text='')
        op.module = utils.common.module()

    column.separator()

    box = column.box().column()
    icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
    box.operator('file.autopack_toggle', text='Toggle Autopack', icon=icon)
    if bpy.app.version >= (2, 93, 0):
        sub = box.row()
        sub.operator_context = 'INVOKE_DEFAULT'
        options = {'do_local_ids': True, 'do_linked_ids': True, 'do_recursive': True}
        utils.ui.draw_op(sub, 'Purge Orphans', 'outliner.orphans_purge', options)
    else:
        box.operator('powersave.purge_orphans', text='Purge Orphans')

    column.separator()
    box = column.box().column()
    box.prop(filepaths, 'use_auto_save_temporary_files')
    col = box.column()
    col.enabled = filepaths.use_auto_save_temporary_files
    col.prop(filepaths, 'auto_save_time')
    box.prop(filepaths, 'save_version')
