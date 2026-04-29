from zcyptobot import Orchestrator


def main() -> None:
    o = Orchestrator()
    print(o.run_cycle())


if __name__ == "__main__":
    main()
