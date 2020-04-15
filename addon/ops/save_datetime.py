import bpy
from .. import utils


class SaveDatetime(bpy.types.Operator):
    bl_idname = "powersave.save_datetime"
    bl_label = "Save Datetime"
    bl_description = "Save this blend file in your PowerSave folder with a name based on the current date and time"

    @classmethod
    def poll(cls, context):
        return not bpy.data.is_saved

    def execute(self, context):
        result = utils.save.save_datetime()
        self.report(result[0], result[1])
        return result[2]
