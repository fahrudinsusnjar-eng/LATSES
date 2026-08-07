import json
import os


class ProvenanceLedger:
    def __init__(self, file_path="data/provenance_ledger.jsonl"):
        self.file_path = file_path
        # Kreiraj direktorij ako ne postoji
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def record(self, event_name, metrics):
        """Zapisuje događaj u JSONL fajl odmah po pozivu."""
        record = {"event": event_name, "metrics": metrics}
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def get_history(self):
        """Učitava svu istoriju iz fajla."""
        history = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        history.append(json.loads(line))
        return history

    def clear_history(self):
        """Briše istoriju (korisno za resetovanje testova)."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
