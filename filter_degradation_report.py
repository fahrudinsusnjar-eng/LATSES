import matplotlib.pyplot as plt


def generate_filter_report(history):
    """
    Analizira istoriju iz ProvenanceLedger i crta trend rasta otpora filtera.
    """
    data_points = []

    for entry in history:
        # Podrzava i "data" (trenutni ledger) i "metrics" (alternativni format).
        metrics = entry.get("data") or entry.get("metrics") or {}
        if "filter_resistance" in metrics:
            data_points.append(metrics["filter_resistance"])

    if not data_points:
        print("Upozorenje: Nema podataka o otporu filtera u ledgeru.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(
        data_points,
        marker="o",
        linestyle="-",
        color="b",
        linewidth=2,
        label="Otpor filtera (Pa)",
    )

    plt.title("LAT-CES Analitika: Trend degradacije filtera", fontsize=14)
    plt.xlabel("Broj izvrsnih tikova", fontsize=12)
    plt.ylabel("Otpor filtera (Relativne jedinice)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    output_path = "filter_degradation_report.png"
    plt.savefig(output_path)
    print(f"Izvjestaj uspjesno generisan: {output_path}")
    plt.show()


if __name__ == "__main__":
    print("Ova skripta je dizajnirana da se pozove nakon sto se popuni ProvenanceLedger.")
