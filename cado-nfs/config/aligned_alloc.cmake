
# aligned_alloc is c11, but not c++11. It's in c++17
#
# http://en.cppreference.com/w/c/memory/aligned_alloc
# http://en.cppreference.com/w/cpp/memory/c/aligned_alloc
                                                                                
include(CheckCXXSourceCompiles)

set(check_aligned_alloc_code "
#include <stdlib.h>
int main()
{
    return aligned_alloc(64, 1024) != NULL;
}
")

set(CMAKE_REQUIRED_FLAGS)
set(CMAKE_REQUIRED_DEFINITIONS)
set(CMAKE_REQUIRED_INCLUDES)
set(CMAKE_REQUIRED_LIBRARIES)
set(OLD_CMAKE_REQUIRED_QUIET "${CMAKE_REQUIRED_QUIET}")
set(CMAKE_REQUIRED_QUIET 1)
CHECK_CXX_SOURCE_COMPILES("${check_aligned_alloc_code}" HAVE_ALIGNED_ALLOC)
set(CMAKE_REQUIRED_QUIET "${OLD_CMAKE_REQUIRED_QUIET}")
