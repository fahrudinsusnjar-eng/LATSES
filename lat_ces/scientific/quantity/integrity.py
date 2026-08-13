"""Deterministic integrity hashes for scientific quantities."""
import hashlib
import json


def _canonical(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def generate_quantity_hash(quantity) -> str:
    data = {
        "quantity_id": quantity.quantity_id,
        "name": quantity.name,
        "symbol": quantity.symbol,
        "definition": quantity.definition,
        "dimension": str(quantity.dimension),
        "unit": str(quantity.unit),
        "equation": str(quantity.equation),
    }
    return hashlib.sha256(_canonical(data)).hexdigest()


def generate_equation_hash(equation) -> str:
    return hashlib.sha256(str(equation.expression).encode("utf-8")).hexdigest()


def verify_quantity_integrity(quantity, stored_hash: str) -> bool:
    return generate_quantity_hash(quantity) == stored_hash
