def generate_proof(trace_hash: str) -> str:
    """Hook for external prover backends (gnark/halo2/snarkjs)."""
    return f"proof_for_{trace_hash}"


def verify_proof(proof: str) -> bool:
    return proof.startswith("proof_for_")
