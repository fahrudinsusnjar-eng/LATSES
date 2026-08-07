import matplotlib.pyplot as plt
import json


def generate_filter_report(file_path="data/provenance_ledger.jsonl"):
    data_points = []

    # Citanje direktno iz fajla
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                metrics = entry.get("metrics", {})
                if "filter_resistance" in metrics:
                    data_points.append(metrics["filter_resistance"])
    except FileNotFoundError:
        print("Fajl sa podacima nije pronadjen.")
        return

    if not data_points:
        print("Nema podataka o otporu filtera.")
        return

    # Plotovanje
    plt.figure(figsize=(10, 6))
    plt.plot(data_points, marker="o", linestyle="-", color="r")
    plt.title("Dugorocni trend degradacije filtera")
    plt.ylabel("Otpor (Pa)")
    plt.xlabel("Vrijeme (Log zapisi)")
    plt.grid(True)
    plt.savefig("filter_degradation_longterm.png")
    print("Grafikon snimljen kao filter_degradation_longterm.png")
