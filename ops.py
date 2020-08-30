##############################################################################
##                                                                          ##
##   p_cuboid add-on for Blender 2.83    Copyright (C) 2020  Pan Thistle    ##
##                                                                          ##
##   This program is free software: you can redistribute it and/or modify   ##
##   it under the terms of the GNU General Public License as published by   ##
##   the Free Software Foundation, either version 3 of the License, or      ##
##   (at your option) any later version.                                    ##
##                                                                          ##
##   This program is distributed in the hope that it will be useful,        ##
##   but WITHOUT ANY WARRANTY; without even the implied warranty of         ##
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          ##
##   GNU General Public License for more details.                           ##
##                                                                          ##
##   You should have received a copy of the GNU General Public License      ##
##   along with this program.  If not, see <https://www.gnu.org/licenses/>. ##
##                                                                          ##
##############################################################################


# ------------------------------------------------------------------------
#    IMPORTED DATA
# ------------------------------------------------------------------------

import bpy
import bmesh


# ------------------------------------------------------------------------
#    p_cuboid class
# ------------------------------------------------------------------------

class p_cuboid:
    ''' cuboid base class '''
    def __init__(self, rad, res, tone):
        self.__verts = []
        self.__faces = []
        self.__setup(rad, res, tone)
        
    def verts(self):
        return self.__verts.copy()
    
    def faces(self):
        return self.__faces.copy()
                    
    def __setup(self, rad, res, tone):
        pts = [i + 1 for i in res]
        inc = [self.__ease_list(tone[i], 2 * rad[i], pts[i]) for i in range(3)]
        idx = 0
        # top
        scan = self.__lscan_one(pts[0] * pts[1], idx)
        seams_a = self.__lnk_plane_seams(pts[0], pts[1], scan)
        self.__faces += self.__lnk_plane_faces(pts[0], pts[1], scan, False)
        self.__verts += [[rad[0] - inc[0][j], rad[1] - inc[1][i], rad[2]] 
                        for i in range(pts[1]) for j in range(pts[0])]
        idx += pts[0] * pts[1]
        # bottom
        scan = self.__lscan_one(pts[0] * pts[1], idx)
        seams_b = self.__lnk_plane_seams(pts[0], pts[1], scan)
        self.__faces += self.__lnk_plane_faces(pts[0], pts[1], scan, True)
        self.__verts += [[rad[0] - inc[0][j], rad[1] - inc[1][i], -rad[2]] 
                        for i in range(pts[1]) for j in range(pts[0])]
        idx += pts[0] * pts[1]
        # far
        scan = self.__lscan_three(idx, seams_a[0], seams_b[0], pts[0], pts[2])
        seams_c = self.__lnk_plane_seams(pts[0], pts[2], scan)
        self.__faces += self.__lnk_plane_faces(pts[0], pts[2], scan, True)
        self.__verts += [[rad[0] - inc[0][j], rad[1], rad[2] - inc[2][i]] 
                        for i in range(1, res[2]) for j in range(pts[0])]
        idx += (res[2] - 1) * pts[0]
        # near
        scan = self.__lscan_three(idx, seams_a[2], seams_b[2], pts[0], pts[2])
        seams_d = self.__lnk_plane_seams(pts[0], pts[2], scan)
        self.__faces += self.__lnk_plane_faces(pts[0], pts[2], scan, False)
        self.__verts += [[rad[0] - inc[0][j], -rad[1], rad[2] - inc[2][i]] 
                        for i in range(1, res[2]) for j in range(pts[0])]
        idx += (res[2] - 1) * pts[0]
        # right   
        scan = self.__lscan_five(idx, seams_a[3], seams_b[3], seams_c[3], 
                                    seams_d[3], pts[1], pts[2])
        seams_e = self.__lnk_plane_seams(pts[1], pts[2], scan)
        self.__faces += self.__lnk_plane_faces(pts[1], pts[2], scan, False)
        self.__verts += [[rad[0], rad[1] - inc[1][j], rad[2] - inc[2][i]] 
                        for i in range(1, res[2]) for j in range(1, res[1])]
        idx += (res[2] - 1) * (res[1] - 1)
        # left
        scan = self.__lscan_five(idx, seams_a[1], seams_b[1], seams_c[1], 
                                    seams_d[1], pts[1], pts[2])
        seams_f = self.__lnk_plane_seams(pts[1], pts[2], scan)
        self.__faces += self.__lnk_plane_faces(pts[1], pts[2], scan, True)
        self.__verts += [[-rad[0], rad[1] - inc[1][j], rad[2] - inc[2][i]] 
                        for i in range(1, res[2]) for j in range(1, res[1])]

    def __ease_in_out(self, t, p = 1):    
        return (t * 2)**p / 2 if t < 0.5 else 1 - (((1 - t) * 2)**p / 2)

    def __ease_list(self, exponent, length, count):
        step = 1 / (count - 1)
        return [self.__ease_in_out(i * step, exponent) * length
                for i in range(count)]

    def __lnk_plane_faces(self, apts, bpts, lscan, flip = False):
        faces = []
        for i in range(bpts - 1):
            j_loop = apts * i
            for j in range(apts - 1):
                face = [lscan[j + j_loop], lscan[j + j_loop + 1], 
                        lscan[j + j_loop + apts + 1], lscan[j + j_loop + apts]]
                faces.append(face[::-1] if flip else face)
        return faces

    def __lnk_plane_seams(self, apts, bpts, lscan):
        ares = apts - 1
        bres = bpts - 1
        npts = apts * bpts
        return [
                [lscan[i] for i in range(apts)],
                [lscan[ares + i * apts] for i in range(bpts)],
                [lscan[i] for i in range(bres * apts, npts)],
                [lscan[i * apts] for i in range(bpts)]
                ]

    def __lscan_one(self, apts, nidx = 0):
        return [nidx + i for i in range(apts)]

    def __lscan_three(self, nidx, seam_a, seam_b, apts, bpts):
        bres = bpts - 2
        ls = []
        ls += seam_a            
        ls += [nidx + j + apts * i for i in range(bres) for j in range(apts)]      
        ls += seam_b
        return ls

    def __lscan_five(self, nidx, seam_a, seam_b, seam_c, seam_d, apts, bpts):
        bres = bpts - 2
        ares = apts - 2
        ls = []
        ls += seam_a
        for i in range(bres):
            ls.append(seam_c[i + 1])
            j_loop = ares * i
            ls += [nidx + j_loop + j for j in range(ares)]
            ls.append(seam_d[i + 1])
        ls += seam_b
        return ls


# ------------------------------------------------------------------------
#    OPERATOR
# ------------------------------------------------------------------------

class MESH_OT_p_cuboid_add(bpy.types.Operator):
    bl_label = "Add Cuboid"
    bl_idname = "mesh.p_cuboid_add"
    bl_description = "Add Cuboid"
    bl_options = {'REGISTER', 'UNDO'}

    wire: bpy.props.BoolProperty(
        name = 'Wire', description = 'Show wireframe', 
        default = True
        )
    res: bpy.props.IntVectorProperty(
        name = 'Resolution', description = 'Resolution', 
        default = [3, 3, 3], min = 1, max = 10, size = 3
        )
    rad: bpy.props.FloatVectorProperty(
        name = 'Radius', description = 'Radius', 
        default = [2.0, 1.0, 1.0], min = 0.01, max = 10, size = 3
        )
    tone: bpy.props.FloatVectorProperty(
        name = 'Tone', description = 'Tone', 
        default = [5.0, 3.0, 3.0], min = 0.1, max = 9, size = 3
        )

    @classmethod
    def poll(self, context):
        return (context.area.type == 'VIEW_3D' and context.mode == 'OBJECT')

    def execute(self, context):
        p_cub = p_cuboid(self.rad, self.res, self.tone)
        verts = p_cub.verts()
        faces = p_cub.faces()
        name = 'p_cuboid'
        me = bpy.data.meshes.new(name)
        bm = bmesh.new(use_operators = False)
        bmv = [bm.verts.new(v) for v in verts]
        for f in faces:        
            bm.faces.new((bmv[f[0]], bmv[f[1]], bmv[f[2]], bmv[f[3]]))
        bm.to_mesh(me)
        me.update()
        bm.free()
        ob = bpy.data.objects.new(name, me)
        context.scene.collection.objects.link(ob) 
        ob.show_wire = self.wire
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align = True)
        split = row.split()
        split.alignment = 'RIGHT'
        split.label(text = 'Radius:')
        split.prop(self, 'rad', text = '')
        row = layout.row(align = True)
        split = row.split()
        split.alignment = 'RIGHT'
        split.label(text = 'Resolution:')
        split.prop(self, 'res', text = '')
        row = layout.row(align = True)
        split = row.split()
        split.alignment = 'RIGHT'
        split.label(text = 'Tone:')
        split.prop(self, 'tone', text = '')
        row = layout.row(align = True)
        split = row.split()
        split.alignment = 'RIGHT'
        split.label(text = 'Wire:')
        split.prop(self, 'wire', text = '')


# ------------------------------------------------------------------------
#    ADD-MESH MENU (APPEND OPERATOR TO UI DRAW)
# ------------------------------------------------------------------------

def mesh_add_menu_draw(self, context):
    self.layout.operator('mesh.p_cuboid_add', icon = 'CUBE')


# ------------------------------------------------------------------------
#    REGISTER/UNREGISTER
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(MESH_OT_p_cuboid_add)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)

def unregister():
    bpy.utils.unregister_class(MESH_OT_p_cuboid_add)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)