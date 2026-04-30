def enforce(output: str):
    banned = ["illegal", "harmful"]
    for b in banned:
        if b in output.lower():
            return "blocked"
    return output
