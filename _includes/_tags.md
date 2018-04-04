{% if page.tags.size > 0 %}
<div id="tags"}>
tags:
{% for t in page.tags %}
    <a href="/tags.html/#{{ t | downcase | replace:" ","-" }}">{{ t | downcase }}</a>
{% endfor %}
</div>
{% endif %}
