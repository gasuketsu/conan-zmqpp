project(conanzmqpp)
cmake_minimum_required(VERSION 2.8)
include(${CMAKE_SOURCE_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()

set(ZEROMQ_LIB_DIR ${CONAN_LIB_DIRS_LIBZMQ} CACHE PATH "libzmq path")
include("${CMAKE_SOURCE_DIR}/CMakeListsOriginal.cmake")
