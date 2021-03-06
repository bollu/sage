ATLAS
=====

Description
-----------

This spkg builds ATLAS for Sage.

License
-------

3-clause BSD


Upstream Contact
----------------

-  Atlas devel mailing list.
-  Clint Whaley has frequently answered questions from the Sage project

Dependencies
------------

-  Python


Special Update/Build Instructions
---------------------------------

-  src/lapack-x.y.z.tgz: The netlib lapack tarball. If you update this,
   make sure you also update the LAPACK_TARBALL variable in
   spkg-install.

-  src/ATLAS-lib: We are using a dummy autotools/libtools project
   to repack the static ATLAS libraries into shared libraries.

-  src/ARCHS: We ship some archdef tarballs to speed ATLAS build.
-  spkg-install: If you update atlas to a new version make sure that the
   ATLAS_OSTYPE, ATLAS_MACHTYPE, and ATLAS_ISAEXT variables in
   spkg-install remain in sync with atlas' CONFIG/include/atlconf.h

-  The package is never installed on OS X, unless you set
   SAGE_ATLAS_ARCH.

Patches
~~~~~~~

-  patches/detect.patch: Fix Itanium2 support on modern
   RHEL 5 and SLES 10 systems, work around -m64 issue on Itanium2,
   and correctly detect number and speed of CPUs on a bunch of systems.

-  patches/arm_hard_floats.patch: make sure soft floats are not enforced
   on ARM.
-  patches/Makefile.patch: fix clean target.
-  patches/do_not_force_mutex.patch: always use assembly over mutex
   since the mutex version fails to build a shared library. See #15045
   for details.

-  patches/glibc_scanf_workaround.patch: Workaround for the scanf bug
   in glibc-2.18 that breaks the atlas auto-tuning system.

Configuration
~~~~~~~~~~~~~

The package can be configured via three environment variables:

-  SAGE_ATLAS_LIB=path

   If this environment variable is set, the libraries libatlas,
   libcblas, liblapack, and libf77blas from the direcory "path" are
   used and ATLAS is not compiled from source. The libraries can be
   either static (endin in .a) or shared libraries (ending in .so or
   .dylib).

-  SAGE_ATLAS_ARCH=arch[,isaext1][,isaext2]...[,isaextN]

   The given architectural default and instruction set extensions are
   used instead of the empirical tuning. Available architectures are

   POWER3, POWER4, POWER5, PPCG4, PPCG5, POWER6, POWER7, IBMz9,
   IBMz10, IBMz196, x86x87, x86SSE1, x86SSE2, x86SSE3, P5, P5MMX,
   PPRO, PII, PIII, PM, CoreSolo, CoreDuo, Core2Solo, Core2, Corei1,
   Corei2, Atom, P4, P4E, Efficeon, K7, HAMMER, AMD64K10h, AMDDOZER,
   UNKNOWNx86, IA64Itan, IA64Itan2, USI, USII, USIII, USIV, UST1, UST2,
   UnknownUS, MIPSR1xK, MIPSICE9, ARMv6, ARMv7

   and instruction set extensions are

   VSX, AltiVec, AVXMAC, AVXFMA4, AVX, SSE3, SSE2, SSE1, 3DNow, NEON

   In addition, you can also set

-  SAGE_ATLAS_ARCH=fast picks defaults for a modern (2-3 year old)
   CPU of your processor line, and

-  SAGE_ATLAS_ARCH=base picks defaults that should work for a ~10
   year old CPU.

   For example,

   SAGE_ATLAS_ARCH=Corei2,AVX,SSE3,SSE2,SSE1

   would be appropriate for a Core i7 CPU.

-  If SAGE_ATLAS_SAVE_ARCHDEF = is given, then a new archdef
   file is created and saved to the given path.
