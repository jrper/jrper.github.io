---
title: Note to self - disabling whitespace in liquid
tags: liquid jekyll
---

It appears that when generating static websites using `liquid`, the default syntax,
{% highlight liquid %}
{% raw %}
{% for a in b %}
	{{ a }}
{% endfor %}
{% endraw %}
{% endhighlight %}

produces a newline in the raw html for each line of liquid. This can be prevented by using hyphens all over the place:

{% highlight liquid %}
{% raw %}
{%- for a in b -%}
	{{- a -}}
{%- endfor -%}
{% endraw %}
{% endhighlight %}

which looks really weird, but seems to curb its enthusiam.
