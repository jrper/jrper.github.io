---
title: A basic navigation toolbar
tags: css jekyll liquid
---

Adding navigation buttons to a layout is really easy. First the `.css` to generate the buttons and  arrows:

{% highlight css %}

#button a:link, #button a:visited {
    background-color: Indigo;
    color: white;
    padding: 1px 6px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    border-radius: 5px;
}


#button a:hover, #button a:active {
    color: Aqua;
    background-color: Navy;
}

i {
    border: solid white;
    border-width: 0 3px 3px 0;
    display: inline-block;
    padding: 3px;
}

.right {
    transform: rotate(-45deg);
    -webkit-transform: rotate(-45deg);
}

.left {
    transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
}

.up {
    transform: rotate(-135deg);
    -webkit-transform: rotate(-135deg);
}

.down {
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
}
{% endhighlight %}

then the `html` fragment to put in the layout files. 

{% highlight html %}
{% raw %}
{% if page.previous %}
<div style="float:left" id="button"><a href="{{ page.previous.url }}"> <i class="arrow left"></i> {{ page.previous.title | truncate: 40 }}</a></div>
{% endif %}
{% if page.next %}
<div style="float:right" id="button"><a href="{{ page.next.url }}">{{ page.next.title | truncate: 40 }} <i class="arrow right"></i></a></div>
{% endif %}
{% endraw %}
{% endhighlight %}
