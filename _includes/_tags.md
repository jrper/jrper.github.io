{% if include.obj.tags.size > 0 %}
<br>
<div id="tags">
tags:
{% for t in include.obj.tags %}
    <a href="/tags.html/#{{ t | downcase | replace:" ","-" }}">{{ t | downcase }}</a>
{% endfor %}
</div>
{% endif %}
