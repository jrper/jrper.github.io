---
title: Git recipes - Part III
---

Yesterday we dealt with some git commands which allow it to be used as originally intended. Today we'll move on to some powerful, but dangerous commands which (almost) literally allow developers to rewrite history.

## Interactive rebasing

The basic command is

{% highlight bash %}
git rebase -i commit_identifier
{% endhighlight %}

This will bring up a list in your famourite text editors of all commits between the one named and the current head. For example:

{% highlight console %}
pick 90d76c1 Add ShowCVs filter to the paraview plugins page.
pick 5b9017f Blogging some git recipes.
pick 8f6c9b0 Another blog post on git.

# Rebase 533d109..8f6c9b0 onto 533d109 (3 command(s))
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
{% endhighlight %}

The commented lines at the bottom provide a note memoir on what can be done. Effectively the incremental changes listed can be

* Reordered, by reordering the lines in the list
* Relabelled by using the `reword` option to change the commit message
* Ammended, using the `edit` option to stop at that commit for a manual change
* Collapsed, using the `fixup` or `squash` options to chain changesets into a single commit.

The last option is particularly suitable for hiding bug fixes from the outside world.

## Automatic rebasing

Another version of the rebase command

{% highlight bash %}
git rebase --autosquash -i
{% endhighlight %}

Scans the log of commit messages and sets commits which begin like `squash!5b9017f` or `fixup!5b9017f` in correct position and with the relevant option. A new commit can also be set with this option by using one of the forms

{% highlight bash %}
git commit --squash 123456
git commit --fixup 123456
{% endhighlight %}

## Further references

* [Git documentation](https://git-scm.com/documentation) at git-scm.com
* [Git tutorial](http://gitimmersion.com/index.html) at gitimmersion.com
* [Git tutorial](http://swcarpentry.github.io/git-novice/) at software carpentry


