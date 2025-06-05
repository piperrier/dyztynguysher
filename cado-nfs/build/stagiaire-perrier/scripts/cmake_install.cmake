# Install script for directory: /home/pperrier/Documents/block_wiedemann/cado-nfs/scripts

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pperrier/Documents/block_wiedemann/cado-nfs/installed")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadocommand.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadologger.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadoparams.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadoprograms.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadotask.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/patterns.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/workunit.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/toplevel.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/wudb.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/api_server.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/cadofactor_tools" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadofactor_tools/__init__.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/cadofactor_tools" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadofactor_tools/certificate.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/cadofactor_tools" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/cadofactor_tools/upload_dir.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/__init__.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/access.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/base.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/dictdb.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/factory.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/misc.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/mysql.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/sqlite3.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/cadofactor/database" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/cadofactor/database/table.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/__main__.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/__init__.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_helper_asyncio.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_helper_fallback.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_lower_class.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_middle_class.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_upper_class.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/descent_utils.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/general_class.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/ideals_above_p.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts/descent" TYPE FILE FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent/log_base.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cado-nfs-3.0.0/scripts" TYPE PROGRAM FILES "/home/pperrier/Documents/block_wiedemann/cado-nfs/scripts/descent.py")
endif()

