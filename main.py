import json
import cadquery as cq



with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

dims = cfg["dimensions"]

L = dims["L"]
L2 = dims["L2"]
D1 = dims["D1"]
D2 = dims["D2"]
d = dims["d"]
C = dims["C"]



model = (
    cq.Workplane("XY")
    .circle(D2 / 2)
    .extrude(L2)
    .faces(">Z")
    .workplane()
    .circle(D1 / 2)
    .extrude(L - L2)
    .faces(">Z")
    .edges("%CIRCLE")
    .chamfer(C)
    .faces("<Z")
    .workplane()
    .hole(d)
)



cq.exporters.export(model, "output/model.step", exportType="STEP")
print("Saved: output/model.step")
