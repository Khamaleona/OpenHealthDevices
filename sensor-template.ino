{% for lib in templ["libraries"] %}
{{lib}}
{% endfor %}

{% for cons in templ["constants"] %}
{{cons}}
{% endfor %}

{% for var in templ["codeVars"] %}
{{var}}
{% endfor %}

{% for sett in templ["settings"] %}
{{sett}}
{% endfor %}

{% for c in templ["code"] %}
{{c}}
{% endfor %}