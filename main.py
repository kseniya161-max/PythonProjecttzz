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
solid = model.val()
volume_mm3 = solid.Volume()
volume_m3 = volume_mm3 / 1e9

material = cfg.get("material", {})
density = float(material["density"])
material_name = material.get("name", "Unknown")

mass_kg = density * volume_m3
price_per_kg = float(material.get("price_per_kg", 0))
cost = mass_kg * price_per_kg

report = {
    "material": {
        "name": material_name,
        "density_kg_m3": density,
        "price_per_kg": price_per_kg
    },
    "geometry": {
        "volume_m3": volume_m3,
        "mass_kg": round(mass_kg, 3)
    },
    "cost": {
        "total": round(cost, 2),
        "currency": "RUB"
    },
    "dimensions_mm": {
        "L": L,
        "L2": L2,
        "D1": D1,
        "D2": D2,
        "d": d,
        "C": C
    }
}


def save_report(report: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)


report_path = cfg.get("output", {}).get("report_path", "output/report.json")
save_report(report, report_path)
print(f"Saved report: {report_path}")
print(f"Price: {price_per_kg:.2f} per kg")
print(f"Cost: {cost:.2f}")
print(f"Material: {material_name}")
print(f"Volume: {volume_m3:.6e} m³")
print(f"Mass: {mass_kg:.3f} kg")



cq.exporters.export(model, "output/model.step", exportType="STEP")
print("Saved: output/model.step")

