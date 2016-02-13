---
title: Test if a variable exists in python
---

Sometimes we want to write a snippet which acts only if a variable doesn't existThis one is fairly straightforward to do using the globals function:

{% highlight python %}
	if 'varname' not in globals():
		varname = 'Here now!'
		# do stuff
	else:
		print varname
{% endhighlight %}

I wonder if there's a better way?
		
