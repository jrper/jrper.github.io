---
title: Git recipes - Part I
---

The utility `git` is the Version Control System of choice within AMCG. Git appears to be coming to dominate the open source version control software world, replacing the centralized `svn` and the now undersupported `bzr`. As an essentially distributed version control framework, `git` can take some effort to learn for people with experience of other software, especially `svn` users, when used in large teams. So, lets begin with some basic recipes for svn users.

### The first command to know

A key command for any new git user to learn is `git status`. If you use this in a working directory in which any series editing has taken place, you are likely likely to be distracted by a lot of superfluous output about untracked files which are not (and which you don't wish to be) under version control. This can be supressed on a single occasion by using a flag,

    git status -uno

Alternatively, to achieve this behaviour by default (which I recommend) run this command on each relevant machine,

    git config --global status.showUntrackedFiles no

With untracked files supressed this may produce output like

{% highlight console %}
On branch master
Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
nothing to commit (use -u to show untracked files)
{% endhighlight %}

Note in particular in this case the message that the local repository is behind the remote repository by several commits. Given the use of local commits it may also be possible for the local repository to be ahead of the remote.

Unfortunately the status of the remote repository only updates when triggered by a suitable git command, such as `git fetch` or `git pull`. We'll address that problem next.

### Replacing svn update

Experienced svn users often expect the command `git pull` to be a like for like replacement for the command they are used to, `svn update`. Unfortunately, due to the distributed nature of the Git paradigm, this isn't precisely the case: Git will merge local and remote commits, attempting to generate a final state consistant with both. To get a more SVN-like behaviour, consider using a command pair like

    git fetch
    git rebase origin/master

This assumes that the remote repository has been nicknamed `origin` and that the remote upstream branch is called `master`. If you don't understand the last sentence, then these are both quite likely to be the case, since these are both default names used within git. Unlike a simple pull, this creates a linear history based off the latest version of the branch on the remote repository, to which it then applies the local commits incrementally, halting when conflicts occur. These should be fixed, in the manner that SVN users are used to, however if multiple local commits have occured, it is necessary to trigger the next increment using the command

    git rebase --continue

### Replacing svn commit

Again SVN users are liable to be seduced into believing the similarly named command, `git commit` will do the same job. In fact the command `svn commit ` effectively performs what git considers four seperate tasks:

* Contact the remote repository and check that the potential update can be applied to achieve a consistant final state.
* Stage all changes to all tracked files.
* Commit the change list into a single update.
* Push/publish the update to the remote directory.

This group of four commands can be reinterpretted into git as

{% highlight bash %}
git fetch # contact the remote
git add -u # stage all untracked files
git commit # perform a local commit on this branch
git push  # publish the results to the remote repository
{% endhighlight %}

If all is successful, then output will be returned something like

{% highlight console %}
Counting objects: 6, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 49.76 KiB | 0 bytes/s, done.
Total 6 (delta 2), reused 0 (delta 0)
To git@github.com:jrper/jrper.github.io.git
   601a64b..2845b21  master -> master
{% endhighlight %}

If the histories of the local and remote branches have diverged then an error message will be returned along those lines. In this case, we can follow the recipe from the previous section to fix conflicts, then repush.

{% highlight bash %}
git rebase origin/master
git push
{% endhighlight %}

## Further references

* [Git documentation](https://git-scm.com/documentation) at git-scm.com
* [Git tutorial](http://gitimmersion.com/index.html) at gitimmersion.com
* [Git tutorial](http://swcarpentry.github.io/git-novice/) at software carpentry

