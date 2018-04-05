---
title: Adding tags to a Github Pages blog
tags: ruby jekyll
---

Today I got round to adding tag support to this blog. The code to process the [tags page]({{ site.url }}/tags.html) looks like the following:

{% highlight html %}
{% raw  %}
{% for tag in site.tags %}
  {% assign t = tag | first %}
  {% assign posts = tag | last %}
  <div id="tags">
	<a name="{{ t | downcase }}"></a><a href ="/tags.html#{{ t | downcase }}">{{ t | downcase }}</a>
  </div>
  <ul>
    {% for post in posts %}
		{% if post.tags contains t %}
			<li>
				<a href="{{ post.url }}">{{ post.title }}</a>
				<span class="date">{{ post.date | date: "%B %-d, %Y"  }}</span>
			</li>
		{% endif %}
	{% endfor %}
  </ul>
{% endfor %}
{% endraw %}
{% endhighlight %}

meanwhile the block at the end of the blog post layout is

{% highlight html %}
{% raw  %}
{% if page.tags.size > 0 %}
<div id="tags">
tags:
{% for t in page.tags %}
    <a href="/tags.html/#{{ t | downcase | replace:' ','-' }}">{{ t | downcase }}</a>
{% endfor %}
</div>
{% endif %}
{% endraw %}
{% endhighlight %}

