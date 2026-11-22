"""Low-poly, flat-color block-outs of the Italian coastal town buildings
from assets/env/italian_town.webp (row 2 of the concept sheet).

Run headless:
  blender -b --factory-startup --python art/blockouts/italian_town/build_town_houses.py

Writes next to this script:
  italian_town_houses.blend   all houses side by side, one object each
  glb/<name>.glb              one file per house, origin at bottom-centre, +Z up, front faces -Y
  previews/*.png              flat-outline and studio-lit renders
Units are metres; one storey is about 3 m.
"""
import json
import math
import os
import random

import bpy
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_GLB = os.path.join(HERE, "glb")
OUT_PNG = os.path.join(HERE, "previews")
os.makedirs(OUT_GLB, exist_ok=True)
os.makedirs(OUT_PNG, exist_ok=True)

# ---------------------------------------------------------------- palette
# Colours after the sunny-lakeside reference: warm cream plaster, orange-red roofs, olive/sage greens,
# cobalt-blue glass and accents (shadows come out cool blue from the sky light).
PALETTE = {
    "plaster_cream": "EED9B2",
    "plaster_yellow": "EDB650",
    "plaster_white": "F2E8D2",
    "plaster_peach": "F0BF8F",
    "plaster_terra": "C8512F",
    "stone": "D7C29C",
    "stone_dark": "A8947A",
    "trim_white": "F6F0E2",
    "roof": "E9622E",
    "roof_dark": "B5452A",
    "shutter_green": "527A3A",
    "door_brown": "6E4430",
    "glass": "4C76C4",
    "glass_dark": "2E3F78",
    "awning_red": "D94A35",
    "awning_blue": "2B54C4",
    "awning_green": "7FA544",
    "pink": "EE8FB0",
    "foliage": "8FA43F",
    "foliage_dark": "5E7030",
    "ivy": "6F8A34",
    "ivy_dark": "4D6428",
    "tree_a": "9AA845", "tree_b": "7C8E38", "tree_c": "B8BE5C", "trunk": "6B4A33",
    "pampas": "EADBB2", "pampas_stem": "B9A66E",
    "pot": "C75F37",
    "gold": "F2C230",
    "wood": "B47F4C",
    "fish": "4A86D9",
    "ice": "DDF1FA",
    "counter_pink": "F4A6B8",
    "scoop": "F7B6C8",
    "cone": "E9A85A",
    "lamp": "FFE27A",
    "iron": "2E2E33",
    "cloth_blue": "8CC6F0",
    "flower_yellow": "F7D84A",
    "steel": "B8C2CC",
    # combat maps + Cat Sanctuary (taken from the colours the game drew these with)
    "sq_stone": "DCC6A0", "sq_stone_light": "EDDDBB", "sq_water": "5F9BE0", "sq_water_deep": "3E72C6",
    "bush_yellow": "D9B84A", "bush_green": "8FA43F", "bush_lime": "AEB759",
    "mush_stem": "F4EAD8", "mush_cap": "D9473F", "mush_dot": "FFF6EA",
    "lamp_blue": "4A5F86", "lamp_glass": "CFE4F2", "bench_wood": "C98A5C", "bench_leg": "5B6B8F",
    "crate_wood": "B07A42", "crate_dark": "7A5228", "basket": "C99A55", "basket_dark": "8A6532", "cloth": "E8F1FF",
    "barrel_wood": "8A5A32", "barrel_band": "3D3D44",
    "cone_orange": "FF7A2A", "barrier_yellow": "FFD23C", "barrier_black": "2B2320", "barrier_leg": "666666",
    "grass_a": "7E9538", "grass_b": "A3B04E",
    "yarn": "B06EEB", "yarn_light": "D9A8F7", "cuke": "4F9A34", "cuke_light": "8CC85A", "cuke_dark": "2F6B22",
    # the Cat Sanctuary diorama: soft pastels
    "room_base": "B98A6A", "room_floor": "D4A27A", "room_floor_dark": "B4825C",
    "room_skirt": "F6EDE4", "room_trim": "F6EDE4",
    "room_wall_n_rose": "F4CFC6", "room_wall_w_rose": "F7DAD2", "room_wainscot_rose": "E8A9A0", "room_cap_rose": "E9B9AE",
    "room_wall_n_mint": "D3EDE2", "room_wall_w_mint": "DFF3EA", "room_wainscot_mint": "9FD3BE", "room_cap_mint": "B8DCCB",
    "room_wall_n_cream": "F3E7CF", "room_wall_w_cream": "F7EEDC", "room_wainscot_cream": "D8C3A0", "room_cap_cream": "E3D3B4",
    "room_wall_n_all": "F4CFC6", "room_wall_w_all": "F7DAD2", "room_wainscot_all": "E8A9A0", "room_cap_all": "E9B9AE",
    "floor_tile_a": "F2E2C6", "floor_tile_b": "C9B396", "floor_grout": "8E9AA8",
    "floor_stone_a": "B9C3CE", "floor_stone_b": "A9B5C2", "floor_stone_c": "C8D0D8", "room_sky": "9CD3F0", "room_cloud": "FFFFFF", "room_curtain": "7FB7A4",
    "room_poster_a": "FCE8C8", "room_poster_b": "BFE0D6", "room_cushion": "E98AA6",
    "rug_a": "E9B44C", "rug_b": "7FB7A4", "rug_c": "EE8E8E", "rug_d": "8FA8D8",
    "catnip_bag": "E9D9B4", "catnip_string": "C0472F", "catnip_leaf": "6FB84A",
    "cardboard": "C99A62", "cardboard_dark": "A77B48", "cardboard_light": "DDB27A", "cardboard_tape": "E8D7AE",
    "squirt_blue": "5ABEFF", "squirt_head": "F26B5B", "salmon": "F59A6E", "nori": "2E3A2C",
    "tempura": "F2A93E", "shrimp_tail": "F0603A", "caviar": "1E1A24", "lemon": "F7D84A",
    "star": "F08A4B", "star_dot": "FFD2A8", "shell_white": "FFF0E6", "shell_pink": "FFD0D8",
    "pebble_a": "B9ADA0", "pebble_b": "9C9086", "pebble_c": "D6CCC0",
    "post_base": "B48A5A", "rope": "D8B98A", "bed_blue": "5A7EC4", "bed_cushion": "EFE4FF",
    "bowl_blue": "3D6EA5", "bowl_inner": "2F5A8A", "terracotta": "C4632B", "catgrass": "5EA83A",
    "cushion": "B58AD8", "cushion_top": "D6B6F0", "toy_red": "E04A3A", "fountain_white": "D9E4EC", "water_blue": "6FC3EE",
    "brick": "9A6A52", "mantel": "5A3A2A", "soot": "2B1D16", "lamp_globe": "FFF4C0", "brass": "C9A24A",
    "tank_wood": "6B4A2E", "tank_water": "78C8F0", "sand": "E8C070", "hammock": "F2B84B", "hammock_rope": "8A5A32",
}
_mats = {}


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def mat(key):
    if key in _mats:
        return _mats[key]
    h = PALETTE[key]
    rgb = [srgb_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    m = bpy.data.materials.new("town_" + key)
    m.diffuse_color = (*rgb, 1.0)
    m.roughness = 1.0
    m.metallic = 0.0
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 1.0
    _mats[key] = m
    return m


# ---------------------------------------------------------------- primitives
class Parts:
    """Collects the pieces of one building so they can be joined."""

    def __init__(self):
        self.objs = []

    def _add(self, ob, key):
        ob.data.materials.clear()
        ob.data.materials.append(mat(key))
        self.objs.append(ob)
        return ob

    def box(self, key, size, loc, rot=(0, 0, 0)):
        """size=(x,y,z); loc = centre x, centre y, BOTTOM z (before rotation)."""
        bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], loc[2] + size[2] / 2), rotation=rot)
        ob = bpy.context.active_object
        ob.scale = size
        return self._add(ob, key)

    def boxc(self, key, size, center, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=center, rotation=rot)
        ob = bpy.context.active_object
        ob.scale = size
        return self._add(ob, key)

    def cyl(self, key, r, depth, center, rot=(0, 0, 0), verts=10, scale=(1, 1, 1)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=center, rotation=rot)
        ob = bpy.context.active_object
        ob.scale = scale
        return self._add(ob, key)

    def cone(self, key, r1, r2, depth, center, rot=(0, 0, 0), verts=8, scale=(1, 1, 1)):
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=center, rotation=rot)
        ob = bpy.context.active_object
        ob.scale = scale
        return self._add(ob, key)

    def blob(self, key, r, center, scale=(1, 1, 1)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=center)
        ob = bpy.context.active_object
        ob.scale = scale
        return self._add(ob, key)

    def mesh(self, key, verts, faces, name="m"):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.update()
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        return self._add(ob, key)

    # --- roofs -------------------------------------------------------
    def gable(self, key, w, d, rise, z0, cx=0.0, cy=0.0, ridge_x=True):
        """Triangular prism. ridge_x: ridge runs along X (eaves face front);
        otherwise the gable end faces front (-Y)."""
        if ridge_x:
            hw, hd = w / 2, d / 2
            v = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0), (-hw, 0, rise), (hw, 0, rise)]
        else:
            hw, hd = w / 2, d / 2
            v = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0), (0, -hd, rise), (0, hd, rise)]
        v = [(x + cx, y + cy, z + z0) for x, y, z in v]
        if ridge_x:
            f = [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5), (3, 2, 1, 0)]
        else:
            f = [(1, 2, 5, 4), (3, 0, 4, 5), (0, 1, 4), (2, 3, 5), (3, 2, 1, 0)]
        return self.mesh(key, v, f, "roof")

    def hip(self, key, w, d, rise, z0, cx=0.0, cy=0.0):
        hw, hd = w / 2, d / 2
        inset = min(hw, hd) * 0.95
        v = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0),
             (-hw + inset, 0, rise), (hw - inset, 0, rise)]
        v = [(x + cx, y + cy, z + z0) for x, y, z in v]
        f = [(0, 1, 5, 4), (2, 3, 4, 5), (3, 0, 4), (1, 2, 5), (3, 2, 1, 0)]
        return self.mesh(key, v, f, "roof")

    # --- facade details ---------------------------------------------
    def window(self, x, zc, w, h, wall_y, shutters="shutter_green", frame="trim_white", glass="glass", sill=True):
        self.boxc(frame, (w + 0.24, 0.10, h + 0.24), (x, wall_y - 0.04, zc))
        self.boxc(glass, (w, 0.12, h), (x, wall_y - 0.07, zc))
        self.boxc(frame, (0.08, 0.14, h), (x, wall_y - 0.08, zc))  # mullion
        if sill:
            self.boxc(frame, (w + 0.4, 0.3, 0.1), (x, wall_y - 0.15, zc - h / 2 - 0.12))
        if shutters:
            sw = w / 2 + 0.05
            for s in (-1, 1):
                self.boxc(shutters, (sw, 0.1, h + 0.1), (x + s * (w / 2 + 0.12 + sw / 2), wall_y - 0.05, zc))

    def arch_window(self, x, z0, w, h, wall_y, glass="glass", frame="trim_white"):
        self.door(x, z0, w + 0.2, h + 0.1, wall_y + 0.02, frame)
        self.door(x, z0 + 0.05, w, h - 0.05, wall_y - 0.02, glass)

    def door(self, x, z0, w, h, wall_y, key="door_brown", arched=True, depth=0.16):
        if arched:
            r = w / 2
            self.box(key, (w, depth, h - r), (x, wall_y - depth / 2 + 0.02, z0))
            self.cyl(key, r, depth, (x, wall_y - depth / 2 + 0.02, z0 + h - r), rot=(math.pi / 2, 0, 0), verts=12)
        else:
            self.box(key, (w, depth, h), (x, wall_y - depth / 2 + 0.02, z0))

    def awning(self, xc, width, z_top, wall_y, depth, colors, stripes=8, angle=0.38):
        sw = width / stripes
        dy, dz = math.cos(angle) * depth, math.sin(angle) * depth
        for i in range(stripes):
            x = xc - width / 2 + sw * (i + 0.5)
            key = colors[i % len(colors)]
            self.boxc(key, (sw, depth, 0.08), (x, wall_y - dy / 2, z_top - dz / 2), rot=(angle, 0, 0))
            # scalloped valance: half-discs hanging from front edge
            self.cyl(key, sw / 2, 0.06, (x, wall_y - dy, z_top - dz - 0.02), rot=(math.pi / 2, 0, 0), verts=10)
        self.box(colors[0], (width, 0.06, 0.18), (xc, wall_y - dy, z_top - dz - 0.12))

    def planter(self, x, y, r=0.45, flowers="pink", z0=0.0):
        hpot = r * 1.3
        self.cone("pot", r * 0.75, r, hpot, (x, y, z0 + hpot / 2), verts=8)
        self.box("roof_dark", (r * 2.15, r * 2.15, 0.1), (x, y, z0 + hpot - 0.05), rot=(0, 0, math.pi / 8))
        self.blob("foliage", r * 1.05, (x, y, z0 + hpot + r * 0.55), scale=(1, 1, 0.85))
        if flowers:
            for a in range(4):
                ang = a * math.pi / 2 + 0.4
                self.blob(flowers, r * 0.32, (x + math.cos(ang) * r * 0.6, y + math.sin(ang) * r * 0.6, z0 + hpot + r * 0.95))

    def vine(self, pts, r=0.45, flower_every=2, flowers="pink"):
        for i, p in enumerate(pts):
            self.blob("foliage", r, p)
            if flowers and i % flower_every == 0:
                self.blob(flowers, r * 0.55, (p[0], p[1] - r * 0.7, p[2] + r * 0.3))

    def railing(self, xc, width, y, z0, posts=6, h=0.8, key="trim_white"):
        self.box(key, (width, 0.12, 0.1), (xc, y, z0 + h - 0.1))
        for i in range(posts):
            x = xc - width / 2 + width * i / (posts - 1)
            self.box(key, (0.1, 0.1, h - 0.1), (x, y, z0))

    def mesh_multi(self, keys, verts, faces, face_keys, name="m"):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.update()
        for k in keys:
            me.materials.append(mat(k))
        for poly, k in zip(me.polygons, face_keys):
            poly.material_index = keys.index(k)
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        self.objs.append(ob)
        return ob

    def text(self, key, body, center, size, rot=(math.pi / 2, 0, 0), extrude=0.04):
        bpy.ops.object.text_add(location=center, rotation=rot)
        ob = bpy.context.active_object
        ob.data.body = body
        ob.data.size = size
        ob.data.extrude = extrude
        ob.data.align_x = "CENTER"
        ob.data.align_y = "CENTER"
        ob.data.resolution_u = 4
        bpy.ops.object.convert(target="MESH")
        ob = bpy.context.active_object
        return self._add(ob, key)

    def tri_prism(self, key, pts, y=0.0, t=0.05):
        """Thin flat panel from three (x, z) points, centred on y."""
        v = [(x, y - t / 2, z) for x, z in pts] + [(x, y + t / 2, z) for x, z in pts]
        f = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
        return self.mesh(key, v, f, "panel")

    def torus(self, key, R, r, center, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_torus_add(major_segments=10, minor_segments=5, major_radius=R, minor_radius=r,
                                         location=center, rotation=rot)
        return self._add(bpy.context.active_object, key)

    def barrel(self, x, y, z0=0.0, r=0.42, h=0.95):
        self.cyl("wood", r, h, (x, y, z0 + h / 2), verts=10)
        for dz in (0.2, h - 0.2):
            self.cyl("iron", r + 0.03, 0.07, (x, y, z0 + dz), verts=10)

    def crate(self, x, y, z0=0.0, s=0.85, rz=0.0):
        self.box("wood", (s, s, s * 0.85), (x, y, z0), rot=(0, 0, rz))
        for dz in (0.0, s * 0.85 - 0.1):
            self.box("door_brown", (s + 0.04, s + 0.04, 0.1), (x, y, z0 + dz), rot=(0, 0, rz))

    def cross_window(self, x, zc, w, h, wall_y, shutters=None):
        self.window(x, zc, w, h, wall_y, shutters=shutters)
        self.boxc("trim_white", (w, 0.14, 0.08), (x, wall_y - 0.08, zc))

    # --- detail pass (the reference's level of detail) ---------------
    def roof_rows(self, w, d, rise, z0, cx=0.0, cy=0.0, kind="gable_x", n=6, key="roof_dark"):
        """Tile courses as thin bars across the roof slopes, plus a ridge cap.
        kind: gable_x (ridge along X), gable_y (gable end to the front), hip."""
        hw, hd = w / 2, d / 2
        if kind == "gable_y":
            a = math.atan2(rise, hw)
            for i in range(1, n):
                t = i / n
                for s in (-1, 1):
                    self.boxc(key, (0.07, d, 0.05), (cx + s * hw * (1 - t), cy, z0 + rise * t + 0.05), rot=(0, s * a, 0))
            self.boxc(key, (0.22, d + 0.04, 0.16), (cx, cy, z0 + rise + 0.02))
            return
        inset = min(hw, hd) * 0.95 if kind == "hip" else 0.0
        a = math.atan2(rise, hd)
        for i in range(1, n):
            t = i / n
            bw = w - 2 * inset * t
            for s in (-1, 1):
                self.boxc(key, (bw, 0.07, 0.05), (cx, cy + s * hd * (1 - t), z0 + rise * t + 0.05), rot=(-s * a, 0, 0))
            if kind == "hip":
                a2 = math.atan2(rise, inset)
                for s in (-1, 1):
                    self.boxc(key, (0.07, d * (1 - t) - 0.1, 0.05), (cx + s * (hw - inset * t), cy, z0 + rise * t + 0.05), rot=(0, s * a2, 0))
        self.boxc(key, (w - 2 * inset + 0.1, 0.22, 0.16), (cx, cy, z0 + rise + 0.02))

    def ivy(self, x0, x1, z0, z1, wall_y, seed=1, n=28, flowers=0.15, face="front"):
        """A patch of ivy hugging a wall (face front: wall at y=wall_y; face east: wall at x=wall_y,
        x0..x1 run along y)."""
        rnd = random.Random(seed)
        strands = max(2, n // 7)
        for s in range(strands):
            # each strand climbs from the bottom, wandering sideways, thinning toward its tip
            u = x0 + (x1 - x0) * (s + rnd.uniform(0.2, 0.8)) / strands
            z = z0
            top = z0 + (z1 - z0) * rnd.uniform(0.55, 1.0)
            while z < top:
                k = (z - z0) / max(0.01, top - z0)
                r = rnd.uniform(0.26, 0.42) * (1 - 0.45 * k)
                for _ in range(2):
                    du, dz = rnd.uniform(-0.22, 0.22), rnd.uniform(-0.1, 0.1)
                    key = "ivy_dark" if rnd.random() < 0.45 else "ivy"
                    if face == "front":
                        self.blob(key, r, (u + du, wall_y - r * 0.3, z + dz), scale=(1, 0.5, 0.85))
                    else:
                        self.blob(key, r, (wall_y + r * 0.3, u + du, z + dz), scale=(0.5, 1, 0.85))
                if rnd.random() < flowers:
                    fp = (u, wall_y - r * 0.75, z + 0.12) if face == "front" else (wall_y + r * 0.75, u, z + 0.12)
                    self.blob("pink", 0.08, fp)
                z += 0.32
                u = min(x1, max(x0, u + rnd.uniform(-0.3, 0.3)))

    def window_box(self, x, z, wall_y, w=1.1, flowers="pink", seed=3):
        rnd = random.Random(seed)
        self.box("pot", (w, 0.3, 0.22), (x, wall_y - 0.17, z))
        for i in range(4):
            fx = x - w / 2 + 0.15 + i * (w - 0.3) / 3
            self.blob("foliage" if i % 2 else "ivy", 0.16, (fx, wall_y - 0.2, z + 0.28), scale=(1, 0.8, 0.8))
            if rnd.random() < 0.8:
                self.blob(flowers, 0.07, (fx + 0.04, wall_y - 0.33, z + 0.36))

    def drainpipe(self, x, y, h, z0=0.0):
        self.cyl("stone_dark", 0.06, h, (x, y, z0 + h / 2), verts=6)
        self.box("stone_dark", (0.2, 0.2, 0.1), (x, y, z0 + h - 0.05))

    def chimney(self, x, y, z0, h, w=0.6, key="plaster_cream"):
        self.box(key, (w, w, h), (x, y, z0))
        self.box("stone_dark", (w + 0.14, w + 0.14, 0.1), (x, y, z0 + h))
        self.cyl("pot", 0.1, 0.3, (x, y, z0 + h + 0.25), verts=6)

    def join(self, name):
        bpy.ops.object.select_all(action="DESELECT")
        for o in self.objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = self.objs[0]
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.join()
        ob = bpy.context.active_object
        ob.name = name
        ob.data.name = name
        bpy.context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        # merge coincident verts per primitive and keep it faceted
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.shade_flat()
        return ob


# ---------------------------------------------------------------- buildings
def trattoria():
    p = Parts()
    W, D, H = 8.0, 5.5, 6.0
    fy = -D / 2
    p.box("plaster_cream", (W, D, H), (0, 0, 0))
    p.box("stone", (W + 0.1, D + 0.1, 0.4), (0, 0, 0))
    p.gable("roof", W + 0.9, D + 1.0, 1.9, H, ridge_x=True)
    p.box("roof_dark", (W + 0.9, D + 1.0, 0.15), (0, 0, H - 0.15))
    p.box("plaster_cream", (1.0, 1.0, 1.2), (2.6, 0.8, H + 0.6))  # chimney
    # upper floor
    for x in (-2.4, 2.4):
        p.window(x, 4.55, 1.0, 1.3, fy)
    p.cyl("pot", 0.8, 0.1, (0, fy - 0.05, 4.6), rot=(math.pi / 2, 0, 0), verts=14)
    p.cyl("trim_white", 0.66, 0.14, (0, fy - 0.07, 4.6), rot=(math.pi / 2, 0, 0), verts=14)
    p.boxc("door_brown", (0.1, 0.18, 0.75), (-0.17, fy - 0.12, 4.6))
    p.boxc("door_brown", (0.1, 0.18, 0.75), (0.17, fy - 0.12, 4.6))
    # ground floor
    p.box("glass", (3.6, 0.12, 2.0), (-1.3, fy - 0.03, 0.6))
    p.box("trim_white", (0.1, 0.16, 2.0), (-1.3, fy - 0.05, 0.6))
    p.door(2.5, 0.4, 1.2, 2.6, fy)
    p.awning(-0.3, 6.8, 3.45, fy, 1.5, ["awning_red", "trim_white"], stripes=8)
    # wall lamp
    p.box("iron", (0.1, 0.5, 0.1), (-W / 2 + 0.05, fy - 0.2, 3.3), rot=(0, 0, 0))
    p.box("iron", (0.5, 0.1, 0.1), (-W / 2 - 0.2, fy - 0.3, 3.3))
    p.box("lamp", (0.35, 0.35, 0.5), (-W / 2 - 0.4, fy - 0.3, 2.8))
    p.box("iron", (0.45, 0.45, 0.1), (-W / 2 - 0.4, fy - 0.3, 3.3))
    # terrace table + chairs
    ty = fy - 1.7
    p.box("wood", (0.12, 0.12, 0.75), (-1.4, ty, 0))
    p.box("trim_white", (1.3, 1.3, 0.1), (-1.4, ty, 0.75))
    for i in range(3):
        for j in range(3):
            if (i + j) % 2 == 0:
                p.box("awning_red", (0.4, 0.4, 0.12), (-1.8 + i * 0.4, ty - 0.4 + j * 0.4, 0.75))
    for s in (-1, 1):
        cx = -1.4 + s * 1.05
        p.box("wood", (0.55, 0.55, 0.45), (cx, ty, 0))
        p.box("wood", (0.12, 0.55, 0.6), (cx + s * 0.22, ty, 0.45))
    p.planter(-W / 2 + 0.5, fy - 0.6, 0.5)
    p.planter(W / 2 - 0.6, fy - 0.6, 0.5, flowers=None)
    # bougainvillea climbing the left corner
    p.vine([(-W / 2, fy, z) for z in (1.6, 2.6, 3.6, 4.6, 5.6)] + [(-W / 2 + 0.8, fy - 0.3, 6.4), (-W / 2 + 1.7, fy + 0.2, 6.9)], r=0.55)
    # detail pass
    p.roof_rows(W + 0.9, D + 1.0, 1.9, H, kind="gable_x", n=7)
    p.ivy(1.0, W / 2 + 0.1, 3.4, H + 0.2, fy, seed=11, n=30)
    p.ivy(-D / 2, D / 2 - 1.0, 0.4, 4.0, W / 2, seed=12, n=22, face="east")
    for x in (-2.4, 2.4):
        p.window_box(x, 3.65, fy, 1.2, seed=int(x * 10))
    p.drainpipe(W / 2 - 0.15, fy - 0.12, H)
    return p.join("trattoria")


def gelateria():
    p = Parts()
    W, D, H = 5.0, 4.5, 4.2
    fy = -D / 2
    p.box("plaster_peach", (W, D, H), (0, 0, 0))
    p.gable("plaster_peach", W, D, 1.6, H, ridge_x=False)
    p.gable("roof", W + 0.8, D + 0.8, 2.0, H - 0.1, ridge_x=False)
    # shop opening + counter
    p.box("glass_dark", (3.8, 0.1, 2.0), (0, fy - 0.02, 0.3))
    p.box("counter_pink", (4.2, 0.9, 1.05), (0, fy - 0.45, 0))
    p.box("trim_white", (4.3, 1.0, 0.1), (0, fy - 0.45, 1.05))
    p.box("ice", (3.6, 0.7, 0.45), (0, fy - 0.45, 1.15))
    for i, k in enumerate(["scoop", "flower_yellow", "awning_green"]):
        p.box(k, (0.8, 0.5, 0.25), (-1.1 + i * 1.1, fy - 0.45, 1.25))
    p.awning(0, 4.8, 3.05, fy, 1.3, ["awning_green", "trim_white"], stripes=7)
    # giant cone sign on the gable
    p.cone("cone", 0.55, 0.0, 1.4, (0, fy - 0.3, 4.6), rot=(math.pi, 0, 0), verts=8)
    p.blob("scoop", 0.62, (0, fy - 0.3, 5.45))
    p.blob("awning_red", 0.15, (0, fy - 0.35, 6.05))
    p.planter(W / 2 + 0.3, fy - 0.6, 0.45, flowers="flower_yellow")
    p.vine([(-W / 2 - 0.1, fy + 0.2, 4.4), (-1.5, fy - 0.1, 5.2), (-0.6, fy, 5.9), (0.7, fy, 5.9), (1.6, fy - 0.1, 5.2), (W / 2 + 0.1, fy + 0.2, 4.4)], r=0.5, flower_every=1)
    p.roof_rows(W + 0.8, D + 0.8, 2.0, H - 0.1, kind="gable_y", n=6)
    p.ivy(-D / 2 + 0.5, D / 2, 0.3, 3.6, W / 2, seed=21, n=20, face="east")
    p.drainpipe(-W / 2 + 0.12, fy - 0.1, H)
    return p.join("gelateria")


def fish_shop():
    p = Parts()
    W, D, H = 5.0, 4.5, 4.2
    fy = -D / 2
    p.box("plaster_cream", (W, D, H), (0, 0, 0))
    p.gable("plaster_cream", W, D, 1.6, H, ridge_x=False)
    p.gable("roof", W + 0.8, D + 0.8, 2.0, H - 0.1, ridge_x=False)
    p.box("foliage_dark", (0.6, 0.6, 1.5), (-1.6, 0.6, H + 0.6))  # chimney
    p.box("flower_yellow", (0.8, 0.8, 0.2), (-1.6, 0.6, H + 2.1))
    p.box("plaster_cream", (0.6, 0.6, 1.3), (1.7, 0.6, H + 0.6))
    p.box("glass_dark", (3.8, 0.1, 2.0), (0, fy - 0.02, 0.3))
    p.awning(0, 4.8, 3.05, fy, 1.3, ["awning_blue", "trim_white"], stripes=7)
    # oval fish sign
    p.cyl("trim_white", 1.0, 0.14, (0, fy - 0.1, 4.75), rot=(math.pi / 2, 0, 0), verts=14, scale=(1.0, 0.6, 1.0))
    p.cyl("awning_blue", 1.1, 0.1, (0, fy - 0.03, 4.75), rot=(math.pi / 2, 0, 0), verts=14, scale=(1.0, 0.68, 1.0))
    p.blob("fish", 0.42, (-0.1, fy - 0.22, 4.75), scale=(1.4, 0.4, 0.7))
    p.cone("fish", 0.3, 0.0, 0.5, (0.55, fy - 0.22, 4.75), rot=(0, math.pi / 2, 0), verts=4, scale=(1, 0.5, 1))
    # fish crate counter
    p.box("wood", (4.2, 1.3, 0.95), (0, fy - 0.7, 0))
    for x in (-2.0, 0, 2.0):
        p.box("door_brown", (0.15, 1.35, 0.95), (x, fy - 0.7, 0))
    p.box("ice", (3.9, 1.1, 0.12), (0, fy - 0.7, 0.95))
    for x in (-1.2, 0.0, 1.2):
        p.blob("fish", 0.3, (x, fy - 0.7, 1.15), scale=(1.6, 0.6, 0.55))
    p.planter(W / 2 + 0.3, fy - 0.6, 0.45, flowers=None)
    p.roof_rows(W + 0.8, D + 0.8, 2.0, H - 0.1, kind="gable_y", n=6)
    p.ivy(-W / 2 - 0.05, -W / 2 + 0.9, 0.3, 3.8, fy, seed=31, n=18)
    p.drainpipe(W / 2 - 0.12, fy - 0.1, H)
    return p.join("fish_shop")


def chapel():
    p = Parts()
    W, D, H = 5.5, 7.0, 5.0
    fy = -D / 2
    p.box("stone", (W, D, H), (0, 0, 0))
    p.box("plaster_cream", (W + 0.1, D + 0.1, 0.5), (0, 0, 0))
    p.gable("stone", W, D, 2.0, H, ridge_x=False)
    p.gable("roof", W + 0.8, D + 0.8, 2.4, H - 0.1, ridge_x=False)
    # bell tower over the front
    ty = fy + 0.9
    p.box("stone", (1.7, 1.7, 3.0), (0, ty, H + 1.4))
    p.box("glass_dark", (1.0, 0.1, 1.2), (0, ty - 0.86, H + 2.6))
    p.cone("gold", 0.45, 0.15, 0.7, (0, ty - 0.6, H + 3.15), verts=8)
    p.box("trim_white", (2.0, 2.0, 0.2), (0, ty, H + 4.4))
    p.cone("roof", 1.45, 0.0, 1.0, (0, ty, H + 5.1), rot=(0, 0, math.pi / 4), verts=4)
    p.box("plaster_cream", (0.18, 0.18, 1.1), (0, ty, H + 5.5))
    p.box("plaster_cream", (0.7, 0.18, 0.18), (0, ty, H + 6.1))
    # facade
    p.cyl("trim_white", 0.75, 0.12, (0, fy - 0.05, 4.0), rot=(math.pi / 2, 0, 0), verts=12)
    p.cyl("glass", 0.58, 0.16, (0, fy - 0.07, 4.0), rot=(math.pi / 2, 0, 0), verts=12)
    p.boxc("trim_white", (1.16, 0.2, 0.1), (0, fy - 0.08, 4.0))
    p.boxc("trim_white", (0.1, 0.2, 1.16), (0, fy - 0.08, 4.0))
    p.door(0, 0.5, 2.0, 3.0, fy + 0.02, "trim_white")
    p.door(0, 0.5, 1.7, 2.8, fy - 0.02, "shutter_green")
    p.box("foliage_dark", (0.08, 0.2, 2.6), (0, fy - 0.1, 0.5))
    for x in (-1.9, 1.9):
        p.arch_window(x, 2.0, 0.55, 1.3, fy)
    p.box("plaster_cream", (2.6, 1.0, 0.25), (0, fy - 0.5, 0))
    p.box("plaster_cream", (2.2, 0.6, 0.25), (0, fy - 0.3, 0.25))
    p.planter(-W / 2 + 0.2, fy - 0.8, 0.5)
    p.planter(W / 2 - 0.2, fy - 0.8, 0.5, flowers=None)
    p.vine([(W / 2, fy + 0.4, z) for z in (1.5, 2.6, 3.7, 4.8)] + [(W / 2 - 0.6, fy, 5.6)], r=0.55)
    p.roof_rows(W + 0.8, D + 0.8, 2.4, H - 0.1, kind="gable_y", n=7)
    p.ivy(-D / 2 + 1.0, D / 2, 0.4, 4.6, W / 2, seed=41, n=34, face="east")
    p.ivy(-W / 2, -W / 2 + 1.2, 0.4, 3.0, fy, seed=42, n=14)
    return p.join("chapel")


def townhouse_yellow():
    p = Parts()
    W, D, H = 4.6, 4.6, 8.6
    fy = -D / 2
    p.box("plaster_yellow", (W, D, H), (0, 0, 0))
    p.box("trim_white", (W + 0.1, D + 0.1, 0.18), (0, 0, 3.0))
    p.box("trim_white", (W + 0.1, D + 0.1, 0.18), (0, 0, 6.0))
    p.hip("roof", W + 0.8, D + 0.8, 1.4, H)
    p.box("roof_dark", (W + 0.8, D + 0.8, 0.15), (0, 0, H - 0.1))
    # ground
    p.door(-0.9, 0, 1.2, 2.5, fy, "shutter_green")
    p.window(1.2, 1.6, 0.8, 1.1, fy)
    # balcony floor
    p.door(0, 3.25, 1.1, 2.3, fy, "glass")
    for s in (-1, 1):
        p.box("shutter_green", (0.6, 0.1, 2.2), (s * 0.95, fy - 0.05, 3.25))
    p.box("trim_white", (2.6, 1.0, 0.16), (0, fy - 0.5, 3.15))
    p.railing(0, 2.5, fy - 0.95, 3.3, posts=7)
    p.planter(-1.0, fy - 0.5, 0.25, z0=3.3)
    p.planter(1.0, fy - 0.5, 0.25, z0=3.3, flowers="awning_red")
    # top floor
    for x in (-1.1, 1.1):
        p.window(x, 7.3, 0.7, 1.1, fy)
    p.planter(W / 2 - 0.2, fy - 0.6, 0.5, flowers=None)
    p.roof_rows(W + 0.8, D + 0.8, 1.4, H, kind="hip", n=5)
    p.chimney(1.2, 0.8, H + 0.4, 1.4)
    for x in (-1.1, 1.1):
        p.window_box(x, 6.45, fy, 1.0, seed=int(x * 7) + 50)
    p.ivy(-D / 2, D / 2 - 0.5, 0.3, 5.5, W / 2, seed=51, n=30, face="east")
    p.drainpipe(-W / 2 + 0.12, fy - 0.1, H)
    return p.join("townhouse_yellow")


def townhouse_white():
    p = Parts()
    W, D, H = 4.8, 4.8, 9.2
    fy = -D / 2
    p.box("plaster_white", (W, D, H), (0, 0, 0))
    p.hip("roof", W + 0.8, D + 0.8, 1.4, H)
    p.box("roof_dark", (W + 0.8, D + 0.8, 0.15), (0, 0, H - 0.1))
    p.box("plaster_white", (0.8, 0.8, 1.3), (-1.4, 0.8, H + 0.5))  # chimney
    p.door(0, 0, 1.3, 2.6, fy, "shutter_green")
    p.box("stone", (1.8, 0.6, 0.2), (0, fy - 0.3, 0))
    for zc in (4.6, 7.6):
        for x in (-1.2, 1.2):
            p.window(x, zc, 0.75, 1.2, fy)
    # flower box under the middle row
    p.box("pot", (1.4, 0.4, 0.3), (1.2, fy - 0.25, 3.6))
    p.vine([(0.8, fy - 0.3, 4.0), (1.2, fy - 0.3, 4.05), (1.6, fy - 0.3, 4.0)], r=0.22, flower_every=1, flowers="flower_yellow")
    # laundry line off the right wall
    lx0, lx1, lz = W / 2, W / 2 + 2.6, 6.6
    p.box("iron", (0.12, 0.12, lz + 0.2), (lx1, fy + 0.6, 0))
    p.boxc("iron", (lx1 - lx0, 0.04, 0.04), ((lx0 + lx1) / 2, fy + 0.6, lz))
    for i, k in enumerate(["trim_white", "pink", "cloth_blue", "trim_white"]):
        x = lx0 + 0.45 + i * 0.6
        p.box(k, (0.5, 0.05, 0.75 - (i % 2) * 0.2), (x, fy + 0.6, lz - 0.8 + (i % 2) * 0.2))
    p.planter(-W / 2 + 0.1, fy - 0.6, 0.5)
    p.vine([(-W / 2, fy, z) for z in (2.0, 3.0)], r=0.5, flowers=None)
    p.roof_rows(W + 0.8, D + 0.8, 1.4, H, kind="hip", n=5)
    p.window_box(-1.2, 6.55, fy, 1.0, seed=61)
    p.ivy(-W / 2, -W / 2 + 1.3, 0.3, 6.8, fy, seed=62, n=26)
    p.drainpipe(W / 2 - 0.12, fy - 0.1, H)
    return p.join("townhouse_white")


def townhouse_small():
    p = Parts()
    W, D, H = 4.2, 4.2, 6.0
    fy = -D / 2
    p.box("plaster_peach", (W, D, H), (0, 0, 0))
    p.box("trim_white", (W + 0.1, D + 0.1, 0.16), (0, 0, 3.0))
    p.gable("roof", W + 0.8, D + 0.9, 1.5, H, ridge_x=True)
    p.box("roof_dark", (W + 0.8, D + 0.9, 0.15), (0, 0, H - 0.1))
    p.door(0, 0, 1.2, 2.5, fy, "shutter_green")
    p.box("stone", (1.6, 0.5, 0.18), (0, fy - 0.25, 0))
    p.window(1.4, 1.7, 0.6, 0.9, fy, shutters=None)
    p.window(-1.4, 1.7, 0.6, 0.9, fy, shutters=None)
    p.window(0, 4.5, 1.1, 1.3, fy)
    # balcony with flower box
    p.box("trim_white", (2.4, 0.9, 0.15), (0, fy - 0.45, 3.2))
    p.box("pot", (2.2, 0.35, 0.4), (0, fy - 0.75, 3.35))
    p.vine([(x, fy - 0.75, 3.85) for x in (-0.8, -0.27, 0.27, 0.8)], r=0.28, flower_every=1, flowers="flower_yellow")
    p.planter(-W / 2 + 0.1, fy - 0.6, 0.45)
    p.planter(W / 2 - 0.1, fy - 0.6, 0.45, flowers="flower_yellow")
    p.roof_rows(W + 0.8, D + 0.9, 1.5, H, kind="gable_x", n=5)
    p.chimney(-1.1, 0.7, H + 0.3, 1.3, w=0.5)
    p.ivy(-D / 2, D / 2 - 0.5, 0.3, 3.0, W / 2, seed=71, n=18, face="east")
    return p.join("townhouse_small")


# ---------------------------------------------------------------- harbor
# From assets/env/harbor_sheet.webp (Big Fish Shop) and the harbor pier
# (Old Gil's stall, your boat "The Chum Storm").
def big_fish_shop():
    """The Big Fish Shop, raised to two storeys."""
    p = Parts()
    W, D, H = 9.0, 6.0, 7.2
    fy = -D / 2
    p.box("plaster_cream", (W, D, H), (0, 0, 0))
    p.box("stone", (W + 0.1, D + 0.1, 0.5), (0, 0, 0))
    p.box("wood", (W + 0.14, D + 0.14, 0.25), (0, 0, 3.65))
    for s in (-1, 1):
        p.box("wood", (0.36, 0.36, H), (s * W / 2, fy, 0))
    p.hip("roof", W + 1.2, D + 1.2, 2.4, H)
    p.box("roof_dark", (W + 1.2, D + 1.2, 0.18), (0, 0, H - 0.12))
    # ground floor: blue door, two display windows with fish counters
    p.box("stone", (2.4, 0.8, 0.25), (0, fy - 0.4, 0))
    p.door(0, 0.5, 1.95, 3.0, fy + 0.03, "wood")
    p.door(0, 0.5, 1.6, 2.8, fy - 0.02, "awning_blue")
    p.blob("gold", 0.09, (0.5, fy - 0.17, 1.8))
    for s in (-1, 1):
        x = s * 2.9
        p.cross_window(x, 2.25, 1.7, 1.15, fy)
        p.box("wood", (2.5, 1.0, 1.0), (x, fy - 0.5, 0))
        p.box("door_brown", (2.55, 1.05, 0.1), (x, fy - 0.5, 0.9))
        p.box("ice", (2.3, 0.8, 0.12), (x, fy - 0.5, 1.0))
        for k in (-0.7, 0.0, 0.7):
            p.blob("fish", 0.27, (x + k, fy - 0.5, 1.22), scale=(1.6, 0.65, 0.6))
        # lanterns beside the door
        p.box("iron", (0.1, 0.4, 0.1), (s * 1.35, fy - 0.2, 3.05))
        p.box("lamp", (0.3, 0.3, 0.42), (s * 1.35, fy - 0.42, 2.6))
        p.box("iron", (0.38, 0.38, 0.08), (s * 1.35, fy - 0.42, 3.02))
        # buoys on the wall
        p.cyl("awning_red", 0.2, 0.55, (s * (W / 2 - 0.45), fy - 0.25, 1.9), verts=8)
        p.cyl("trim_white", 0.21, 0.16, (s * (W / 2 - 0.45), fy - 0.25, 1.9), verts=8)
        # blue fish banners on poles at each corner
        bx = s * (W / 2 + 0.7)
        p.box("iron", (0.12, 0.12, 5.0), (bx, fy - 0.4, 0))
        p.box("iron", (1.1, 0.1, 0.1), (bx, fy - 0.4, 4.85))
        p.box("awning_blue", (0.85, 0.06, 1.7), (bx, fy - 0.45, 3.15))
        p.blob("trim_white", 0.25, (bx, fy - 0.5, 4.05), scale=(0.6, 0.3, 1.3))
    p.awning(0, W - 0.3, 3.6, fy, 1.6, ["awning_red", "trim_white"], stripes=10)
    # upper floor
    for x in (-2.9, 0.0, 2.9):
        p.cross_window(x, 5.35, 1.1, 1.25, fy, shutters="awning_blue")
    p.box("pot", (1.5, 0.4, 0.3), (0, fy - 0.25, 4.35))
    p.vine([(x, fy - 0.3, 4.75) for x in (-0.5, 0.0, 0.5)], r=0.24, flower_every=1, flowers="pink")
    # sign board on the roof front
    sz = H + 0.15
    p.box("wood", (7.0, 0.2, 1.6), (0, fy - 0.45, sz))
    p.box("plaster_cream", (6.6, 0.26, 1.25), (0, fy - 0.5, sz + 0.18))
    p.text("door_brown", "BIG FISH SHOP", (0, fy - 0.66, sz + 0.8), 0.78)
    for s in (-1, 1):
        p.blob("fish", 0.17, (s * 2.95, fy - 0.66, sz + 0.8), scale=(1.6, 0.4, 0.8))
    # big fish on a wave, on top of the roof
    k = 2.0  # size of the rooftop fish
    fyy = fy + 1.6
    fz = H + 1.45 - 0.3 * k  # belly rests on the roof slope

    def at(x, dy, z):
        return (x * k, fyy + dy * k, fz + z * k)

    p.blob("fish", 1.0 * k, at(0, 0, 1.2), scale=(2.1, 0.7, 0.9))
    p.blob("cloth_blue", 0.9 * k, at(-0.1, -0.12, 0.95), scale=(1.9, 0.6, 0.45))
    p.cone("fish", 0.85 * k, 0.0, 1.2 * k, at(2.55, 0, 1.45), rot=(0, -math.pi / 2, 0), verts=4, scale=(1, 0.3, 1))
    p.cone("awning_blue", 0.45 * k, 0.0, 0.7 * k, at(0.2, 0, 2.0), verts=4, scale=(1.4, 0.25, 1))
    p.blob("trim_white", 0.24 * k, at(-1.35, -0.55, 1.45))
    p.blob("iron", 0.12 * k, at(-1.4, -0.72, 1.45))
    # props out front
    p.barrel(-W / 2 - 0.1, fy - 1.0)
    p.crate(-3.4, fy - 1.75)
    p.crate(-2.45, fy - 1.75)
    p.crate(-2.9, fy - 1.75, z0=0.72, s=0.75, rz=0.3)
    p.crate(W / 2 - 0.2, fy - 1.3, s=0.8)
    # chalkboard A-frame
    for t in (-1, 1):
        p.boxc("wood", (0.8, 0.08, 1.15), (2.2, fy - 1.6 + t * 0.15, 0.55), rot=(t * 0.25, 0, 0))
    p.boxc("iron", (0.65, 0.1, 0.9), (2.2, fy - 1.76, 0.6), rot=(-0.25, 0, 0))
    p.boxc("trim_white", (0.35, 0.11, 0.05), (2.2, fy - 1.78, 0.62), rot=(-0.25, 0, 0))
    p.roof_rows(W + 1.2, D + 1.2, 2.4, H, kind="hip", n=6)
    p.chimney(2.8, 1.2, H + 0.6, 1.6, w=0.7)
    p.ivy(-D / 2, D / 2 - 0.8, 0.5, 6.5, W / 2, seed=81, n=36, face="east")
    p.drainpipe(W / 2 - 0.2, fy - 0.2, H)
    p.drainpipe(-W / 2 + 0.2, fy - 0.2, H)
    return p.join("big_fish_shop")


def gil_stall():
    """Old Gil's fish stall on the pier."""
    p = Parts()
    W, D = 4.6, 2.6
    fy = -D / 2
    z0 = 0.25
    p.box("wood", (W + 1.8, D + 1.8, z0), (0, 0.1, 0))
    for i in range(7):
        p.box("door_brown", (0.05, D + 1.8, 0.02), (-W / 2 - 0.9 + (i + 1) * (W + 1.8) / 8, 0.1, z0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box("wood", (0.18, 0.18, 3.1), (sx * (W / 2 - 0.1), sy * (D / 2 - 0.1), z0))
    p.awning(0, W + 0.5, z0 + 3.25, D / 2 + 0.25, D + 0.9, ["awning_blue", "trim_white"], stripes=7, angle=0.12)
    # back shelf + front counter with the day's catch
    p.box("wood", (W - 0.4, 0.5, 1.4), (0, D / 2 - 0.4, z0))
    p.box("ice", (W - 0.6, 0.4, 0.1), (0, D / 2 - 0.4, z0 + 1.4))
    # the front counter is its own child object, so the game can stand Gil between it and the rest
    pf = Parts()
    pf.box("wood", (W - 0.3, 0.9, 1.1), (0, fy + 0.45, z0))
    for x in (-(W - 0.3) / 2, 0.0, (W - 0.3) / 2):
        pf.box("door_brown", (0.12, 0.95, 1.1), (x, fy + 0.45, z0))
    pf.box("ice", (W - 0.5, 0.75, 0.12), (0, fy + 0.45, z0 + 1.1))
    for i, k in enumerate(["fish", "pink", "awning_red", "flower_yellow", "fish"]):
        pf.blob(k, 0.22, (-1.6 + i * 0.8, fy + 0.45, z0 + 1.32), scale=(1.5, 0.7, 0.6))
    front = pf.join("gil_stall_front")
    # crates stacked on the left
    p.crate(-W / 2 - 0.4, fy + 0.2, z0)
    p.crate(-W / 2 - 0.4, fy + 1.1, z0)
    p.crate(-W / 2 - 0.4, fy + 0.6, z0 + 0.72, s=0.75, rz=0.25)
    # hanging scale on a little gallows, right side
    gx = W / 2 + 0.45
    p.box("wood", (0.18, 0.18, 2.8), (gx, fy + 0.3, z0))
    p.box("wood", (1.0, 0.15, 0.15), (gx - 0.42, fy + 0.3, z0 + 2.65))
    p.box("iron", (0.04, 0.04, 0.45), (gx - 0.8, fy + 0.3, z0 + 2.2))
    p.cyl("iron", 0.32, 0.08, (gx - 0.8, fy + 0.34, z0 + 2.0), rot=(math.pi / 2, 0, 0), verts=12)
    p.cyl("trim_white", 0.27, 0.12, (gx - 0.8, fy + 0.3, z0 + 2.0), rot=(math.pi / 2, 0, 0), verts=12)
    p.box("iron", (0.03, 0.03, 0.35), (gx - 0.8, fy + 0.3, z0 + 1.65))
    p.cone("steel", 0.1, 0.42, 0.15, (gx - 0.8, fy + 0.3, z0 + 1.62), verts=10)
    # life ring, barrel, rope coil
    p.torus("awning_red", 0.36, 0.11, (gx + 0.12, fy + 0.3 - 0.18, z0 + 1.3), rot=(math.pi / 2, 0, 0))
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        p.boxc("trim_white", (0.16, 0.26, 0.16), (gx + 0.12 + math.cos(ang) * 0.36, fy + 0.12, z0 + 1.3 + math.sin(ang) * 0.36),
               rot=(0, -ang, 0))
    p.barrel(gx + 0.1, fy - 0.6, z0)
    p.torus("cone", 0.28, 0.09, (gx - 0.85, fy - 0.55, z0 + 0.09))
    p.torus("cone", 0.22, 0.08, (gx - 0.85, fy - 0.55, z0 + 0.25))
    # name board on the canopy
    p.box("iron", (0.06, 0.06, 0.4), (-1.1, fy - 0.15, z0 + 2.85))
    p.box("iron", (0.06, 0.06, 0.4), (1.1, fy - 0.15, z0 + 2.85))
    p.box("wood", (3.5, 0.15, 0.85), (0, fy - 0.15, z0 + 3.05))
    p.box("plaster_cream", (3.3, 0.2, 0.68), (0, fy - 0.2, z0 + 3.13))
    p.text("door_brown", "OLD GIL'S FISH", (0, fy - 0.33, z0 + 3.47), 0.4)
    ob = p.join("gil_stall")
    front.parent = ob
    return ob


def chum_storm_boat():
    """Your sailing boat, The Chum Storm. Bottom at z=0; waterline about z=0.6."""
    p = Parts()
    xs = [-3.0, -2.0, -0.5, 1.2, 2.6, 3.5]
    top_w = [1.05, 1.3, 1.4, 1.25, 0.75, 0.05]
    top_z = [1.55, 1.45, 1.4, 1.45, 1.6, 1.85]
    keel_w = [0.55, 0.65, 0.7, 0.6, 0.3, 0.03]
    keel_z = [0.35, 0.1, 0.0, 0.05, 0.35, 0.95]
    rows = [
        [(tw, tz) for tw, tz in zip(top_w, top_z)],
        [(tw - (tw - kw) * 0.18, tz - 0.28) for tw, kw, tz in zip(top_w, keel_w, top_z)],
        [(kw, kz) for kw, kz in zip(keel_w, keel_z)],
    ]
    n = len(xs)
    verts = []
    idx = {}
    for r, row in enumerate(rows):
        for i, (w, z) in enumerate(row):
            idx[(r, i, -1)] = len(verts); verts.append((xs[i], -w, z))
            idx[(r, i, 1)] = len(verts); verts.append((xs[i], w, z))
    faces, fk = [], []
    for r in range(len(rows) - 1):
        key = "trim_white" if r == 0 else "awning_red"
        for i in range(n - 1):
            a0, a1 = idx[(r, i, -1)], idx[(r, i + 1, -1)]
            b0, b1 = idx[(r + 1, i, -1)], idx[(r + 1, i + 1, -1)]
            faces.append((b0, b1, a1, a0)); fk.append(key)
            a0, a1 = idx[(r, i, 1)], idx[(r, i + 1, 1)]
            b0, b1 = idx[(r + 1, i, 1)], idx[(r + 1, i + 1, 1)]
            faces.append((a0, a1, b1, b0)); fk.append(key)
    kr = len(rows) - 1
    for i in range(n - 1):
        faces.append((idx[(kr, i, -1)], idx[(kr, i, 1)], idx[(kr, i + 1, 1)], idx[(kr, i + 1, -1)])); fk.append("awning_red")
    # transom (stern)
    faces.append(tuple(idx[(r, 0, 1)] for r in range(len(rows))) + tuple(idx[(r, 0, -1)] for r in reversed(range(len(rows)))))
    fk.append("awning_red")
    # deck, just under the gunwale
    deck = []
    for i in range(n):
        deck.append(len(verts)); verts.append((xs[i], -top_w[i] * 0.94, top_z[i] - 0.08))
    for i in reversed(range(n)):
        deck.append(len(verts)); verts.append((xs[i], top_w[i] * 0.94, top_z[i] - 0.08))
    faces.append(tuple(deck)); fk.append("wood")
    p.mesh_multi(["awning_red", "trim_white", "wood"], verts, faces, fk, "hull")
    # name on both sides of the hull
    slant = math.atan2(0.7, 1.4)
    for s in (-1, 1):
        p.text("trim_white", "THE CHUM STORM", (-0.5 * -s, s * 1.2, 0.78), 0.3,
               rot=(math.pi / 2 + slant, 0, 0 if s < 0 else math.pi), extrude=0.08)
    # mast, boom and sails
    mx = 0.4
    p.cyl("door_brown", 0.1, 6.0, (mx, 0, 1.3 + 3.0), verts=8)
    p.blob("gold", 0.16, (mx, 0, 7.35))
    p.boxc("door_brown", (2.9, 0.12, 0.12), (mx - 1.45, 0, 2.1))
    p.tri_prism("trim_white", [(mx - 0.12, 2.25), (mx - 0.12, 7.0), (mx - 2.8, 2.25)])
    p.tri_prism("trim_white", [(mx + 0.12, 2.0), (mx + 0.12, 6.4), (3.3, 2.0)])
    p.box("iron", (0.03, 0.03, 0.03), (3.3, 0, 1.85))
    p.boxc("iron", (0.03, 0.03, 5.6), ((mx + 3.45) / 2, 0, 4.6), rot=(0, math.atan2(3.45 - mx, 5.4) * -1, 0))
    for s in (-1, 1):
        p.blob("fish", 0.42, (mx - 1.0, s * 0.03, 3.6), scale=(1.4, 0.12, 0.75))
        p.cone("fish", 0.32, 0.0, 0.45, (mx - 0.25, s * 0.03, 3.6), rot=(0, -math.pi / 2, 0), verts=4, scale=(1, 0.12, 1))
    # Italian flag on a stern pole
    p.cyl("door_brown", 0.05, 1.9, (-2.75, 0, 1.5 + 0.95), verts=6)
    for k, key in enumerate(["shutter_green", "trim_white", "awning_red"]):
        p.box(key, (0.32, 0.05, 0.6), (-2.95 - 0.32 * k, 0, 2.7))
    # a bench, a crate and a bucket of fish on deck
    p.box("wood", (0.45, 2.3, 0.12), (-1.3, 0, 1.75))
    p.box("wood", (0.15, 0.15, 0.4), (-1.3, 0, 1.35))
    p.crate(1.8, 0.35, 1.37, s=0.6, rz=0.2)
    p.cone("awning_blue", 0.22, 0.28, 0.4, (1.6, -0.55, 1.57), verts=8)
    p.blob("fish", 0.14, (1.6, -0.55, 1.8), scale=(1.4, 0.7, 0.6))
    return p.join("chum_storm_boat")


# ---------------------------------------------------------------- combat-map props
# Sized from what index.html drew: 40 game units = 1 m. All stand on z=0 with the origin at the
# base centre and their front to -Y; they are rendered with the run's front-on camera (FRONT).
def fountain():
    """Cat Town's tiered fountain (drawSquareFountain)."""
    p = Parts()
    p.cyl("sq_stone", 4.45, 0.75, (0, 0, 0.375), verts=16)
    p.cyl("sq_water_deep", 3.85, 0.06, (0, 0, 0.72), verts=16)
    p.cyl("sq_water", 3.65, 0.08, (0, 0, 0.74), verts=16)
    p.cone("sq_stone", 0.85, 0.65, 1.75, (0, 0, 0.65 + 0.875), verts=8)
    p.cone("sq_stone", 1.1, 2.3, 0.45, (0, 0, 2.3 + 0.225), verts=10)
    p.cyl("sq_water", 2.05, 0.06, (0, 0, 2.74), verts=10)
    p.cone("sq_stone", 0.5, 0.4, 1.0, (0, 0, 2.75 + 0.5), verts=8)
    p.cone("sq_stone", 0.65, 1.3, 0.3, (0, 0, 3.65 + 0.15), verts=10)
    p.cyl("sq_water", 1.12, 0.05, (0, 0, 3.96), verts=10)
    p.cone("sq_stone_light", 0.25, 0.1, 0.55, (0, 0, 3.95 + 0.27), verts=6)
    return p.join("fountain")


def _bush(name, key):
    def build():
        p = Parts()
        for x, y, z, r in [(0, 0.1, 0.95, 1.2), (-0.85, 0, 0.7, 0.85), (0.9, -0.05, 0.7, 0.9),
                           (0.2, 0.55, 1.05, 0.95), (-0.3, -0.5, 0.55, 0.7), (0.45, -0.55, 0.5, 0.6)]:
            p.blob(key, r, (x, y, z), scale=(1, 1, 0.9))
        return p.join(name)
    build.__name__ = name
    return build


bush_yellow = _bush("bush_yellow", "bush_yellow")
bush_green = _bush("bush_green", "bush_green")
bush_lime = _bush("bush_lime", "bush_lime")


def mushroom():
    p = Parts()
    p.cone("mush_stem", 0.16, 0.13, 0.38, (0, 0, 0.19), verts=6)
    p.blob("mush_cap", 0.38, (0, 0, 0.42), scale=(1, 1, 0.62))
    for x, y, z in [(-0.15, -0.22, 0.56), (0.12, -0.25, 0.6), (0.24, -0.1, 0.5), (-0.02, -0.05, 0.66)]:
        p.blob("mush_dot", 0.065, (x, y, z))
    return p.join("mushroom")


def street_lamp():
    p = Parts()
    p.cone("lamp_blue", 0.28, 0.22, 0.25, (0, 0, 0.125), verts=6)
    p.cyl("lamp_blue", 0.1, 3.0, (0, 0, 1.75), verts=6)
    p.cone("lamp_glass", 0.2, 0.3, 0.6, (0, 0, 3.25 + 0.3), verts=6)
    p.cone("lamp_blue", 0.32, 0.07, 0.18, (0, 0, 3.85 + 0.09), verts=6)
    p.box("lamp_blue", (0.06, 0.06, 0.6), (0, 0, 3.25))
    return p.join("street_lamp")


def park_bench():
    p = Parts()
    for k in range(3):
        p.box("bench_wood", (2.4, 0.15, 0.07), (0, -0.05 - k * 0.18, 0.5))
    for k in range(2):
        p.box("bench_wood", (2.4, 0.07, 0.17), (0, 0.42, 0.75 + k * 0.25))
    for dx in (-1.0, 1.0):
        p.cyl("bench_leg", 0.08, 0.5, (dx, -0.2, 0.25), verts=4)
        p.cyl("bench_leg", 0.07, 1.15, (dx, 0.45, 0.575), verts=4)
    return p.join("park_bench")


def prop_crate():
    """Breakable crate (Cat Town) and the worksite's crate."""
    p = Parts()
    s = 0.75
    p.box("crate_wood", (s, s, s), (0, 0, 0))
    for z in (0.0, s - 0.09):
        p.box("crate_dark", (s + 0.03, s + 0.03, 0.09), (0, 0, z))
    for sx in (-1, 1):
        p.box("crate_dark", (0.09, s + 0.03, s), (sx * (s / 2 - 0.04), 0, 0))
    ang = math.atan2(s - 0.18, s - 0.08)
    p.boxc("crate_dark", (0.09, 0.05, math.hypot(s - 0.08, s - 0.18)), (0, -s / 2 - 0.02, s / 2), rot=(0, ang, 0))
    p.boxc("crate_dark", (0.09, 0.05, math.hypot(s - 0.08, s - 0.18)), (0, -s / 2 - 0.02, s / 2), rot=(0, -ang, 0))
    return p.join("prop_crate")


def prop_basket():
    """Breakable picnic basket (Willow Park)."""
    p = Parts()
    p.cone("basket", 0.34, 0.42, 0.42, (0, 0, 0.21), verts=10, scale=(1.25, 0.85, 1))
    for z in (0.12, 0.28):
        p.cone("basket_dark", 0.38 + z * 0.2, 0.39 + z * 0.2, 0.04, (0, 0, z), verts=10, scale=(1.25, 0.85, 1))
    p.cyl("cloth", 0.4, 0.06, (0, 0, 0.44), verts=10, scale=(1.2, 0.8, 1))
    p.torus("basket_dark", 0.32, 0.04, (0, 0, 0.44), rot=(math.pi / 2, 0, 0))
    return p.join("prop_basket")


def prop_barrel():
    """Breakable barrel (Sunny Beach)."""
    p = Parts()
    p.cone("barrel_wood", 0.3, 0.3, 0.8, (0, 0, 0.4), verts=10)
    p.cyl("barrel_wood", 0.35, 0.5, (0, 0, 0.4), verts=10)
    for z in (0.18, 0.62):
        p.cyl("barrel_band", 0.345, 0.06, (0, 0, z), verts=10)
    return p.join("prop_barrel")


def traffic_cone():
    p = Parts()
    p.box("cone_orange", (0.7, 0.7, 0.06), (0, 0, 0))
    p.cone("cone_orange", 0.28, 0.03, 0.95, (0, 0, 0.06 + 0.475), verts=8)
    p.cone("trim_white", 0.2, 0.15, 0.16, (0, 0, 0.42), verts=8)
    return p.join("traffic_cone")


def road_barrier():
    p = Parts()
    for sx in (-1, 1):
        p.box("barrier_leg", (0.1, 0.1, 0.75), (sx * 0.72, 0, 0))
        p.box("barrier_leg", (0.1, 0.5, 0.06), (sx * 0.72, 0, 0))
        p.blob("barrier_yellow", 0.1, (sx * 0.7, -0.02, 1.33))
    p.box("barrier_yellow", (1.6, 0.08, 0.4), (0, 0, 0.8))
    for k in range(5):
        p.boxc("barrier_black", (0.13, 0.1, 0.48), (-0.6 + k * 0.3, -0.01, 1.0), rot=(0, 0.6, 0))
    p.box("barrier_yellow", (1.6, 0.1, 0.06), (0, 0, 0.77))
    p.box("barrier_yellow", (1.6, 0.1, 0.06), (0, 0, 1.17))
    return p.join("road_barrier")


def tree_round():
    """A broad leafy tree: crooked trunk, foliage in chunky olive clumps with a lighter top."""
    p = Parts()
    rnd = random.Random(7)
    p.cone("trunk", 0.26, 0.16, 3.0, (0, 0, 1.5), verts=6)
    p.boxc("trunk", (0.14, 0.14, 1.4), (0.45, 0, 2.6), rot=(0, 0.7, 0))
    p.boxc("trunk", (0.12, 0.12, 1.2), (-0.4, 0.1, 2.8), rot=(0.2, -0.6, 0))
    for i in range(16):
        a = rnd.uniform(0, 2 * math.pi)
        rr = rnd.uniform(0.3, 1.5)
        z = rnd.uniform(3.0, 4.8)
        key = "tree_c" if z > 4.3 and rnd.random() < 0.7 else ("tree_a" if rnd.random() < 0.6 else "tree_b")
        p.blob(key, rnd.uniform(0.7, 1.05), (math.cos(a) * rr, math.sin(a) * rr * 0.8, z), scale=(1, 1, 0.8))
    return p.join("tree_round")


def tree_poplar():
    """A tall poplar/cypress column, like the one on the reference's left."""
    p = Parts()
    rnd = random.Random(9)
    p.cone("trunk", 0.16, 0.1, 1.4, (0, 0, 0.7), verts=6)
    for i in range(9):
        z = 1.3 + i * 0.75
        r = 0.95 * (1 - i / 11)
        for k in range(2):
            key = "tree_c" if (k == 0 and i > 4) else ("tree_a" if (i + k) % 2 else "tree_b")
            p.blob(key, r * rnd.uniform(0.85, 1.05), (rnd.uniform(-0.15, 0.15), rnd.uniform(-0.1, 0.1), z + k * 0.3), scale=(1, 1, 1.2))
    return p.join("tree_poplar")


def pampas():
    """A clump of tall pale grass with soft plumes (the reference's foreground)."""
    p = Parts()
    rnd = random.Random(5)
    for i in range(11):
        a = rnd.uniform(-0.35, 0.35)
        x = rnd.uniform(-0.45, 0.45)
        y = rnd.uniform(-0.25, 0.25)
        h = rnd.uniform(1.1, 1.7)
        p.boxc("pampas_stem", (0.03, 0.03, h), (x + math.sin(a) * h / 2, y, h / 2), rot=(0, a, 0))
        p.blob("pampas", 0.13, (x + math.sin(a) * h, y, h + 0.12), scale=(0.8, 0.8, 2.2))
    for i in range(8):
        a = i / 8 * 2 * math.pi
        p.tri_prism("ivy" if i % 2 else "foliage", [(-0.06, 0), (0.06, 0), (math.cos(a) * 0.4, 0.7)], y=math.sin(a) * 0.2, t=0.03)
    return p.join("pampas")


# ---------------------------------------------------------------- one-time items (placed / thrown in runs)
def yarn_ball():
    """The Yarn Ball item: a wound purple ball with a loose strand trailing on the ground."""
    p = Parts()
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.42, location=(0, 0, 0.42))
    p._add(bpy.context.active_object, "yarn")
    for rx, ry, rz in [(0.3, 0.2, 0), (1.2, 0.4, 0.6), (-0.5, 1.1, 1.3), (0.9, -0.7, 2.2)]:
        p.torus("yarn_light", 0.4, 0.035, (0, 0, 0.42), rot=(rx, ry, rz))
    for i in range(5):   # the loose end
        p.boxc("yarn_light", (0.26, 0.05, 0.05), (0.35 + i * 0.22, -0.1 + math.sin(i * 1.3) * 0.12, 0.03), rot=(0, 0, math.sin(i * 1.3 + 0.6) * 0.6))
    return p.join("yarn_ball")


def cucumber():
    """The Cucumber item: a bumpy green cucumber lying on the ground, ends a little paler."""
    p = Parts()
    rnd = random.Random(3)
    p.blob("cuke", 0.3, (0, 0, 0.27), scale=(2.3, 1, 0.95))
    for s in (-1, 1):
        p.blob("cuke_light", 0.2, (s * 0.6, 0, 0.27), scale=(0.7, 1.1, 1.1))
    for i in range(14):
        x = rnd.uniform(-0.55, 0.55)
        a = rnd.uniform(0.2, math.pi - 0.2)
        p.blob("cuke_dark", 0.05, (x, -math.cos(a) * 0.29, 0.27 + math.sin(a) * 0.27))
    p.cone("trunk", 0.05, 0.03, 0.12, (-0.74, 0, 0.3), rot=(0, math.pi / 2, 0), verts=5)
    return p.join("cucumber")


def party_treats():
    """Party Treats: a little dish of golden fried shrimp."""
    p = Parts()
    p.cone("trim_white", 0.36, 0.52, 0.14, (0, 0, 0.07), verts=14)
    p.cyl("plaster_cream", 0.42, 0.02, (0, 0, 0.14), verts=14)
    for i, (x, y, a) in enumerate([(-0.18, 0.05, 0.4), (0.12, 0.1, -0.5), (0.0, -0.14, 0.1)]):
        p.blob("tempura", 0.13, (x, y, 0.26), scale=(2.1, 0.9, 0.9))
        p.cone("shrimp_tail", 0.1, 0.0, 0.18, (x + math.cos(a) * 0.3, y + math.sin(a) * 0.05, 0.3), rot=(0, math.pi / 2, a), verts=4, scale=(1, 0.5, 1))
    return p.join("party_treats")


def catnip_bomb():
    """Catnip Bomb: a little cloth pouch tied with string, leaves poking out."""
    p = Parts()
    p.blob("catnip_bag", 0.32, (0, 0, 0.3), scale=(1, 1, 1.05))
    p.cone("catnip_bag", 0.18, 0.08, 0.2, (0, 0, 0.6), verts=8)
    p.torus("catnip_string", 0.14, 0.03, (0, 0, 0.56))
    for i in range(5):
        a = i * 2 * math.pi / 5
        p.blob("catnip_leaf", 0.1, (math.cos(a) * 0.1, math.sin(a) * 0.1, 0.76), scale=(1.4, 0.6, 0.5))
    p.blob("catnip_leaf", 0.08, (0.24, -0.2, 0.34), scale=(1.4, 0.5, 0.5))
    return p.join("catnip_bomb")


def cardboard_box():
    """Cardboard Box: an open box with its flaps folded out (if it fits, it sits)."""
    p = Parts()
    w, d, h = 1.4, 1.0, 0.65
    p.box("cardboard", (w, d, 0.06), (0, 0, 0))
    for s in (-1, 1):
        p.box("cardboard", (w, 0.06, h), (0, s * (d / 2 - 0.03), 0))
        p.box("cardboard_dark", (0.06, d, h), (s * (w / 2 - 0.03), 0, 0))
        p.boxc("cardboard_light", (w, 0.42, 0.05), (0, s * (d / 2 + 0.18), h + 0.06), rot=(s * -0.5, 0, 0))
        p.boxc("cardboard_light", (0.38, d, 0.05), (s * (w / 2 + 0.16), 0, h + 0.06), rot=(0, s * 0.5, 0))
    p.box("cardboard_tape", (0.18, d + 0.02, 0.02), (0, 0, h - 0.02))
    return p.join("cardboard_box")


def squirt_bottle():
    """Squirt Bottle: a blue spray bottle with a trigger nozzle."""
    p = Parts()
    p.cone("squirt_blue", 0.22, 0.2, 0.7, (0, 0, 0.35), verts=10)
    p.cyl("trim_white", 0.205, 0.18, (0, 0, 0.5), verts=10)
    p.cone("squirt_head", 0.14, 0.1, 0.18, (0, 0, 0.79), verts=8)
    p.box("squirt_head", (0.34, 0.12, 0.12), (0.12, 0, 0.84))
    p.boxc("squirt_head", (0.08, 0.1, 0.24), (0.12, 0, 0.78), rot=(0, 0.35, 0))
    p.blob("water_blue", 0.05, (0.31, 0, 0.9))
    return p.join("squirt_bottle")


def sushi_platter():
    """Sushi Platter: a wooden board with nigiri and maki."""
    p = Parts()
    p.box("wood", (1.3, 0.7, 0.08), (0, 0, 0.05))
    for s in (-1, 1):
        p.box("door_brown", (0.12, 0.7, 0.05), (s * 0.45, 0, 0))
    for i, x in enumerate((-0.38, -0.08)):
        p.blob("trim_white", 0.12, (x, -0.1, 0.2), scale=(1.5, 0.9, 0.6))
        p.blob("salmon", 0.12, (x, -0.1, 0.27), scale=(1.6, 0.95, 0.35))
    for x in (0.22, 0.45):
        p.cyl("nori", 0.11, 0.16, (x, 0.08, 0.21), verts=10)
        p.cyl("trim_white", 0.08, 0.17, (x, 0.08, 0.21), verts=10)
        p.blob("salmon", 0.04, (x, 0.08, 0.3))
    p.blob("foliage", 0.06, (0.3, -0.2, 0.15), scale=(1.4, 0.8, 0.6))
    return p.join("sushi_platter")


def caviar_plate():
    """Princess Rosalind's caviar plate (the bait for Sebastian)."""
    p = Parts()
    p.cone("steel", 0.6, 0.72, 0.08, (0, 0, 0.04), verts=16)
    p.cyl("trim_white", 0.6, 0.02, (0, 0, 0.09), verts=16)
    rnd = random.Random(4)
    for i in range(30):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 0.3) ** 0.7
        p.blob("caviar", 0.05, (math.cos(a) * r, math.sin(a) * r, 0.14))
    p.blob("lemon", 0.1, (0.38, -0.1, 0.13), scale=(1.4, 0.5, 0.6))
    p.blob("foliage", 0.07, (-0.38, 0.12, 0.13), scale=(1.4, 0.9, 0.5))
    return p.join("caviar_plate")


def grass_tuft():
    """Willow Park's grass: a flat card of blades (no line art), rendered straight on with alpha."""
    p = Parts()
    blades = [(-0.32, 0.55, -0.25, "grass_a"), (-0.18, 0.8, -0.1, "grass_b"), (-0.04, 1.0, 0.02, "grass_a"),
              (0.1, 0.85, 0.12, "grass_b"), (0.25, 0.6, 0.28, "grass_a"), (0.36, 0.42, 0.4, "grass_b"),
              (-0.42, 0.38, -0.5, "grass_b")]
    for i, (x, h, lean, key) in enumerate(blades):
        w = 0.1
        p.tri_prism(key, [(x - w, 0), (x + w, 0), (x + lean * 0.5 + x * 0.3, h)], y=-0.001 * i, t=0.002)
    return p.join("grass_tuft")


def starfish():
    p = Parts()
    p.cyl("star", 0.1, 0.05, (0, 0, 0.025), verts=5)
    for k in range(5):
        a = k * 2 * math.pi / 5 + math.pi / 2
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.08, radius2=0.01, depth=0.26,
                                        location=(math.cos(a) * 0.14, math.sin(a) * 0.14, 0.03),
                                        rotation=(0, math.pi / 2, a))
        ob = bpy.context.active_object
        ob.scale = (0.5, 1, 1)
        p._add(ob, "star")
        p.blob("star_dot", 0.02, (math.cos(a) * 0.12, math.sin(a) * 0.12, 0.06))
    return p.join("starfish")


def _shell(name, key):
    def build():
        p = Parts()
        p.cone(key, 0.26, 0.0, 0.08, (0, 0, 0.04), verts=7, scale=(1.1, 0.9, 1))
        for k in range(-2, 3):
            p.boxc("pebble_c", (0.015, 0.22, 0.02), (k * 0.06, -0.05, 0.06), rot=(0, 0, k * 0.28))
        return p.join(name)
    build.__name__ = name
    return build


shell_white = _shell("shell_white", "shell_white")
shell_pink = _shell("shell_pink", "shell_pink")


def pebbles():
    p = Parts()
    for i, (x, y, key) in enumerate([(-0.18, 0.02, "pebble_a"), (0.0, -0.06, "pebble_b"), (0.18, 0.04, "pebble_c")]):
        p.blob(key, 0.12, (x, y, 0.05), scale=(1.1, 0.8, 0.5))
    return p.join("pebbles")


# ---------------------------------------------------------------- Cat Sanctuary furniture
# The room is drawn in screen pixels, so the game fits each of these to the width it used to draw.
def scratch_post():
    p = Parts()
    p.box("post_base", (1.2, 1.0, 0.25), (0, 0, 0))
    p.cyl("rope", 0.2, 2.0, (0, 0, 1.25), verts=8)
    for z in range(9):
        p.cyl("post_base", 0.205, 0.03, (0, 0, 0.35 + z * 0.2), verts=8)
    p.box("post_base", (1.1, 0.9, 0.22), (0, 0, 2.25))
    return p.join("scratch_post")


def cat_bed():
    p = Parts()
    p.torus("bed_blue", 1.0, 0.34, (0, 0, 0.34))
    p.cyl("bed_blue", 1.05, 0.14, (0, 0, 0.07), verts=16)
    p.cyl("bed_cushion", 0.78, 0.18, (0, 0, 0.22), verts=16)
    return p.join("cat_bed")


def food_bowl():
    p = Parts()
    p.cone("bowl_blue", 0.42, 0.6, 0.3, (0, 0, 0.15), verts=14)
    p.cyl("bowl_inner", 0.48, 0.04, (0, 0, 0.29), verts=14)
    return p.join("food_bowl")


def cat_grass_pot():
    p = Parts()
    p.cone("terracotta", 0.24, 0.34, 0.45, (0, 0, 0.225), verts=8)
    p.cyl("roof_dark", 0.36, 0.06, (0, 0, 0.45), verts=8)
    for i in range(-3, 4):
        h = 0.55 + (3 - abs(i)) * 0.09
        p.tri_prism("catgrass", [(i * 0.07 - 0.04, 0.45), (i * 0.07 + 0.04, 0.45), (i * 0.13, 0.45 + h)], y=(i % 2) * 0.05, t=0.03)
    return p.join("cat_grass_pot")


def floor_cushion():
    p = Parts()
    p.blob("cushion", 1.0, (0, 0, 0.28), scale=(1.0, 0.8, 0.3))
    p.blob("cushion_top", 0.65, (0, -0.05, 0.43), scale=(1.0, 0.75, 0.18))
    return p.join("floor_cushion")


def cat_tower():
    p = Parts()
    p.box("post_base", (1.5, 1.1, 0.3), (0, 0, 0))
    p.cyl("rope", 0.18, 2.3, (0, 0, 1.45), verts=8)
    p.box("bed_blue", (1.3, 1.0, 0.22), (0, 0, 1.25))
    p.box("bed_blue", (1.1, 0.9, 0.22), (0, 0, 2.45))
    p.box("rope", (0.03, 0.03, 0.45), (0.45, -0.3, 0.8))
    p.blob("toy_red", 0.13, (0.45, -0.3, 0.75))
    return p.join("cat_tower")


def pet_fountain():
    p = Parts()
    p.cone("fountain_white", 0.42, 0.55, 0.28, (0, 0, 0.14), verts=14)
    p.cyl("water_blue", 0.45, 0.04, (0, 0, 0.28), verts=14)
    p.cone("fountain_white", 0.12, 0.08, 0.3, (0, 0, 0.4), verts=8)
    return p.join("pet_fountain")


def fireplace():
    p = Parts()
    p.box("brick", (1.76, 0.5, 1.4), (0, 0, 0))
    p.box("mantel", (2.08, 0.62, 0.2), (0, 0, 1.4))
    p.door(0, 0, 1.12, 1.12, -0.25, "soot", depth=0.06)
    p.box("stone", (1.4, 0.4, 0.08), (0, -0.4, 0))
    return p.join("fireplace")


def wall_lamp():
    p = Parts()
    p.box("brass", (0.18, 0.1, 0.5), (0, 0.1, -0.25))
    p.box("brass", (0.08, 0.35, 0.08), (0, -0.05, 0.0))
    p.blob("lamp_globe", 0.36, (0, -0.25, 0.0))
    return p.join("wall_lamp")


def fishtank():
    p = Parts()
    p.box("tank_wood", (1.6, 0.6, 0.68), (0, 0, 0))
    p.box("crate_dark", (1.65, 0.65, 0.06), (0, 0, 0.62))
    p.box("tank_water", (1.44, 0.5, 1.0), (0, 0, 0.68))
    p.box("sand", (1.42, 0.48, 0.14), (0, -0.02, 0.68))
    p.box("crate_dark", (1.5, 0.56, 0.05), (0, 0, 1.68))
    return p.join("fishtank")


def hammock():
    p = Parts()
    n = 8
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        x0, x1 = -0.92 + 1.84 * t0, -0.92 + 1.84 * t1
        z0 = -0.6 * (1 - (2 * t0 - 1) ** 2)
        z1 = -0.6 * (1 - (2 * t1 - 1) ** 2)
        ln = math.hypot(x1 - x0, z1 - z0)
        p.boxc("hammock", (ln + 0.02, 0.7, 0.06), ((x0 + x1) / 2, 0, (z0 + z1) / 2), rot=(0, -math.atan2(z1 - z0, x1 - x0), 0))
    for s in (-1, 1):
        p.boxc("hammock_rope", (0.05, 0.05, 0.75), (s * 1.08, 0, 0.32), rot=(0, s * -0.55, 0))
    return p.join("hammock")


def cat_room(part="all", fstyle="wood", wstyle="rose", name="cat_room"):
    """The Cat Sanctuary as a cosy cutaway diorama (after a pastel isometric room reference): a thick
    floor slab with wood planks, two back walls (north + west) seen from the south-east corner, a big
    window, posters, shelves, wall steps for climbing, plants and a patchwork rug. Game room space maps
    1:1 at 40 units/m: game (x, y) = Blender (X, -Y); the floor spans X 0..RW, Y 0..-RD; origin = the
    north-west corner. Furniture you buy is drawn separately, so cats can walk in front of / behind it."""
    p = Parts()
    RW, RD, WH, T = 16.0, 12.0, 4.6, 0.35
    F, Wl = part in ("all", "floor"), part in ("all", "walls")
    wk = lambda k: k + "_" + wstyle      # wall-style colour keys (room_wall_n_rose, ...)
    rnd = random.Random(12)
    # floor slab and its surface: wood planks, checker tiles or stone flags
    if F:
        p.box("room_base", (RW + T, RD + T, 0.9), (RW / 2 - T / 2, -RD / 2 + T / 2, -0.9))
        if fstyle == "wood":
            p.box("room_floor", (RW, RD, 0.06), (RW / 2, -RD / 2, -0.06))
            for i in range(1, 16):
                y = -i * RD / 16
                p.box("room_floor_dark", (RW, 0.04, 0.02), (RW / 2, y, -0.01))
                for k in range(3):
                    x = (i * 2.9 + k * 4.1) % RW
                    p.box("room_floor_dark", (0.04, RD / 16, 0.02), (x, y + RD / 32, -0.01))
        elif fstyle == "tiles":
            n = 16
            for i in range(n):
                for j in range(12):
                    p.box("floor_tile_a" if (i + j) % 2 else "floor_tile_b", (RW / n, RD / 12, 0.06), ((i + 0.5) * RW / n, -(j + 0.5) * RD / 12, -0.06))
        else:   # stone flags (like the reference's cool blue-grey stone)
            p.box("floor_grout", (RW, RD, 0.05), (RW / 2, -RD / 2, -0.06))
            frnd = random.Random(31)
            y = 0.0
            while y < RD - 0.05:
                h = min(frnd.uniform(0.9, 1.5), RD - y)
                x = 0.0
                while x < RW - 0.05:
                    w = min(frnd.uniform(1.0, 1.9), RW - x)
                    p.box(frnd.choice(["floor_stone_a", "floor_stone_b", "floor_stone_c"]), (w - 0.09, h - 0.09, 0.07), (x + w / 2, -(y + h / 2), -0.06))
                    x += w
                y += h
    if Wl:
        # walls (north at Y=0, west at X=0), with wainscot, skirting and a top cap (the cutaway edge)
        p.box(wk("room_wall_n"), (RW + T, T, WH), (RW / 2 - T / 2, T / 2, 0))
        p.box(wk("room_wall_w"), (T, RD, WH), (-T / 2, -RD / 2, 0))
        p.box(wk("room_wainscot"), (RW, 0.06, 1.2), (RW / 2, 0.0, 0))
        p.box(wk("room_wainscot"), (0.06, RD, 1.2), (0.0, -RD / 2, 0))
        p.box("room_skirt", (RW, 0.1, 0.18), (RW / 2, -0.03, 0))
        p.box("room_skirt", (0.1, RD, 0.18), (0.03, -RD / 2, 0))
        p.box("room_trim", (RW, 0.12, 0.08), (RW / 2, -0.03, 1.2))
        p.box("room_trim", (0.12, RD, 0.08), (0.03, -RD / 2, 1.2))
        p.box(wk("room_cap"), (RW + T, T + 0.06, 0.12), (RW / 2 - T / 2, T / 2, WH))
        p.box(wk("room_cap"), (T + 0.06, RD, 0.12), (-T / 2, -RD / 2, WH))
        # the big window on the north wall: sky, frame, sill, curtains
        wx, wz, ww, wh = 8.0, 2.6, 3.2, 2.0
        p.boxc("trim_white", (ww + 0.3, 0.14, wh + 0.3), (wx, -0.02, wz))
        p.boxc("room_sky", (ww, 0.16, wh), (wx, -0.03, wz))
        p.boxc("room_cloud", (0.9, 0.18, 0.25), (wx - 0.6, -0.04, wz + 0.45))
        p.boxc("room_cloud", (0.5, 0.18, 0.18), (wx + 0.7, -0.04, wz + 0.1))
        p.boxc("trim_white", (0.08, 0.2, wh), (wx, -0.05, wz))
        p.boxc("trim_white", (ww, 0.2, 0.08), (wx, -0.05, wz))
        p.box("trim_white", (ww + 0.6, 0.45, 0.1), (wx, -0.2, wz - wh / 2 - 0.15))
        for s in (-1, 1):
            p.box("room_curtain", (0.55, 0.12, wh + 0.5), (wx + s * (ww / 2 + 0.25), -0.12, wz - wh / 2 - 0.35))
        p.boxc("door_brown", (ww + 1.6, 0.1, 0.08), (wx, -0.12, wz + wh / 2 + 0.3))
        # posters on the north wall: a fish and a cat
        for x, key, art in ((3.2, "room_poster_a", "fish"), (12.6, "room_poster_b", "cat")):
            p.boxc("wood", (1.3, 0.08, 1.6), (x, -0.04, 3.0))
            p.boxc(key, (1.1, 0.1, 1.4), (x, -0.05, 3.0))
            if art == "fish":
                p.blob("awning_blue", 0.28, (x - 0.05, -0.12, 3.0), scale=(1.6, 0.25, 0.8))
                p.cone("awning_blue", 0.22, 0.0, 0.3, (x + 0.42, -0.12, 3.0), rot=(0, -math.pi / 2, 0), verts=4, scale=(1, 0.25, 1))
            else:
                p.blob("plaster_yellow", 0.32, (x, -0.12, 2.9), scale=(1, 0.25, 0.9))
                for s in (-1, 1):
                    p.cone("plaster_yellow", 0.14, 0.0, 0.3, (x + s * 0.2, -0.12, 3.25), verts=4, scale=(1, 0.3, 1))
        # a wall shelf with books and a plant (north wall), and climbing steps for cats (west wall)
        p.box("wood", (2.0, 0.45, 0.1), (12.6, -0.25, 1.7))
        for i in range(6):
            p.box(rnd.choice(["awning_red", "awning_blue", "plaster_yellow", "awning_green", "trim_white"]), (0.16, 0.32, rnd.uniform(0.35, 0.5)), (11.85 + i * 0.2, -0.22, 1.8))
        p.cone("pot", 0.14, 0.18, 0.25, (13.3, -0.25, 1.92), verts=8)
        p.blob("foliage", 0.22, (13.3, -0.25, 2.2), scale=(1, 1, 0.9))
        for i, (y, z) in enumerate([(-9.0, 1.0), (-7.6, 1.8), (-6.0, 2.6), (-4.4, 3.4)]):
            p.box("wood", (0.75, 1.1, 0.12), (0.4, y, z))
            p.box("room_cushion", (0.65, 0.9, 0.08), (0.4, y, z + 0.12))
        # a door in the west wall, a framed photo, a little wall lamp glow spot
        p.box("door_brown", (0.1, 1.6, 3.0), (0.05, -10.8 + 0.8, 0))
        p.boxc("gold", (0.14, 0.12, 0.12), (0.12, -10.4, 1.5))
        # corner plants
        for x, y, h in ((0.8, -0.7, 1.0), (15.2, -0.8, 0.8)):
            p.cone("pot", 0.3, 0.42, 0.6, (x, y, 0.3), verts=8)
            for k in range(5):
                a = k * 2 * math.pi / 5
                p.blob("foliage" if k % 2 else "ivy", 0.42, (x + math.cos(a) * 0.25, y + math.sin(a) * 0.25, 0.75 + h * 0.5 + (k % 2) * 0.25), scale=(1, 1, 1.2))
    # a patchwork rug in the middle of the floor
    if F:
        cols = ["rug_a", "rug_b", "rug_c", "rug_d"]
        for i in range(3):
            for j in range(2):
                p.box(cols[(i + j * 2) % 4], (1.4, 1.3, 0.04), (6.6 + i * 1.4, -5.4 - j * 1.3, 0))
        p.box("trim_white", (4.4, 2.8, 0.02), (8.0, -6.05, 0))
    return p.join(name)


# the room in layers, so the floor and the walls can be restyled separately in the game's decorate mode
ROOM_FLOORS = ("wood", "tiles", "stone")
ROOM_WALLS = ("rose", "mint", "cream")


def _room_layer(part, style):
    def build():
        return cat_room(part, fstyle=style, wstyle=style, name="room_%s_%s" % ("floor" if part == "floor" else "walls", style))
    build.__name__ = "room_%s_%s" % ("floor" if part == "floor" else "walls", style)
    return build


ROOM_LAYERS = [_room_layer("floor", s) for s in ROOM_FLOORS] + [_room_layer("walls", s) for s in ROOM_WALLS]


GROUPS = [
    ("town", [trattoria, gelateria, fish_shop, chapel, townhouse_yellow, townhouse_white, townhouse_small]),
    ("harbor", [big_fish_shop, gil_stall, chum_storm_boat]),
    ("combat", [fountain, bush_yellow, bush_green, bush_lime, mushroom, street_lamp, park_bench,
                prop_crate, prop_basket, prop_barrel, traffic_cone, road_barrier, grass_tuft,
                tree_round, tree_poplar, pampas, yarn_ball, cucumber, party_treats, caviar_plate,
                catnip_bomb, cardboard_box, squirt_bottle, sushi_platter,
                starfish, shell_white, shell_pink, pebbles]),
    ("sanctuary", [scratch_post, cat_bed, food_bowl, cat_grass_pot, floor_cushion, cat_tower, pet_fountain,
                   fireplace, wall_lamp, fishtank, hammock]),
    ("room", ROOM_LAYERS),
]
# groups seen by the run / Cat Sanctuary camera (straight from the south) instead of the harbor's corner-on one
FRONT_GROUPS = {"combat", "sanctuary"}


# ---------------------------------------------------------------- scene
def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for b in list(c):
            c.remove(b)


def fam(ob):
    """An asset and its child pieces (e.g. Gil's front counter)."""
    return [ob] + list(ob.children)


def export_glb(ob):
    bpy.ops.object.select_all(action="DESELECT")
    for o in fam(ob):
        o.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_GLB, ob.name + ".glb"),
                              export_format="GLB", use_selection=True, export_apply=True)


def setup_render(scene):
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.view_settings.view_transform = "Standard"
    sh = scene.display.shading
    sh.color_type = "MATERIAL"
    sh.show_cavity = False
    sh.show_object_outline = False
    sh.object_outline_color = (0.08, 0.06, 0.05)
    scene.render.film_transparent = False
    world = bpy.data.worlds.new("bg") if not scene.world else scene.world
    scene.world = world
    world.color = (srgb_to_linear(0.93), srgb_to_linear(0.95), srgb_to_linear(0.97))
    scene.display.render_aa = "16"


def camera_for(scene, target, extent, res):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = extent
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    rot = Euler((math.radians(62), 0, math.radians(-32)))
    cam.rotation_euler = rot
    view = rot.to_matrix() @ Vector((0, 0, -1))
    cam.location = Vector(target) - view * 60
    cam_data.clip_end = 200
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res
    return cam


# ---------------------------------------------------------------- game sprites
# The harbor in index.html is drawn on a 2D canvas with an isometric camera (ISO in index.html):
# seen from the south-east corner, ground foreshortened by ISO.FY, heights unscaled. An orthographic
# camera at 45 deg azimuth and elevation atan(ISO.FY) gives the same picture once the game stretches
# the sprite vertically by 1/cos(elevation). Keep ISO_FY equal to ISO.FY in index.html.
ISO_FY = 0.56
ISO_ELEV = math.atan(ISO_FY)
SPRITE_PPM = 80  # sprite pixels per metre (the game draws 40 world units per metre, x0.8 zoom)
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT_SPRITES = os.path.join(REPO, "assets", "env", "blockouts")
# quick look: BLK_ONLY=trattoria,fountain BLK_OUT=<folder> renders just those sprites there (nothing else is written)
ONLY = set(filter(None, os.environ.get("BLK_ONLY", "").split(",")))
# add BLK_MERGE=1 to render those straight into the game's sprites and update just their manifest entries
MERGE = bool(ONLY and os.environ.get("BLK_MERGE"))
if ONLY and not MERGE:
    OUT_SPRITES = os.environ.get("BLK_OUT") or os.path.join(HERE, "_test")
# footprint (body width x depth, metres) of the buildings; their sprites anchor at the front-centre
FOOTPRINT = {
    "trattoria": (8.0, 5.5), "gelateria": (5.0, 4.5), "fish_shop": (5.0, 4.5), "chapel": (5.5, 7.0),
    "townhouse_yellow": (4.6, 4.6), "townhouse_white": (4.8, 4.8), "townhouse_small": (4.2, 4.2),
    "big_fish_shop": (9.0, 6.0),
}
# others anchor at the origin: (anchor point in metres, turn about Z in degrees)
SPRITE_EXTRA = {
    "gil_stall": ((0, 0, 0), 0),
    "chum_storm_boat": ((0, 0, 0.6), -90),  # waterline; moored lengthwise along the pier, bow to the south
}


# Sunny lakeside light (the reference style): a warm, low-ish sun from the south-west and a deep blue
# sky fill, so lit faces go cream/warm and shadows go cool blue. Colours stay flat per face (no
# textures); the light does the work. Values are tuned so a lit wall reads ~1.05x its base colour.
SUN_DIR = Vector((0.32, 0.55, -0.78)).normalized()     # the direction the light travels
SUN_COLOR, SUN_STRENGTH = (1.0, 0.82, 0.18), 1.12
SKY_COLOR, SKY_STRENGTH = (0.5, 0.58, 0.95), 0.85
SHADOW_TINT = (0.16, 0.2, 0.42)                       # colour of cast shadows on the ground
NO_GROUND_SHADOW = {"chum_storm_boat", "grass_tuft", "wall_lamp", "hammock", "fireplace", "fishtank", "cat_room",
                    "room_floor_wood", "room_floor_tiles", "room_floor_stone", "room_walls_rose", "room_walls_mint", "room_walls_cream",
                    "starfish", "shell_white", "shell_pink", "pebbles"}


SHADOW_COOL = (0.30, 0.28, 0.58)   # what shade leans toward (a cool violet-blue)


def _lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def lit_materials():
    """Painterly two-tone light: how lit a face is (sun vs shade, incl. cast shadows, from Shader to RGB)
    blends between a warm lit colour (base x sunlight) and a rich cool shade (base darkened, nudged
    toward violet, a little more saturated), so shadows stay colourful instead of going muddy."""
    lit = Vector(SUN_COLOR) * SUN_STRENGTH * 0.55 + Vector(SKY_COLOR) * SKY_STRENGTH   # a wall facing the sun
    amb = Vector(SKY_COLOR) * SKY_STRENGTH
    for m in bpy.data.materials:
        if not m.name.startswith("town_"):
            continue
        base = Vector(m.diffuse_color[:3])
        lit_col = Vector((base.x * 1.06, base.y * 1.0, base.z * 0.9))
        shade = base * 0.6
        shade_col = shade.lerp(Vector(SHADOW_COOL), 0.28)
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        diff = nt.nodes.new("ShaderNodeBsdfDiffuse")
        diff.inputs["Color"].default_value = (1, 1, 1, 1)
        s2r = nt.nodes.new("ShaderNodeShaderToRGB")
        bw = nt.nodes.new("ShaderNodeRGBToBW")
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.clamp = True
        mr.inputs["From Min"].default_value = _lum(amb)
        mr.inputs["From Max"].default_value = _lum(lit)
        hsv = nt.nodes.new("ShaderNodeHueSaturation")
        hsv.inputs["Saturation"].default_value = 1.18
        hsv.inputs["Color"].default_value = (*shade_col, 1)
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
        mix.inputs[7].default_value = (*lit_col, 1)
        # brighter than a sun-facing wall (roofs, tops): let it go a touch past the lit colour
        over = nt.nodes.new("ShaderNodeMath"); over.operation = "DIVIDE"
        over.inputs[1].default_value = _lum(lit)
        boost = nt.nodes.new("ShaderNodeMix"); boost.data_type = "RGBA"; boost.blend_type = "MULTIPLY"
        boost.inputs["Factor"].default_value = 1.0
        clampv = nt.nodes.new("ShaderNodeMath"); clampv.operation = "MAXIMUM"; clampv.inputs[1].default_value = 1.0
        clamp2 = nt.nodes.new("ShaderNodeMath"); clamp2.operation = "MINIMUM"; clamp2.inputs[1].default_value = 1.12
        comb = nt.nodes.new("ShaderNodeCombineColor")
        emit = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(diff.outputs[0], s2r.inputs[0])
        nt.links.new(s2r.outputs["Color"], bw.inputs[0])
        nt.links.new(bw.outputs[0], mr.inputs["Value"])
        nt.links.new(mr.outputs[0], mix.inputs["Factor"])
        nt.links.new(hsv.outputs[0], mix.inputs[6])
        nt.links.new(bw.outputs[0], over.inputs[0])
        nt.links.new(over.outputs[0], clampv.inputs[0])
        nt.links.new(clampv.outputs[0], clamp2.inputs[0])
        for k in range(3):
            nt.links.new(clamp2.outputs[0], comb.inputs[k])
        nt.links.new(mix.outputs[2], boost.inputs[6])
        nt.links.new(comb.outputs[0], boost.inputs[7])
        nt.links.new(boost.outputs[2], emit.inputs["Color"])
        nt.links.new(emit.outputs[0], out.inputs["Surface"])


def setup_lights(scene):
    sun_data = bpy.data.lights.new("sun", "SUN")
    sun_data.color = SUN_COLOR
    sun_data.energy = SUN_STRENGTH * math.pi   # (a sun of strength pi lights a white diffuse face to 1.0)
    sun_data.angle = math.radians(2.5)
    try:
        sun_data.use_shadow = True
    except AttributeError:
        pass
    sun = bpy.data.objects.new("sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (-SUN_DIR).to_track_quat("Z", "Y").to_euler()
    world = scene.world or bpy.data.worlds.new("sky")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (*SKY_COLOR, 1)
    bg.inputs["Strength"].default_value = SKY_STRENGTH


def shadow_catcher():
    """A big transparent ground at z=0 that only shows the cast shadows, in a cool blue."""
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0.002))
    g = bpy.context.active_object
    g.name = "shadow_catcher"
    m = bpy.data.materials.new("shadow_catcher")
    m.use_nodes = True
    try:
        m.surface_render_method = "DITHERED"   # (Shader to RGB needs the deferred path)
    except AttributeError:
        m.blend_method = "HASHED"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    diff = nt.nodes.new("ShaderNodeBsdfDiffuse")
    diff.inputs["Color"].default_value = (1, 1, 1, 1)
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    if os.environ.get("BLK_DEBUG_CATCHER"):      # show the raw light on the ground instead
        em0 = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(diff.outputs[0], s2r.inputs[0]); nt.links.new(s2r.outputs[0], em0.inputs[0]); nt.links.new(em0.outputs[0], out.inputs[0])
        g.data.materials.append(m)
        return g
    lit = Vector(SUN_COLOR) * SUN_STRENGTH * -SUN_DIR.z + Vector(SKY_COLOR) * SKY_STRENGTH
    amb = Vector(SKY_COLOR) * SKY_STRENGTH
    lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = lum(amb)
    mr.inputs["From Max"].default_value = lum(lit) * 0.97
    mr.inputs["To Min"].default_value = 0.42
    mr.inputs["To Max"].default_value = 0.0
    tr = nt.nodes.new("ShaderNodeHoldout")   # (cuts to alpha 0 cleanly; Transparent BSDF left ~45% alpha)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*SHADOW_TINT, 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(diff.outputs[0], s2r.inputs[0])
    nt.links.new(s2r.outputs["Color"], bw.inputs[0])
    nt.links.new(bw.outputs[0], mr.inputs["Value"])
    nt.links.new(mr.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    if os.environ.get("BLK_DEBUG_MASK"):
        em1 = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(mr.outputs[0], em1.inputs[0]); nt.links.new(em1.outputs[0], out.inputs[0])
    g.data.materials.append(m)
    return g


def toon_materials():
    """(Old look) Flat colour, lit per face: walls facing south brightest, east walls in shade."""
    light = Vector((0.3, -0.8, 0.9)).normalized()
    for m in bpy.data.materials:
        if not m.name.startswith("town_"):
            continue
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        emit = nt.nodes.new("ShaderNodeEmission")
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        dot = nt.nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
        dot.inputs[1].default_value = light
        fac = nt.nodes.new("ShaderNodeMath"); fac.operation = "MULTIPLY_ADD"; fac.use_clamp = True
        fac.inputs[1].default_value = 0.42
        fac.inputs[2].default_value = 0.66
        col = nt.nodes.new("ShaderNodeVectorMath"); col.operation = "SCALE"
        col.inputs[0].default_value = m.diffuse_color[:3]
        nt.links.new(geo.outputs["Normal"], dot.inputs[0])
        nt.links.new(dot.outputs["Value"], fac.inputs[0])
        nt.links.new(fac.outputs["Value"], col.inputs["Scale"])
        nt.links.new(col.outputs["Vector"], emit.inputs["Color"])
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])


def setup_sprite_render(scene):
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.render.engine = eng
            break
        except TypeError:
            pass
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    try:
        scene.eevee.taa_render_samples = 48
    except AttributeError:
        pass
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.use_freestyle = False  # no outlines on the 3D assets


# The runs and the Cat Sanctuary look straight from the south; their upright things squash round
# shapes on the ground by MESH_FLAT (index.html), so that camera's elevation is atan(MESH_FLAT).
MESH_FLAT = 0.55
FRONT_ELEV = math.atan(MESH_FLAT)
FLAT_CARDS = {"grass_tuft"}   # flat alpha cards, rendered straight on (no tilt, no stretch)
ALSO_FRONT = {"trattoria", "fish_shop", "gelateria"}   # also rendered from the front as <name>_front
# run props that also stand on the harbor island: also rendered from the harbor's corner camera as <name>_iso
ALSO_ISO = {"street_lamp", "bush_yellow", "bush_green", "bush_lime", "mushroom", "tree_round", "tree_poplar", "pampas",
            # the Cat Sanctuary's furniture, for the 3/4 room
            "scratch_post", "cat_bed", "food_bowl", "cat_grass_pot", "floor_cushion", "cat_tower", "pet_fountain",
            "fireplace", "wall_lamp", "fishtank", "hammock"}


def render_sprite(scene, objs_on, frame_objs, anchor, path, elev=ISO_ELEV, azim=45, catcher=None):
    """Renders objs_on with an ortho camera at (elev, azim), framed on frame_objs (plus their cast
    shadow on the ground when a shadow catcher is given). Returns size + anchor pixel."""
    on = set(objs_on) | ({catcher} if catcher else set())
    for o in scene.objects:
        if o.type in ("MESH", "CURVE", "FONT"):
            o.hide_render = o not in on
    R = Euler((math.pi / 2 - elev, 0, math.radians(azim))).to_matrix()
    right, up, fwd = R @ Vector((1, 0, 0)), R @ Vector((0, 1, 0)), R @ Vector((0, 0, -1))
    us, vs = [], []
    bpy.context.view_layer.update()
    for o in frame_objs:
        for c in o.bound_box:
            p = o.matrix_world @ Vector(c)
            us.append(p.dot(right)); vs.append(p.dot(up))
            if catcher and p.z > 0:   # where this corner's shadow lands
                s = p + SUN_DIR * (p.z / -SUN_DIR.z)
                s.z = 0
                us.append(s.dot(right)); vs.append(s.dot(up))
    m = 0.15
    u0, u1, v0, v1 = min(us) - m, max(us) + m, min(vs) - m, max(vs) + m
    eu, ev = u1 - u0, v1 - v0
    cam_data = bpy.data.cameras.new("spritecam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(eu, ev)
    cam_data.clip_end = 400
    cam = bpy.data.objects.new("spritecam", cam_data)
    scene.collection.objects.link(cam)
    cam.rotation_euler = R.to_euler()
    cam.location = right * ((u0 + u1) / 2) + up * ((v0 + v1) / 2) - fwd * 150
    scene.camera = cam
    w, h = round(eu * SPRITE_PPM), round(ev * SPRITE_PPM)
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = 100
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    a = Vector(anchor)
    return {"w": w, "h": h, "ax": round((a.dot(right) - u0) * SPRITE_PPM, 1), "ay": round((v1 - a.dot(up)) * SPRITE_PPM, 1)}


def render_sprites(scene, built, front=()):
    os.makedirs(OUT_SPRITES, exist_ok=True)
    setup_sprite_render(scene)
    lit_materials()
    setup_lights(scene)
    catcher = shadow_catcher()
    manifest = {}
    for ob in built:
        saved = (ob.location.copy(), ob.rotation_euler.copy())
        ob.location = (0, 0, 0)
        if ob.name in FOOTPRINT:
            W, D = FOOTPRINT[ob.name]
            anchor, turn = (0, -D / 2, 0), 0
        else:
            anchor, turn = SPRITE_EXTRA.get(ob.name, ((0, 0, 0), 0))
            W = D = None
        view = "front" if ob in front else "iso"
        elev = 0.0 if ob.name in FLAT_CARDS else FRONT_ELEV if view == "front" else ISO_ELEV
        azim = 0 if view == "front" else 45
        ob.rotation_euler = (0, 0, math.radians(turn))
        bpy.context.view_layer.update()
        anchor_w = ob.matrix_world @ Vector(anchor)
        layers = [(ob.name, fam(ob))]
        if ob.children:  # back layer without the child pieces, then each child alone
            layers = [(ob.name, [ob])] + [(c.name, [c]) for c in ob.children]
        for name, objs in layers:
            shadow = catcher if (name == ob.name and ob.name not in NO_GROUND_SHADOW) else None
            info = render_sprite(scene, objs, fam(ob), anchor_w, os.path.join(OUT_SPRITES, name + ".png"), elev, azim, shadow)
            info.update(file=name + ".png", ppm=SPRITE_PPM, cos=round(math.cos(elev), 5), view=view,
                        top=round(ob.dimensions.z, 2), mw=round(ob.dimensions.x, 3))
            if W:
                info.update(W=W, D=D)
            manifest[name] = info
        ob.location, ob.rotation_euler = saved
    # buildings that also stand in Cat Town's story square, seen from the run camera
    for ob in built:
        if ob.name not in ALSO_FRONT:
            continue
        saved = ob.location.copy()
        ob.location = (0, 0, 0)
        bpy.context.view_layer.update()
        W, D = FOOTPRINT[ob.name]
        name = ob.name + "_front"
        info = render_sprite(scene, fam(ob), fam(ob), Vector((0, -D / 2, 0)), os.path.join(OUT_SPRITES, name + ".png"), FRONT_ELEV, 0, catcher)
        info.update(file=name + ".png", ppm=SPRITE_PPM, cos=round(math.cos(FRONT_ELEV), 5), view="front",
                    top=round(ob.dimensions.z, 2), mw=round(ob.dimensions.x, 3), W=W, D=D)
        manifest[name] = info
        ob.location = saved
    for ob in built:
        if ob.name not in ALSO_ISO:
            continue
        saved = ob.location.copy()
        ob.location = (0, 0, 0)
        bpy.context.view_layer.update()
        name = ob.name + "_iso"
        info = render_sprite(scene, fam(ob), fam(ob), Vector((0, 0, 0)), os.path.join(OUT_SPRITES, name + ".png"), ISO_ELEV, 45, catcher)
        info.update(file=name + ".png", ppm=SPRITE_PPM, cos=round(math.cos(ISO_ELEV), 5), view="iso",
                    top=round(ob.dimensions.z, 2), mw=round(ob.dimensions.x, 3))
        manifest[name] = info
        ob.location = saved
    if MERGE:   # keep every other sprite's entry
        try:
            old = open(os.path.join(OUT_SPRITES, "blockouts.js"), encoding="utf-8").read()
            old = json.loads(old.split("window.BLOCKOUT_SPRITES = ", 1)[1].rsplit(";", 1)[0])
            old.update(manifest)
            manifest = old
        except (OSError, IndexError, ValueError):
            pass
    js = ("// Generated by art/blockouts/italian_town/build_town_houses.py: do not edit by hand.\n"
          "// Isometric sprites of the low-poly block-outs; w/h/ax/ay in pixels, ppm = pixels per metre,\n"
          "// cos = cos(camera elevation) (stretch the sprite by 1/cos vertically), top/W/D in metres.\n"
          "window.BLOCKOUT_VERSION = '%d';\n" % int(__import__("time").time()) +
          "window.BLOCKOUT_SPRITES = " + json.dumps(manifest, indent=1) + ";\n")
    with open(os.path.join(OUT_SPRITES, "blockouts.js"), "w", encoding="utf-8") as f:
        f.write(js)
    for o in scene.objects:
        o.hide_render = False


def render(scene, path, light):
    scene.display.shading.light = light
    if light == "STUDIO":
        scene.display.shading.show_shadows = True
        scene.display.shadow_focus = 0.2
    else:
        scene.display.shading.show_shadows = False
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    reset()
    scene = bpy.context.scene
    setup_render(scene)
    built, rows = [], []
    if ONLY:
        front = set()
        for group, fns in GROUPS:
            for fn in fns:
                if fn.__name__ in ONLY:
                    ob = fn()
                    built.append(ob)
                    if group in FRONT_GROUPS:
                        front.add(ob)
        render_sprites(scene, built, front=front)
        print("TEST SPRITES ->", OUT_SPRITES)
        return
    for gi, (group, fns) in enumerate(GROUPS):
        row = []
        for fn in fns:
            ob = fn()
            export_glb(ob)
            row.append(ob)
        # lay out left-to-right like the concept sheet; one row per group
        x, gap = 0.0, 3.0
        for ob in row:
            w = ob.dimensions.x
            ob.location.x = x + w / 2
            ob.location.y = -gi * 25.0
            x += w + gap
        total = x - gap
        for ob in row:
            ob.location.x -= total / 2
        rows.append((group, row, total, -gi * 25.0))
        built += row

    # per-asset previews
    def show_only(keep):
        for o in built:
            for part in fam(o):
                part.hide_render = o not in keep

    for ob in built:
        show_only([ob])
        dims = ob.dimensions
        c = ob.location + Vector((0, 0, dims.z / 2))
        cam = camera_for(scene, c, max(dims.x, dims.z) * 1.45 + 2, (1000, 1000))
        render(scene, os.path.join(OUT_PNG, ob.name + ".png"), "FLAT")
        bpy.data.objects.remove(cam)

    for group, row, total, gy in rows:
        show_only(row)
        cam = camera_for(scene, (0, gy - 1, 2.0), max(total * 1.05, 36), (2400, 1100))
        render(scene, os.path.join(OUT_PNG, "lineup_%s_flat.png" % group), "FLAT")
        render(scene, os.path.join(OUT_PNG, "lineup_%s_studio.png" % group), "STUDIO")
        bpy.data.objects.remove(cam)
    show_only(built)
    camera_for(scene, (0, -13, 3), 90, (2400, 1100))

    for ob in built:
        tris = sum(len(pl.vertices) - 2 for part in fam(ob) for pl in part.data.polygons)
        print("BUILT %-18s tris=%5d  size=%.1f x %.1f x %.1f m" % (ob.name, tris, *ob.dimensions))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "italian_town_houses.blend"))

    # game sprites last: they swap the materials to flat toon shading (the .blend is already saved)
    render_sprites(scene, built, front={o for g, row, _, _ in rows if g in FRONT_GROUPS for o in row})
    print("SPRITES ->", OUT_SPRITES)


main()
