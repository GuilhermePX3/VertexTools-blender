bl_info = {
    "name": "Random Vertex Color",
    "author": "Seu Nome",
    "version": (1, 17),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Vertex Color",
    "description": "Paint randomly all selected meshes or meshes in the selected collection",
    "category": "Paint",
}

import bpy
import random


def random_vertex_color(objects, self):
    color = (random.random(), random.random(), random.random(), 1.0)

    self.report({'INFO'}, f"Generated {round(color[0],2)} color")

    for obj in objects:
        if obj.type == "MESH":
            mesh = obj.data
            mesh.vertex_colors.new(name="RandomColor")
            color_layer = mesh.vertex_colors["RandomColor"]
            
            self.report({'INFO'}, f"N o Polygons {len(mesh.polygons)}*")

            for poly in mesh.polygons:
                for loop_index in poly.loop_indices:
                    color_layer.data[loop_index].color = color


class RandomVertexColorOperator(bpy.types.Operator):
    bl_idname = "object.random_vertex_color"
    bl_label = "Generate (v1.17)"
    bl_description = "Generate random vertex colors for selected meshes or meshes in selected collection"

    def execute(self, context):
        collection = bpy.context.collection
        selected_objects = bpy.context.selected_objects
        mesh_objects = []            

        if collection and len(selected_objects) == 0:
            self.report({'INFO'}, "Collection Found: " + collection.name)

            for obj in collection.all_objects:
                if obj.type == "MESH":
                    mesh_objects.append(obj)
        else:
            for obj in selected_objects:
                self.report({'INFO'}, "No collection found, next object type: " + obj.type + " / ")
                if obj.type == "MESH":
                    mesh_objects.append(obj)

            if len(mesh_objects) == 0:
                self.report({'INFO'}, "No meshes found.")
                return {'CANCELLED'}

        self.report({'INFO'}, f"Trying to paint {len(mesh_objects)} meshes")
        random_vertex_color(mesh_objects, self)

        return {'FINISHED'}


class RandomVertexColorPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_random_vertex_color"
    bl_label = "Vertex Color (v1.17)"
    bl_category = "Vertex Color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.random_vertex_color", text="Generate (v1.17)")


classes = (RandomVertexColorOperator, RandomVertexColorPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
