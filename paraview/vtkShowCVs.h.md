---
title: Example - vtkShowCVs.h 
---

{% highlight cpp %}
#include "vtkDataObjectAlgorithm.h"

#include "vtkUnstructuredGridAlgorithm.h"

class vtkShowCVs : public vtkUnstructuredGridAlgorithm
{
 public:
  static vtkShowCVs* New();
  vtkTypeRevisionMacro(vtkShowCVs,vtkUnstructuredGridAlgorithm);

 protected:

  vtkShowCVs();
  ~vtkShowCVs();

  virtual int RequestData(
			  vtkInformation* request,
			  vtkInformationVector** InputVector,
			  vtkInformationVector* outputVector);
  virtual int RequestUpdateExtent(
			  vtkInformation* request,
			  vtkInformationVector** InputVector,
			  vtkInformationVector* outputVector);
  virtual int FillInputPortInformation(int port,vtkInformation *info);

};
{% endhighlight %}
