import python

from FunctionCall fc, Function f
where
  fc.getTarget().getName() = "execute" and
  not exists(FunctionCall check |
    check.getTarget().getName() = "enforce_tenant" and
    check.getEnclosingCallable() = fc.getEnclosingCallable()
  )
select fc, "Execution without tenant isolation check"
