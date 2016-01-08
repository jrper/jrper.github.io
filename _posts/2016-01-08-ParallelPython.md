---
title: Python in parallel with mpi4py
---

The module `mpi4py` makes it fairly trivial to make MPI calls within python scripts, by allowing first class python objects to be passed. As an example of a near  do nothing script, consider the following:

{% highlight python %}
## example.py
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print('rank %d of %d'%(rank,size))
{% endhighlight %}

When run on 4 processes this produces the following output:

{% highlight console %}
$> mpirun -np 4 python example.py

rank 2 of 4
rank 1 of 4
rank 3 of 4
rank 0 of 4
{% endhighlight %}

The usual MPI commands exist in two variants as methods on the communicator (in this case `comm` which has been set to MPI_COMM_WORLD). The lower case version supports python friendly objects,


{% highlight python %}

data_sent=rank
if rank==0:
	data_received = comm.recv(source=1, tag=13)
elif rank==1:
	comm.send(data_sent,dest=0, tag=13)
{% endhighlight %}

while the capitalized versions use numpy buffers (and are thus significantly faster).

