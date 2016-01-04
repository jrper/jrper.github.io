---
title: Example - vtkShowCVs.cxx 
---

{% highlight cpp %}
#include "vtkShowCVs.h"

#include "vtkInformation.h"
#include "vtkInformationVector.h"
#include "vtkCell.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
#include "vtkIdTypeArray.h"
#include "vtkCellArray.h"
#include "vtkPoints.h"
#include "vtkUnstructuredGrid.h"
#include "vtkSmartPointer.h"
#include "vtkDataObject.h"
#include "vtkObjectFactory.h"
#include "vtkStreamingDemandDrivenPipeline.h"
#include "vtkTriangle.h"
#include "vtkQuadraticTriangle.h"
#include "vtkTetra.h"
#include "vtkQuad.h"
#include "vtkHexahedron.h"
#include "vtkPolygon.h"
#include "vtkDoubleArray.h"
#include "vtkGeometryFilter.h"
#include "vtkIntArray.h"
#include "vtkTrivialProducer.h"
#include <iostream>
#include <map>
#include <cmath>



vtkCxxRevisionMacro(vtkShowCVs, "$Revision: 0.5$");
vtkStandardNewMacro(vtkShowCVs);

void Average(vtkCell* cell,int id1,int id2, double out[3]) {
  double p1[3], p2[3];
  
  cell->GetPoints()->GetPoint(id1,p1);
  cell->GetPoints()->GetPoint(id2,p2);

  for (int i=0; i<3; i++) {
    out[i]=(p1[i]+p2[i])/2.0;
  }
}   

void Average(vtkCell* cell,int id1,int id2,int id3, double out[3]) {
  double p1[3], p2[3], p3[3];
  
  cell->GetPoints()->GetPoint(id1,p1);
  cell->GetPoints()->GetPoint(id2,p2);
  cell->GetPoints()->GetPoint(id3,p3);

  for (int i=0; i<3; i++) {
    out[i]=(p1[i]+p2[i]+p3[i])/3.0;
  }
}

void Average(vtkCell* cell,int id1,int id2,int id3,int id4, double out[3]) {
  double p1[3], p2[3], p3[3], p4[3];
  
  cell->GetPoints()->GetPoint(id1,p1);
  cell->GetPoints()->GetPoint(id2,p2);
  cell->GetPoints()->GetPoint(id3,p3);
  cell->GetPoints()->GetPoint(id4,p4);

  for (int i=0; i<3; i++) {
    out[i]=(p1[i]+p2[i]+p3[i]+p4[i])/4.0;
  }
} 

vtkShowCVs::vtkShowCVs(){
#ifndef NDEBUG
  this->DebugOn();
#endif
  this->Degree=-1;
  this->Continuity=0;
}
vtkShowCVs::~vtkShowCVs(){};

int vtkShowCVs::RequestData(
		      vtkInformation* vtkNotUsed(request),
		      vtkInformationVector **inputVector,
		      vtkInformationVector* outputVector )
{
  vtkInformation* outInfo=outputVector->GetInformationObject(0);
  vtkUnstructuredGrid* output= vtkUnstructuredGrid::SafeDownCast(outInfo->Get(vtkDataObject::DATA_OBJECT() ) );
  
  //  vtkInformation *inInfo=inputVector[0]->GetInformationObject(0);
  vtkUnstructuredGrid* input= vtkUnstructuredGrid::GetData(inputVector[0]);


  vtkSmartPointer<vtkMergePointFilter> mergeFilter= vtkSmartPointer<vtkMergePointFilter>::New();

  vtkDebugMacro(<<input->GetNumberOfCells() );


  vtkIdType NC=input->GetNumberOfCells();
  vtkIdType NP=input->GetNumberOfPoints();
  vtkIdType NF;

  vtkIdTypeArray* faces;

  vtkCell* cell=input->GetCell(0);
  int NPointsOut=0;
  int discontinuous=0;



  if (NC==0)
    {
      vtkDebugMacro(<<"NothingToExtract"<<NC<<NP);
      return 1;
    }  else {
    vtkDebugMacro(<<"Extracting Points" << NC);
  }


    switch (cell->GetCellType())
    {
    case  VTK_TRIANGLE:
      {
	  NPointsOut=3*NC;
      }
      break;
    case  VTK_TETRA:
      {
	  NPointsOut=4*NC;
      }
      break;
    }

    vtkSmartPointer<vtkPoints> outpoints= vtkSmartPointer<vtkPoints>::New();
    outpoints->Allocate(NPointsOut);


    output->Allocate(NP);
  

    for (vtkIdType j=0;j<NP;j++)
      {
	outpoints->InsertNextPoint(input->GetPoint(j));
      };
      
    for(vtkIdType i = 0;i<NC;i++)
	{
	  vtkDebugMacro(<<"GetCell " << i);
	  vtkCell* cell=input->GetCell(i);
	  vtkDebugMacro(<<"Get Points ");
	  vtkPoints* pts=cell->GetPoints();
	  
	  vtkIdType NPP=pts->GetNumberOfPoints();
	  
	  vtkIdList* ptsIds=vtkIdList::New();

	  double center[3];
	  
	  switch (cell->GetCellType())
	    {
	    case  VTK_TRIANGLE:
	   {
	     ptsIds->Allocate(6);
	     vtkTriangle::TriangleCenter(pts->GetPoint(0),
					 pts->GetPoint(1),
					 pts->GetPoint(2),
					 center);
	     vtkQuad* myQuad=vtkQuad::New();
	     
	     ptsIds->InsertNextId(cell->GetPointIds()->GetId(0));
	     ptsIds->InsertNextId(cell->GetPointIds()->GetId(1));
	     ptsIds->InsertNextId(cell->GetPointIds()->GetId(2));
	     
	     ptsIds->InsertNextId(outpoints->InsertNextPoint(
		  0.5*pts->GetPoint(0)[0]+0.5*pts->GetPoint(1)[0],
		  0.5*pts->GetPoint(0)[1]+0.5*pts->GetPoint(1)[1],
		  0.5*pts->GetPoint(0)[2]+0.5*pts->GetPoint(1)[2]
							   ));

	     ptsIds->InsertNextId(outpoints->InsertNextPoint(
		  0.5*pts->GetPoint(1)[0]+0.5*pts->GetPoint(2)[0],
		  0.5*pts->GetPoint(1)[1]+0.5*pts->GetPoint(2)[1],
		  0.5*pts->GetPoint(1)[2]+0.5*pts->GetPoint(2)[2]
							   ));
	     ptsIds->InsertNextId(outpoints->InsertNextPoint(
			0.5*pts->GetPoint(2)[0]+0.5*pts->GetPoint(0)[0],
			0.5*pts->GetPoint(2)[1]+0.5*pts->GetPoint(0)[1],
			0.5*pts->GetPoint(2)[2]+0.5*pts->GetPoint(0)[2]
							   ));

	     ptsIds->InsertNextId(outpoints->InsertNextPoint(
	      (pts->GetPoint(0)[0]+pts->GetPoint(1)[0]+pts->GetPoint(2)[0])/3.0,
	      (pts->GetPoint(0)[1]+pts->GetPoint(1)[1]+pts->GetPoint(2)[1])/3.0,
	      (pts->GetPoint(0)[2]+pts->GetPoint(1)[2]+pts->GetPoint(2)[2])/3.0
							   ));

	  
	     myQuad->GetPointIds()->SetId(0,ptsIds->GetId(0));
	     myQuad->GetPointIds()->SetId(1,ptsIds->GetId(3));
	     myQuad->GetPointIds()->SetId(2,ptsIds->GetId(6));
	     myQuad->GetPointIds()->SetId(3,ptsIds->GetId(5));
	     output->InsertNextCell(myQuad->GetCellType(),
				    myQuad->GetPointIds());

	     myQuad->GetPointIds()->SetId(0,ptsIds->GetId(1));
	     myQuad->GetPointIds()->SetId(1,ptsIds->GetId(4));
	     myQuad->GetPointIds()->SetId(2,ptsIds->GetId(6));
	     myQuad->GetPointIds()->SetId(3,ptsIds->GetId(3));
	     output->InsertNextCell(myQuad->GetCellType(),
				    myQuad->GetPointIds());

	     myQuad->GetPointIds()->SetId(0,ptsIds->GetId(2));
	     myQuad->GetPointIds()->SetId(1,ptsIds->GetId(5));
	     myQuad->GetPointIds()->SetId(2,ptsIds->GetId(6));
	     myQuad->GetPointIds()->SetId(3,ptsIds->GetId(4));
	     output->InsertNextCell(myQuad->GetCellType(),
				    myQuad->GetPointIds());

	     myQuad->Delete();

	     break;
	   }
	    case  VTK_TETRA:
	      {
		ptsIds->Allocate(15);
		vtkTetra::TetraCenter(pts->GetPoint(0),
				      pts->GetPoint(1),
				      pts->GetPoint(2),
				      pts->GetPoint(3),
				      center);
		
		vtkHexahedron* myHex=vtkHexahedron::New();
		
		ptsIds->InsertNextId(cell->GetPointIds()->GetId(0));
		ptsIds->InsertNextId(cell->GetPointIds()->GetId(1));
		ptsIds->InsertNextId(cell->GetPointIds()->GetId(2));
		ptsIds->InsertNextId(cell->GetPointIds()->GetId(3));


	   // Points 4-9 are the line midpoints 
	   // 4: 0-1
	   // 5: 1-2
	   // 6: 2-3
	   // 7: 3-0
	   // 8: 1-3
	   // 9: 0-2


		ptsIds->InsertNextId(outpoints->InsertNextPoint(
			0.5*pts->GetPoint(0)[0]+0.5*pts->GetPoint(1)[0],
			0.5*pts->GetPoint(0)[1]+0.5*pts->GetPoint(1)[1],
			0.5*pts->GetPoint(0)[2]+0.5*pts->GetPoint(1)[2]
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
		    0.5*pts->GetPoint(1)[0]+0.5*pts->GetPoint(2)[0],
		    0.5*pts->GetPoint(1)[1]+0.5*pts->GetPoint(2)[1],
		    0.5*pts->GetPoint(1)[2]+0.5*pts->GetPoint(2)[2]
							   ));
		ptsIds->InsertNextId(outpoints->InsertNextPoint(
		    0.5*pts->GetPoint(2)[0]+0.5*pts->GetPoint(3)[0],
		    0.5*pts->GetPoint(2)[1]+0.5*pts->GetPoint(3)[1],
		    0.5*pts->GetPoint(2)[2]+0.5*pts->GetPoint(3)[2]
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
		    0.5*pts->GetPoint(3)[0]+0.5*pts->GetPoint(0)[0],
		    0.5*pts->GetPoint(3)[1]+0.5*pts->GetPoint(0)[1],
		    0.5*pts->GetPoint(3)[2]+0.5*pts->GetPoint(0)[2]
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
			0.5*pts->GetPoint(3)[0]+0.5*pts->GetPoint(1)[0],
			0.5*pts->GetPoint(3)[1]+0.5*pts->GetPoint(1)[1],
			0.5*pts->GetPoint(3)[2]+0.5*pts->GetPoint(1)[2]
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
			0.5*pts->GetPoint(2)[0]+0.5*pts->GetPoint(0)[0],
			0.5*pts->GetPoint(2)[1]+0.5*pts->GetPoint(0)[1],
			0.5*pts->GetPoint(2)[2]+0.5*pts->GetPoint(0)[2]
							   ));



	   // Points 10-13 are the Triangle midpoints
	   // 10 : 0-1-2
	   // 11 : 3-0-1
	   // 12 : 2-3-0
	   // 13 : 1-2-3

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
	     (pts->GetPoint(0)[0]+pts->GetPoint(1)[0]+pts->GetPoint(2)[0])/3.0,
	     (pts->GetPoint(0)[1]+pts->GetPoint(1)[1]+pts->GetPoint(2)[1])/3.0,
	     (pts->GetPoint(0)[2]+pts->GetPoint(1)[2]+pts->GetPoint(2)[2])/3.0
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
	     (pts->GetPoint(0)[0]+pts->GetPoint(1)[0]+pts->GetPoint(3)[0])/3.0,
	     (pts->GetPoint(0)[1]+pts->GetPoint(1)[1]+pts->GetPoint(3)[1])/3.0,
	     (pts->GetPoint(0)[2]+pts->GetPoint(1)[2]+pts->GetPoint(3)[2])/3.0
							   ));

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
	     (pts->GetPoint(0)[0]+pts->GetPoint(3)[0]+pts->GetPoint(2)[0])/3.0,
	     (pts->GetPoint(0)[1]+pts->GetPoint(3)[1]+pts->GetPoint(2)[1])/3.0,
	     (pts->GetPoint(0)[2]+pts->GetPoint(3)[2]+pts->GetPoint(2)[2])/3.0
							   ));


		ptsIds->InsertNextId(outpoints->InsertNextPoint(
	     (pts->GetPoint(3)[0]+pts->GetPoint(1)[0]+pts->GetPoint(2)[0])/3.0,
	     (pts->GetPoint(3)[1]+pts->GetPoint(1)[1]+pts->GetPoint(2)[1])/3.0,
	     (pts->GetPoint(3)[2]+pts->GetPoint(1)[2]+pts->GetPoint(2)[2])/3.0
							   ));

	   
	   // Point 14 is the tet midpoint

		ptsIds->InsertNextId(outpoints->InsertNextPoint(
	     (pts->GetPoint(0)[0]+pts->GetPoint(1)[0]+pts->GetPoint(2)[0]
	      +pts->GetPoint(3)[0])/4.0,
	     (pts->GetPoint(0)[1]+pts->GetPoint(1)[1]+pts->GetPoint(2)[1]
	               +pts->GetPoint(3)[1])/4.0,
	     (pts->GetPoint(0)[2]+pts->GetPoint(1)[2]+pts->GetPoint(2)[2]
	               +pts->GetPoint(3)[2])/4.0
							   ));

	  
		myHex->GetPointIds()->SetId(0,ptsIds->GetId(0));
		myHex->GetPointIds()->SetId(1,ptsIds->GetId(4));
		myHex->GetPointIds()->SetId(2,ptsIds->GetId(10));
		myHex->GetPointIds()->SetId(3,ptsIds->GetId(9));
		myHex->GetPointIds()->SetId(4,ptsIds->GetId(7));
		myHex->GetPointIds()->SetId(5,ptsIds->GetId(11));
		myHex->GetPointIds()->SetId(6,ptsIds->GetId(14));
		myHex->GetPointIds()->SetId(7,ptsIds->GetId(12));
		output->InsertNextCell(myHex->GetCellType(),
				  myHex->GetPointIds());


		myHex->GetPointIds()->SetId(0,ptsIds->GetId(1));
		myHex->GetPointIds()->SetId(1,ptsIds->GetId(5));
		myHex->GetPointIds()->SetId(2,ptsIds->GetId(10));
		myHex->GetPointIds()->SetId(3,ptsIds->GetId(4));
		myHex->GetPointIds()->SetId(4,ptsIds->GetId(8));
		myHex->GetPointIds()->SetId(5,ptsIds->GetId(13));
		myHex->GetPointIds()->SetId(6,ptsIds->GetId(14));
		myHex->GetPointIds()->SetId(7,ptsIds->GetId(11));
		output->InsertNextCell(myHex->GetCellType(),
				       myHex->GetPointIds());


		myHex->GetPointIds()->SetId(0,ptsIds->GetId(2));
		myHex->GetPointIds()->SetId(1,ptsIds->GetId(9));
		myHex->GetPointIds()->SetId(2,ptsIds->GetId(10));
		myHex->GetPointIds()->SetId(3,ptsIds->GetId(5));
		myHex->GetPointIds()->SetId(4,ptsIds->GetId(6));
		myHex->GetPointIds()->SetId(5,ptsIds->GetId(12));
		myHex->GetPointIds()->SetId(6,ptsIds->GetId(14));
		myHex->GetPointIds()->SetId(7,ptsIds->GetId(13));
		output->InsertNextCell(myHex->GetCellType(),
				       myHex->GetPointIds());

	   

		myHex->GetPointIds()->SetId(0,ptsIds->GetId(11));
		myHex->GetPointIds()->SetId(1,ptsIds->GetId(14));
		myHex->GetPointIds()->SetId(2,ptsIds->GetId(12));
		myHex->GetPointIds()->SetId(3,ptsIds->GetId(7));
		myHex->GetPointIds()->SetId(4,ptsIds->GetId(8));
		myHex->GetPointIds()->SetId(5,ptsIds->GetId(13));
		myHex->GetPointIds()->SetId(6,ptsIds->GetId(6));
		myHex->GetPointIds()->SetId(7,ptsIds->GetId(3));
		output->InsertNextCell(myHex->GetCellType(),
				       myHex->GetPointIds());


		myHex->Delete();
		break;
	      }

	    }

	  ptsIds->Delete();

    }
     
    output->SetPoints(outpoints);
    
    
    vtkCellData* cd=output->GetCellData();
    vtkFieldData* pd=(vtkFieldData *) input->GetPointData();

    cd->ShallowCopy(pd);

    return 1;
}

int vtkShowCVs::RequestUpdateExtent(
			  vtkInformation* request,
			  vtkInformationVector** inputVector,
			  vtkInformationVector* outputVector)
 {

  vtkInformation* outInfo=outputVector->GetInformationObject(0);
  vtkInformation *inInfo=inputVector[0]->GetInformationObject(0);


  //  this->DebugOn();

  int piece, numPieces, ghostLevels;
  
  piece=outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_PIECE_NUMBER());
  numPieces=outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_NUMBER_OF_PIECES());
  ghostLevels=outInfo->Get(vtkStreamingDemandDrivenPipeline::UPDATE_NUMBER_OF_GHOST_LEVELS());

  if (numPieces > 1)
  {
    ++ghostLevels;
  }

  vtkDebugMacro(<<"Running Update Extent"<<piece<<numPieces<<ghostLevels);

  inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_PIECE_NUMBER(),piece);
  inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_NUMBER_OF_PIECES(),numPieces);
  inInfo->Set(vtkStreamingDemandDrivenPipeline::UPDATE_NUMBER_OF_GHOST_LEVELS(),ghostLevels);
  inInfo->Set(vtkStreamingDemandDrivenPipeline::EXACT_EXTENT(),1);


  return 1;

};


int vtkShowCVs::FillInputPortInformation(int,vtkInformation *info)
{
  info->Set(vtkAlgorithm::INPUT_REQUIRED_DATA_TYPE(),"vtkUnstructuredGrid");
  return 1;
}
{% endhighlight %}
