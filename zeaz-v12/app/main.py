from app.aiops.orchestrator import AIOps
from app.sim.simulator import SystemSimulator

sim = SystemSimulator()
ai = AIOps()

while True:
    state = sim.state
    action = ai.step(state)
    new_state = sim.step(action)
    print("ACTION:", action, "STATE:", new_state)
