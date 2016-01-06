---
title: Example - ShowCVs.xml 
---

{% highlight xml %}
<ServerManagerConfiguration>
  <ProxyGroup name="filters">
    <SourceProxy name="vtkShowCVs" class="vtkShowCVs" label="Show Control Volumes">
      <Documentation long_help="Calculate a Vornoi tesselation to show the control volume structure." short_help="Show Control Volumes">
      </Documentation>
      <InputProperty
	  name="Input"
	  command="SetInputConnection">
	<ProxyGroupDomain name="groups">
	  <Group name="sources"/>
	  <Group name="filters"/>
	</ProxyGroupDomain>
	<DataTypeDomain name="input_type">
	  <DataType value="vtkUnstructuredGrid"/>
	</DataTypeDomain>
      </InputProperty>
    </SourceProxy>
  </ProxyGroup>
</ServerManagerConfiguration>
{% endhighlight %}