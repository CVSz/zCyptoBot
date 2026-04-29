import subprocess


class Validator:
    def run_unit(self) -> bool:
        p = subprocess.run(["pytest", "-q"], capture_output=True)
        return p.returncode == 0

    def run_lint(self) -> bool:
        p = subprocess.run(["python", "-m", "py_compile", "-q", "."], capture_output=True)
        return p.returncode == 0

    def simulate(self) -> float:
        import random

        return random.uniform(0.0, 1.0)

    def validate(self) -> tuple[bool, dict]:
        ok = self.run_lint() and self.run_unit()
        score = self.simulate()
        return ok, {"sim_score": score}
