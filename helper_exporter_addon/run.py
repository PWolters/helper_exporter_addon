import json
import yaml
from pathlib import Path

total = 0

for slug in ["input_number", "input_text", "input_boolean", "input_datetime"]:
    try:
        with open(f"/config/.storage/{slug}", "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("data", {}).get("items", [])
        out = {}
        for item in items:
            key = item.get("alias") or item.get("id")
            if not key:
                continue
            obj = {"name": item.get("name", key)}
            if slug == "input_number":
                obj.update({
                    "min": item.get("min", 0),
                    "max": item.get("max", 100),
                    "step": item.get("step", 1),
                    "mode": item.get("mode", "slider"),
                    "initial": item.get("initial", 0)
                })
            elif slug == "input_text":
                obj.update({
                    "initial": item.get("initial", ""),
                    "max": item.get("max", 255)
                })
            elif slug == "input_boolean":
                obj.update({
                    "initial": item.get("initial", False)
                })
            elif slug == "input_datetime":
                if "has_time" in item and "has_date" in item:
                    obj.update({
                        "has_time": item["has_time"],
                        "has_date": item["has_date"],
                        "initial": item.get("initial")
                    })
            out[key] = obj

        path = Path(f"/config/helpers/{slug}.yaml")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(out, f, sort_keys=False, allow_unicode=True)
        print("✓ Exportiert", len(out), slug, "→", path)
        total += len(out)
    except Exception as e:
        print(f"⚠️ Fehler bei {slug}:", e)

print(f"=== Gesamt: {total} Helfer exportiert ===")
