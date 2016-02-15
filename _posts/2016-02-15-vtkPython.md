---
title: Using straight VTK to render text
---

Lets write a simple script to display some text in a standard vtk window:

{% highlight python %}
#!/usr/bin/env python
from vtk import*
 
#Create a source
textSource = vtkVectorText();
textSource.SetText("Hello AMCG!");
textSource.Update();
 
#Create a mapper and actor
mapper = vtkPolyDataMapper();
mapper.SetInputConnection(textSource.GetOutputPort());
 
actor = vtkActor();
actor.SetMapper(mapper);
actor.GetProperty().SetColor(1, 0, 0)

 
#Create a renderer, render window, and interactor
renderer = vtkRenderer();
renderWindow = vtkRenderWindow();
renderWindow.AddRenderer(renderer);
renderWindowInteractor = vtkRenderWindowInteractor();
renderWindowInteractor.SetRenderWindow(renderWindow);
 
#Add the actor to the scene
renderer.AddActor(actor);
renderer.SetBackground(1,1,1); # Background color white
 
#Render and interact
renderWindow.Render();
renderWindowInteractor.Start();
{% endhighlight %}

You could run this under the vtkpython binary, but actually it'll probably work just fine with your normal python interpreter, assuming your vtk installation is remotely normal.
