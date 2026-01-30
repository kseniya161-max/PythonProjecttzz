import ezdxf

L = 60
L2 = 20
D1 = 24
D2 = 36
d = 12
C = 2

OUT_PATH = "output/model.dxf"

TEXT_H = 2.5
OFF_1 = 7.5
OFF_6 = 7.5
AXIS_OVER = 7.0

doc = ezdxf.new("R2010")
doc.header["$INSUNITS"] = 4
msp = doc.modelspace()

for name in ["CONTUR", "THIN", "AXIS", "DIM"]:
    if name not in doc.layers:
        doc.layers.new(name)

try:
    doc.linetypes.load("CENTER", "acad.lin")
    doc.layers.get("AXIS").dxf.linetype = "CENTER"
except Exception:
    pass

if "ESKD" not in doc.dimstyles:
    doc.dimstyles.new(
        "ESKD",
        dxfattribs={
            "dimtxt": TEXT_H,
            "dimasz": 2.5,
            "dimexe": 1.5,
            "dimexo": 1.0,
            "dimdsep": 44,
        },
    )

y1 = -D1 / 2
y2 = D1 / 2
y3 = -D2 / 2
y4 = D2 / 2
h = d / 2

msp.add_lwpolyline([(0, y1), (L, y1), (L, y2), (0, y2), (0, y1)], dxfattribs={"layer": "CONTUR"})
msp.add_lwpolyline([(0, y3), (L2, y3), (L2, y4), (0, y4), (0, y3)], dxfattribs={"layer": "CONTUR"})

msp.add_line((0, -h), (L, -h), dxfattribs={"layer": "THIN"})
msp.add_line((0, h), (L, h), dxfattribs={"layer": "THIN"})

msp.add_line((-AXIS_OVER, 0), (L + AXIS_OVER, 0), dxfattribs={"layer": "AXIS"})
msp.add_line((0, y3 - AXIS_OVER), (0, y4 + AXIS_OVER), dxfattribs={"layer": "AXIS"})

msp.add_line((L, D1 / 2), (L - C, D1 / 2 - C), dxfattribs={"layer": "THIN"})
msp.add_line((L, -D1 / 2), (L - C, -D1 / 2 + C), dxfattribs={"layer": "THIN"})

x_dim_hole = L + OFF_1
dim_hole = msp.add_linear_dim(base=(x_dim_hole, 0), p1=(L, -h), p2=(L, h), angle=90, dimstyle="ESKD")
dim_hole.dimension.dxf.layer = "DIM"
dim_hole.dimension.dxf.text = f"⌀{d}"
dim_hole.render()

x_dim_d1 = L + OFF_1 + 14
dim_d1 = msp.add_linear_dim(base=(x_dim_d1, 0), p1=(L, y1), p2=(L, y2), angle=90, dimstyle="ESKD")
dim_d1.dimension.dxf.layer = "DIM"
dim_d1.dimension.dxf.text = f"⌀{D1}"
dim_d1.render()

x_dim_d2 = -OFF_1 - 14
dim_d2 = msp.add_linear_dim(base=(x_dim_d2, 0), p1=(0, y3), p2=(0, y4), angle=90, dimstyle="ESKD")
dim_d2.dimension.dxf.layer = "DIM"
dim_d2.dimension.dxf.text = f"⌀{D2}"
dim_d2.render()

y_dim1 = y3 - OFF_1
y_dim2 = y_dim1 - OFF_6

dim_L2 = msp.add_linear_dim(base=(0, y_dim1), p1=(0, y3), p2=(L2, y3), angle=0, dimstyle="ESKD")
dim_L2.dimension.dxf.layer = "DIM"
dim_L2.dimension.dxf.text = f"{L2}"
dim_L2.render()

dim_L = msp.add_linear_dim(base=(0, y_dim2), p1=(0, y3), p2=(L, y3), angle=0, dimstyle="ESKD")
dim_L.dimension.dxf.layer = "DIM"
dim_L.dimension.dxf.text = f"{L}"
dim_L.render()

txt_x = L - C - 6
txt_y = y2 + OFF_1 + 2
msp.add_text("2×45°", dxfattribs={"height": TEXT_H, "layer": "DIM"}).set_placement((txt_x, txt_y))
msp.add_line((txt_x + 1, txt_y - 1), (L - C / 2, y2 - C / 2), dxfattribs={"layer": "THIN"})

doc.saveas(OUT_PATH)
print(f"Saved: {OUT_PATH}")
