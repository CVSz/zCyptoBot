{{- define "zeaz.name" -}}
zeaz
{{- end -}}

{{- define "zeaz.fullname" -}}
{{ include "zeaz.name" . }}
{{- end -}}
