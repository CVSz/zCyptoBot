import python

from Function f
where
  f.getName().matches("%order%") and
  not exists(FunctionCall c |
    c.getTarget().getName() = "check_tenant"
  )
select f, "API endpoint missing tenant validation"
