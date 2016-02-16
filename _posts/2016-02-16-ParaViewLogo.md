---
title: Adding a logo to a ParaView window
---

The vtkLogoWidget class exists to allow logo insertion in standard VTK render instances, but what about in ParaView? It turns out you can still use it fine. Run the following script in the ParaView python shell, or even make it a macro!

{% highlight python %}
from paraview.simple import *
import vtk 

image = vtk.vtkPNGReader()
image.SetFileName('Logo.png')
image.Update()

rep = vtk.vtkLogoRepresentation()
rep.SetImage(image.GetOutput())

widget = vtk.vtkLogoWidget()
widget.SetRepresentation(rep)
widget.SetInteractor(GetRenderView().GetInteractor())
widget.On()
{% endhighlight %}
