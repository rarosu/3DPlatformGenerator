import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty

bl_info = {
    "name": "Bezier Exporter",
    "description": "Exports a bezier curve",
    "author": "Lars Woxberg, Thomas Sievert",
    "version": (1, 0),
    "blender": (2, 66, 1),
    "location": "File > Import-Export",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Import-Export"}
    
class ExportBezier(bpy.types.Operator, ExportHelper):
    bl_idname = "export_bezier.txt"
    bl_label = 'Export Bezier'
    bl_options = {'PRESET'}
    
    filename_ext = ".txt"
    filter_glob = StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )
    check_extension = True
            
    def execute(self, context):        
        keywords = self.as_keywords()
        filename = keywords["filepath"]

        file = open(filename, "w")
        
        curve = bpy.data.curves[0]
        splines = curve.splines
        
        for s in splines:
            for p in s.bezier_points:
                if p == s.bezier_points[0]:
                    # Exclude left handle
                    file.write("%.3f, %.3f, %.3f " % (p.co.x, p.co.y, p.co.z)) 
                    file.write("%.3f, %.3f, %.3f " % (p.handle_right.x, p.handle_right.y,p.handle_right.z)) 
                elif p == s.bezier_points[-1]:
                    # Exclude right handle
                    file.write("%.3f, %.3f, %.3f " % (p.handle_left.x, p.handle_left.y, p.handle_left.z)) 
                    file.write("%.3f, %.3f, %.3f " % (p.co.x, p.co.y, p.co.z)) 
                else:
                    # Include all control points                    
                    file.write("%.3f, %.3f, %.3f\n" % (p.handle_left.x, p.handle_left.y, p.handle_left.z)) 
                    file.write("%.3f, %.3f, %.3f " % (p.co.x, p.co.y, p.co.z)) 
                    file.write("%.3f, %.3f, %.3f " % (p.handle_right.x, p.handle_right.y,p.handle_right.z))
                    
                    
        file.close()
        
        return { "FINISHED" }

def menu_func_export(self, context):
    self.layout.operator("export_bezier.txt", text="Bezier curve (.txt)")

def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    
if __name__ == "__main__":
    register()