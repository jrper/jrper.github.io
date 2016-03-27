---
title: Trying out Hombrew
---

When I bought a new macbook four years ago, I made the decision to migrate from [fink](http://www.finkproject.org) to [macports](https://www.macports.org). Now, having decided to make the upgrade to El Capitan, I'm also experimenting with [homebrew](http://brew.sh). This time however, I'm attempting to run both package managers simultaneously. I'm not, however doing this in parallel (the homebrew people specifically warn against this, and neither system would be particularly happy).

Given that I idealogically object to brew's preferred choice to install in `/usr/local` and that I already have the `modules` [environment module](http://modules.sourceforge.net) control system installed on my mac, I've set things up so that my path can be switched by running

%{ highlight bash %}
module load homebrew
%{ endhighlight %}

or

%{ highlight bash %}
module load macports
%{ endhighlight %}

to place either tool into my default path. Let the unnecessary duplication begin.
