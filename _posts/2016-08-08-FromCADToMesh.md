---
title: From CAD File to Fluid Mesh
---


These notes describe a process for converting a set of CAD files in .stp format into a volume mesh which can be simulated using _Fluidity_. The proximate reason is the exercise in processing a CAD model of a centrifugal pump provided by an industrial contact, so ther won't be many images, but this should still cover the key points:

Briefly the process is:

1. Convert the .stp file(s) into .stl files (by generating a 2d mesh)
2. Generate additional surfaces to close the space occupied by the fluid
3. Add labels for the surfaces.
4. Unify the faces together and remove duplicate vertices or degenerate faces.
5. Mesh the closed volume bounded by the unified surface.

This whole process can be achieved using  a sufficiently advanced GMSH build, installation of VTK for python, ParaView, and a lot of scripting.

##Meshing the CAD surfaces##

Provided your version of GMSH has been build with OpenCASCADE support, it is able to read many .stp files and extract the two dimensional surface geometries. Furthermore it can generate a triangulation representing that geometry and then output it in .stl format. The command will be of the form:

```
gmsh -2 input.stp -clmax 10 -format stl -o output.stl
```

Unfortunately this meshing is unlikely to be perfect, and may introduce degenerate triangles or duplicate vertices which could impact on the closure and quality of the final mesh.

##Closing the boundary##

_<section could be improved>_

This can be performed in a graphical environment using ParaView, GMSH, plus one of my VTK/ParaView plugins (to output a GMSH .msh file) and a simple python script to convert a .msh file into .geo file. The process goes as follows:

 1. First load the combied surfaces into ParaView.
 2. Use the Extract Edges filter to reduce the polygonal faces of the surfaces down to their constituent edges.
 3. Apply a suitable set of filters (e.g. a Calculator filter, followed by a Threshold filter) to extract only the edges lying on the open boundaries.
 4. Save these boundaries to a .msh file using my plugin.
 5. Run the following script on the gmsh mesh:
{% highlight python %}
{% raw %}
def msh2geo(m):

    string=""

    for k,x in m.nodes.items():
        string += 'Point(%d) = {%f,%f,%f};\n'%(k,x[0],x[1],x[2])
    
    for k,l in m.elements.items():
        string += "Line(%d) = {%d,%d};\n"%(k,l[2][0],l[2][1])

    return string
{% endraw %}
{% endhighlight %}
 6. Load the .geo file this creates in the GMSH gui and add the extra surface
 7. Mesh and output as an .stl file.

##Labelling##

Create a .geo file like the following:

{% highlight text %}
Merge "file1.stl";
Merge "file2.stl";
Merge "file3.stl";
Merge "file4.stl";
Merge "file5.stl";

Physical Surface (1) = 1;
Physical Surface (2) = 2;
Physical Surface (3) = 3;
Physical Surface (4) = 4;
Physical Surface (5) = 5;
{% endhighlight %}

When processed with GMSH this will create a surface mesh with the correct labels.

## Mesh Surgery and Cleanup##

_<section could be improved>_

We now return to VTK world to fix up the mesh. Run the `merge_grid` function in the following script:

{% highlight python %}
{% raw %}

def merge_points(ugrid):

    mf = vtk.vtkMergePoints()
    pts = vtk.vtkPoints()
    mf.InitPointInsertion(pts,ugrid.GetBounds())

    point_map = []
    n_nonunique = 0

    for i in range(ugrid.GetNumberOfPoints()):
        newid = vtk.mutable(0)
        n_nonunique += mf.InsertUniquePoint(ugrid.GetPoint(i),newid)
        point_map.append(newid)

    return pts, point_map

def merge_grid(ugrid):
    pts, point_map = merge_points(ugrid)

    vgrid = vtk.vtkUnstructuredGrid()

    vgrid.SetPoints(pts)

    cell_map = []

    for i in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(i)
        ids = vtk.vtkIdList()

        if cell.ComputeArea()==0.0:
            continue

        cell_map.append(i)

        for j in range(cell.GetPointIds().GetNumberOfIds()):
            ids.InsertNextId(point_map[cell.GetPointIds().GetId(j)])

        vgrid.InsertNextCell(cell.GetCellType(),ids)

    cd = vgrid.GetCellData()
    icd = ugrid.GetCellData()

    cd.CopyStructure(icd)

    for i in range(icd.GetNumberOfArrays()):
        data = cd.GetArray(i)
        idata = icd.GetArray(i)

        data.SetNumberOfComponents(idata.GetNumberOfComponents())
        data.SetNumberOfTuples(vgrid.GetNumberOfCells())

        for i in range(vgrid.GetNumberOfCells()):
            data.SetTuple(i, cell_map[i], idata)
        
    return vgrid

{% endraw %}
{% endhighlight %}

This removes duplicate points and degenerate triangles, but preserves the remaining information.

## The Final Meshing ##

The last task is to mesh the object. The following script creates a .geo file from the mesh, while preserving the surface label information:

{% highlight python %}
{% raw %}
def msh2geo3d(m, use_ids=False):

    string=''

    for k,x in m.nodes.items():
        string += 'Point(%d) = {%f,%f,%f};\n'%(k,x[0],x[1],x[2])
    
    ids = {}

    for k,l in m.elements.items():

        ids.setdefault(l[1][-1],[]).append(k)

        string += "Line(%d) = {%d,%d};\n"%(3*(k-1)+1,l[2][0],l[2][1])
        string += "Line(%d) = {%d,%d};\n"%(3*(k-1)+2,l[2][1],l[2][2])
        string += "Line(%d) = {%d,%d};\n"%(3*(k-1)+3,l[2][2],l[2][0])
        string += "Line Loop(%d) = {%d,%d,%d};"%(k,
                                                 3*(k-1)+1,
                                                 3*(k-1)+2,
                                                 3*(k-1)+3)
        string += "Plane Surface(%d) = %d;"%(k,k)

    print ids

    string += "Surface Loop(1) = {%s};\n"%(",".join([str(k+1) for k in range(len(m.elements))]))
    string += "Volume(1) = 1;\n"
    string += "Physical Volume(1) = 1;\n"
    string += "Coherence;\n"

    if use_ids:
        for k, v in ids.items():
            string += "Physical Surface(%d) = {%s};\n"%(k,",".join(map(str,v)))

    return string
{% endraw %}
{% endhighlight %}

Add a Volume and Physical Volume to the .geo file (e.g. using the GUI), then ask for a 3D mesh and we're done.
