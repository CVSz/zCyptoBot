from app.observability.metrics import orders_executed


class ExecutionEngine:
    async def execute(self, sig: str, size: float) -> None:
        orders_executed.labels(side=sig).inc()
        print(f"EXEC {sig} {size}")
