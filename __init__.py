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
#    META DATA [ MCutter info ]
# ------------------------------------------------------------------------

bl_info = {
    "name": "p_cuboid",
    "description": "Add custom cuboid mesh object",
    "author": "Pan Thistle",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "View3D > Add > Mesh",
    "doc_url": "https://github.com/panthistle/p_cuboid_Blender_add-on",
    "category": "Add Mesh"
}


# ------------------------------------------------------------------------
#    IMPORTED DATA
# ------------------------------------------------------------------------

import bpy
from . import ops


# ------------------------------------------------------------------------
#    REGISTER/UNREGISTER
# ------------------------------------------------------------------------

def register():
    ops.register()

def unregister():
    ops.unregister()