FROM openpolicyagent/opa:0.64.0

COPY ./policies /policies
CMD ["run", "--server", "--addr=0.0.0.0:8181", "--set=decision_logs.console=true", "/policies"]
