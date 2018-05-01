---
title: Installing Delft3d on an Apple Mac
---

[Delft3d](http://oss.deltares.nl/web/delft3d/home "Delft3d's homepage") is "a world leading 3D modeling suite to investigate hydrodynamics, sediment transport and morphology and water quality for fluvial, estuarine and coastal environments.", available for multiple operating systems. However it can be surprisingly difficult to get it running on OSX.

Based on the recipe [here](http://oss.deltares.nl/web/delft3d/coast-/-estuary/-/message_boards/view_message/1174311) I'll attempt to document a method based on [homebrew]() as a package manager.

First obtain the code. Sign up [here](http://oss.deltares.nl/web/delft3d/get-started) then download the code via svn.

{% highlight bash %}
brew install svn
svn checkout --username <username> https://svn.oss.deltares.nl/repos/delft3d/tags/6686 delft3d
{% endhighlight %}

Next we need to patch a fairly large number of files which I've collected into a patch(see the end of this post).

{% highlight bash %}
cd delft3d/src
patch -p0 -i ~/my_patch.diff
{% endhighlight %}

Now download the relevant dependencies and build the code

{% highlight bash %}
brew install coreutils
brew install autoconf
brew install automake
brew install gcc
brew install netcdf
brew install openmpi
brew install ossp-uuid
brew install libtool

autoconf
LDFLAGS=-L/usr/local/lib NETCDF_FORTRAN_CFLAGS=-I/usr/local/Cellar/netcdf/4.6.0/include ./configure --prefix=$HOME/delft3d
make
make install
{% endhighlight %}

Finally, [here's]({{ site.url }}/files/my_patch.diff) the patch file:

{% highlight bash %}
===================================================================
--- utils_lgpl/deltares_common/packages/deltares_common/src/juldat.f90	(revision 8581)
+++ utils_lgpl/deltares_common/packages/deltares_common/src/juldat.f90	(working copy)
@@ -49,5 +49,6 @@
 !
 !! executable statements -------------------------------------------------------
 !
+
     julday = ymd2jul(itdate)
 end subroutine juldat
Index: utils_lgpl/deltares_common/packages/deltares_common/src/time_module.f90
===================================================================
--- utils_lgpl/deltares_common/packages/deltares_common/src/time_module.f90	(revision 8581)
+++ utils_lgpl/deltares_common/packages/deltares_common/src/time_module.f90	(working copy)
@@ -204,6 +204,7 @@
          year = yyyymmdd/10000
          month = yyyymmdd/100 - year*100
          day = yyyymmdd - month*100 - year*10000
+
          jdn = GregorianYearMonthDayToJulianDateNumber(year, month, day)
       end function GregorianDateToJulianDateNumber
       
@@ -231,6 +232,8 @@
          !
          ! Calculate backwards to test if the assumption is correct
          !
+
+         write(*,fmt="(a)", advance='no') ''
          call jul2ymd(jdn, y, m, d)
          !
          ! Test if calculation is correct
Index: utils_lgpl/io_netcdf/packages/io_netcdf/src/io_netcdf_api.F90
===================================================================
--- utils_lgpl/io_netcdf/packages/io_netcdf/src/io_netcdf_api.F90	(revision 8581)
+++ utils_lgpl/io_netcdf/packages/io_netcdf/src/io_netcdf_api.F90	(working copy)
@@ -466,16 +466,16 @@
  do i = 1, length
     char_array_to_string(i:i) = char_array(i)
  enddo
-end function char_array_to_string
-
-function string_to_char_array(string, length) result(char_array)
-   character(len=length), intent(in) :: string
-   integer, intent(in) :: length
-   character(kind=c_char,len=1) :: char_array(MAXSTRLEN)
-   integer :: i
-   do i = 1, len(string)
-       char_array(i) = string(i:i)
-   enddo
-   char_array(len(string)+1) = C_NULL_CHAR
-end function string_to_char_array
-end module io_netcdf_api
\ No newline at end of file
+end function char_array_to_string
+
+function string_to_char_array(string, length) result(char_array)
+   integer, intent(in) :: length
+   character(len=length), intent(in) :: string
+   character(kind=c_char,len=1) :: char_array(MAXSTRLEN)
+   integer :: i
+   do i = 1, len(string)
+       char_array(i) = string(i:i)
+   enddo
+   char_array(len(string)+1) = C_NULL_CHAR
+end function string_to_char_array
+end module io_netcdf_api
Index: utils_lgpl/nefis/packages/nefis/include/c2c.h
===================================================================
--- utils_lgpl/nefis/packages/nefis/include/c2c.h	(revision 8581)
+++ utils_lgpl/nefis/packages/nefis/include/c2c.h	(working copy)
@@ -32,10 +32,10 @@
 #include "nefis.h"
 #include "nef-tag.h"
 
-BInt4 nefis_errcnt;
-BInt4 nefis_errno;
-BChar error_text[LENGTH_ERROR_MESSAGE+1];
-BInt4 nefis_flush;
+BInt4 extern nefis_errcnt;
+BInt4 extern nefis_errno;
+BChar extern error_text[LENGTH_ERROR_MESSAGE+1];
+BInt4 extern nefis_flush;
 
 BInt4 close_nefis_files    ( BInt4 *);
 BInt4 create_nefis_files   ( BInt4 *, BText  , BText  , BChar  , BChar  );
Index: utils_lgpl/nefis/packages/nefis/include/f2c.h
===================================================================
--- utils_lgpl/nefis/packages/nefis/include/f2c.h	(revision 8581)
+++ utils_lgpl/nefis/packages/nefis/include/f2c.h	(working copy)
@@ -69,8 +69,8 @@
 BInt4 OC_reset_file_version( BInt4, BInt4 );
 BInt4 OC_close_all_nefis_files( void );
 
-BInt4 nefis_flush;
-BInt4 nefis_errcnt;
-BInt4 nefis_errno;
-BChar error_text[LENGTH_ERROR_MESSAGE+1];
+BInt4 extern nefis_flush;
+BInt4 extern nefis_errcnt;
+BInt4 extern nefis_errno;
+BChar extern error_text[LENGTH_ERROR_MESSAGE+1];
 #endif
Index: utils_lgpl/nefis/packages/nefis/src/gp.c
===================================================================
--- utils_lgpl/nefis/packages/nefis/src/gp.c	(revision 8581)
+++ utils_lgpl/nefis/packages/nefis/src/gp.c	(working copy)
@@ -67,7 +67,7 @@
 #  define FILE_WRITE _write
 #elif defined(GNU_PC) || defined(HAVE_CONFIG_H) || defined(salford32)
 #  define FILE_READ  read
-#  define FILE_SEEK  lseek64
+#  define FILE_SEEK  lseek
 #  define FILE_WRITE write
 #elif defined(USE_SUN)
 #  define FILE_READ  read
Index: utils_lgpl/ods/packages/ods/src/jspost.c
===================================================================
--- utils_lgpl/ods/packages/ods/src/jspost.c	(revision 8581)
+++ utils_lgpl/ods/packages/ods/src/jspost.c	(working copy)
@@ -57,7 +57,7 @@
 #include <math.h>
 #include <float.h>
 #include <errno.h>
-#include <malloc.h>
+#include <malloc/malloc.h>
 
 #include "ods.h"
 #include "portable.h"
{% endhighlight %}
