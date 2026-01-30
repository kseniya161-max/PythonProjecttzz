import cadquery as cq

L = 60
L2 = 20
D1 = 24
D2 = 36
d = 12
C = 2

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
