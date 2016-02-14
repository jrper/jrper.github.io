---
title: Colourful copying in Mac OS X
---

The [pygmentize tool](pygments.org) can automagically syntax mark up an awful lot of languages, but sometimes you need to paste the text into a windowed application. Fortunately on Mac OS X there's a convenient way of doing this making its way round the interweb. It makes use of rich text format (rtf) and the command line tool `pbcopy` which copies stdout to the mac pasteboard. The full command is

{% highlight bash %}
pygmentize -f rtf myfile.py | pbcopy
{% endhighlight %}

Now just paste and go.

