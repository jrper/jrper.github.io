---
title: Git recipes - Part II
---

Yesterday we dealt with methods for SVN users to try to pretend they aren't being forced to use git. Today we'll move on to some recipes to take advantage of the strengths of git.

### Local commits

We referred to these frequently in our previous recipes. These are easy enough to create, however it must be remembered that this is a two stage process, first

{% highlight bash %}
git add file1 file2 file3 ... # place files in staging area
{% endhighlight %}

and then

{% highlight bash %}
git commit -m "My commit message"  # Move staged files into a local commit.
{% endhighlight %}

The staging area can sometimes be an annoyance, and exposes the framework nature of `git` as a version control tool, however it can also be useful. It is the difference of the staged versions of the files from the previous commit which are stored in the commit, rather than the difference of the working directory. Using tools such as the interactive addition mode, `git add -i` large change can be broken down and applied across several logical commits.

### Making new branches

As a framework, git doesn't enforce any single workflow on users, however almost all sane workflows use branches to some extent to reconcile the need for a stable, trusted, code-base and freedom for developers to refactor or modify individual sections of code. Unfortunately this is an area in which `git` has chosen some obscure and badly un-mnemonic syntax. To create a new branch from an exising one use
 
{% highlight bash %}
git checkout -n new_branch_name old_branch_name
{% endhighlight %}

To list the existing local branches use

{% highlight bash %}
git branch
{% endhighlight %}

To list all known named branches, both local and remote, requires a flag, `git branch -a`. More generally passing flags to `git branch` is used to interact with existing branches generally to delete `-d`, forced delete `-D`, move or forced move `-M` them. The forced actions should be used judiciously, since they off the potential for data loss (or certainly to make such data difficult to recover).

### Transfering commit information between branches

A useful, although dangerous command in the git armoury is `git cherry-pick`. This allows a chain of commit increments to be selected and applied to the current branch. To grab a single commit the form

{% highlight bash %}
git cherry-pick 90d76c1
{% endhighlight %}

where the alphanumeric code is the sha1 hash of the commit desired. Note that when the commit applied to the current branch git will often generate a new hash identifier, since the hash is a function of the sum of the history which caused that point to be reached, and this may differ. Since a branch name is just a moving label for a commit this can also be used for a cherry-pick, either singlely

{% highlight bash %}
git cherry-pick my_cool_feature_branch
{% endhighlight %}

or in the chain form

{% highlight bash %}
git cherry-pick master..my_cool_feature_branch
{% endhighlight %}

Note that the chain form applies every commit after the first one named (so in this case the first addition on top of master in my_cool_feature_branch). This can be an off by one trap for the unwary.

## Further references

* [Git documentation](https://git-scm.com/documentation) at git-scm.com
* [Git tutorial](http://gitimmersion.com/index.html) at gitimmersion.com
* [Git tutorial](http://swcarpentry.github.io/git-novice/) at software carpentry

