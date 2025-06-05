#ifndef CADO_CONFIG_H
#define CADO_CONFIG_H

/* cado_config.h is auto-generated (by cmake) from cado_config_h.in
 * cado_config_h.in is *NOT* auto-generated */

/* we strive to list the cmakedefine's in the order they are created by
 * CMakeLists.txt.
 *
 * Note that some flags are used only in the CMakeLists.txt files. As
 * such, they need not appear here, but we could expose these if need
 * arises. The corresponding names are put in comments below.
 */

#define CFLAGS      "-std=c99 -W -Wall -O2  -msse3 -mssse3 -msse4.1 -mpopcnt -mavx -mpclmul -mavx2"
#define CXXFLAGS    "-export-dynamic -std=c++11 -Wno-c++11-compat -W -Wall -O2  -Wno-literal-suffix -msse3 -mssse3 -msse4.1 -mpopcnt -mavx -mpclmul -mavx2"
#define    ULONG_BITS   64
#define    ULONGLONG_BITS   64

/* #undef CADO_NFS_USE_SHARED_LIBS */

#define HAVE_GDB_PYTHON_PRETTY_PRINT

#define    HAVE_CXX11

/* #undef HAVE_CXX20 */

#define GMP_INCDIR    "/usr/local/include"
#define GMP_LIBDIR    "/usr/local/lib"
#define MPIR_INCDIR    ""
#define MPIR_LIBDIR    ""
/* #undef HAVE_MPIR */

// #define HAVE_KNOWN_GMP_RANDOM_BEHAVIOUR

#define    HAVE_MMX

#define    HAVE_SSE2

#define    HAVE_SSE3

#define    HAVE_SSSE3

#define    HAVE_SSE41

#define    HAVE_AVX

#define    HAVE_AVX2

/* #undef HAVE_AVX512F */

/* #undef HAVE_AVX512VL */

/* #undef HAVE_AVX512DQ */

#define    HAVE_PCLMUL

/* #undef HAVE_ARM_NEON */

#define    HAVE_GCC_STYLE_AMD64_INLINE_ASM
/* #undef HAVE_GCC_STYLE_ARM_INLINE_ASM */

/* #undef VOLATILE_IF_GCC_UBUNTU_BUG */
/* #undef VOLATILE_IF_GCC_58805_BUG */

#define HAVE_GAS_SYNTAX_ASSEMBLY_SOURCES

#define HAVE_EXECINFO

/* #undef STATIC_ANALYSIS */

#define HAVE_GLIBC
/* #undef HAVE_MUSL */
/* #undef MUSL_VERSION */

/* #undef HAVE_CURL */

#define    HAVE_CABSL
#define    HAVE_LOG2
#define    HAVE_CLOG
#define    HAVE_EXP2

#define    HAVE_STDCPP_MATH_SPEC_FUNCS

#define    HAVE_RESOURCE_H
#define    HAVE_UTSNAME_H
#define    HAVE_STATVFS_H
#define    HAVE_WAIT_H
#define    HAVE_LIBGEN_H
#define    HAVE_SYS_MMAN_H

#define    HAVE_SIGHUP
#define    HAVE_POSIX_MEMALIGN
#define    HAVE_ALIGNAS
#define    HAVE_NANOSLEEP
#define    HAVE_USLEEP
#define    HAVE_POPEN
#define    HAVE_PCLOSE
#define    HAVE_GETRUSAGE
/* #undef HAVE_LRAND48 */
#define    HAVE_STRDUP
#define    HAVE_STRNDUP
#define    HAVE_STRNLEN
// #define HAVE_SIGACTION
#define    HAVE_WAITPID
#define    HAVE_CTIME_R
#define    HAVE_REALPATH
#define    HAVE_MMAP
#define    HAVE_SYSCONF

#define    HAVE_RUSAGE_THREAD
#define    HAVE_CLOCK_MONOTONIC
#define    HAVE_CLOCK_MONOTONIC_RAW
#define    HAVE_CLOCK_THREAD_CPUTIME_ID

#define    HAVE_SYNC_FETCH

#define    HAVE_ASPRINTF

#define    HAVE_USUAL_SRAND_DETERMINISTIC_BEHAVIOR
/* #undef HAVE_SRAND_DETERMINISTIC */

#define    HAVE_STRLCPY
#define    HAVE_STRLCAT

#define    HAVE_LINUX_BINFMTS_H

/* #undef HAVE_HWLOC */

#define    HAVE_GMPECM

#define    HAVE_CXXABI_H

#define    HAVE_REGEX_H

#define    HAVE_PTHREAD_BARRIER_WAIT
/* In the C source files, we may of course check MPI_VERSION and
 * MPI_SUBVERSION by ourselves. However we would like to possibly
 * dismiss, on the per-implementation basis, the claim of MPI-3 support.
 */
/* #undef HAVE_MPI2_API */
/* #undef HAVE_MPI3_API */
#define    HAVE_OPENMP

/* #undef HAVE_MINGW */
/* #undef HAVE_EXECUTABLE_SUFFIX */
#ifdef HAVE_EXECUTABLE_SUFFIX
#define EXECUTABLE_SUFFIX ""
#endif

/* #undef HAVE_M4RI */
/* #undef HAVE_M4RIE */

/* #undef HAVE_JEVENTS */

#define    HAVE_INT128

#define    HAVE_ALIGNED_ALLOC

/* #undef HAVE_SYS_ENDIAN_H */

/* #undef HAVE_BSWAP32_IN_SYS_ENDIAN_H */

#define    UINT64_T_IS_EXACTLY_UNSIGNED_LONG
/* #undef UINT64_T_IS_EXACTLY_UNSIGNED_LONG_LONG */
#define    INT64_T_IS_EXACTLY_LONG
/* #undef INT64_T_IS_EXACTLY_LONG_LONG */
/* #undef UINT32_T_IS_EXACTLY_UNSIGNED_LONG */
#define    UINT32_T_IS_EXACTLY_UNSIGNED
/* #undef INT32_T_IS_EXACTLY_LONG */
#define    INT32_T_IS_EXACTLY_INT
#define    MP_LIMB_T_IS_EXACTLY_UNSIGNED_LONG
/* #undef MP_LIMB_T_IS_EXACTLY_UNSIGNED_LONG_LONG */
/* #undef MP_SIZE_T_IS_EXACTLY_LONG_LONG */
#define    MP_SIZE_T_IS_EXACTLY_LONG
/* #undef MP_SIZE_T_IS_EXACTLY_INT */
/* #undef MPZ_INTERNAL_SIZE_T_IS_EXACTLY_LONG_LONG */
/* #undef MPZ_INTERNAL_SIZE_T_IS_EXACTLY_LONG */
#define    MPZ_INTERNAL_SIZE_T_IS_EXACTLY_INT
/* #undef UNSIGNED_LONG_LONG_IS_EXACTLY_UNSIGNED_LONG */
/* #undef UNSIGNED_LONG_IS_EXACTLY_UNSIGNED */
/* #undef LONG_LONG_IS_EXACTLY_LONG */
/* #undef LONG_IS_EXACTLY_INT */

/* #undef UINT64_T_IS_COMPATIBLE_WITH_UNSIGNED_LONG */
#define    UINT64_T_IS_COMPATIBLE_WITH_UNSIGNED_LONG_LONG
/* #undef INT64_T_IS_COMPATIBLE_WITH_LONG */
#define    INT64_T_IS_COMPATIBLE_WITH_LONG_LONG
/* #undef UINT32_T_IS_COMPATIBLE_WITH_UNSIGNED_LONG */
/* #undef UINT32_T_IS_COMPATIBLE_WITH_UNSIGNED */
/* #undef INT32_T_IS_COMPATIBLE_WITH_LONG */
/* #undef INT32_T_IS_COMPATIBLE_WITH_INT */
/* #undef MP_LIMB_T_IS_COMPATIBLE_WITH_UNSIGNED_LONG */
#define    MP_LIMB_T_IS_COMPATIBLE_WITH_UNSIGNED_LONG_LONG
#define    MP_SIZE_T_IS_COMPATIBLE_WITH_LONG_LONG
/* #undef MP_SIZE_T_IS_COMPATIBLE_WITH_LONG */
/* #undef MP_SIZE_T_IS_COMPATIBLE_WITH_INT */
/* #undef MPZ_INTERNAL_SIZE_T_IS_COMPATIBLE_WITH_LONG_LONG */
/* #undef MPZ_INTERNAL_SIZE_T_IS_COMPATIBLE_WITH_LONG */
/* #undef MPZ_INTERNAL_SIZE_T_IS_COMPATIBLE_WITH_INT */

#define CADO_MPI_SIZE_T    MPI_UNSIGNED_LONG
#define CADO_MPI_SSIZE_T   MPI_LONG
#define CADO_MPI_UINT32_T  MPI_UNSIGNED
#define CADO_MPI_UINT64_T  MPI_UNSIGNED_LONG
#define CADO_MPI_INT32_T   MPI_INT
#define CADO_MPI_INT64_T   MPI_LONG
#define CADO_MPI_MP_LIMB_T   MPI_UNSIGNED_LONG
#define CADO_MPI_MP_SIZE_T   MPI_LONG_LONG
#define CADO_MPI_MPZ_INTERNAL_SIZE_T   MPI_INT

/* see also select_mpi.h for c++ templates meant to help in determining mpi type tags */

/* vim:set ft=c: */
#endif  /* CADO_CONFIG_H */
