import python

from FunctionCall fc
where
  fc.getTarget().getName() = "execute" and
  not exists(FunctionCall r |
    r.getTarget().getName() = "validate" and
    r.getEnclosingCallable() = fc.getEnclosingCallable()
  )
select fc, "Execution without risk validation"
