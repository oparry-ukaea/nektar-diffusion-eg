CMAKE_MINIMUM_REQUIRED(VERSION 3.5.1)

PROJECT(CoupledBCsSolvers)

# Nektar++ requires C++14.
SET(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(CMAKE_CXX_EXTENSIONS OFF)

# Default install location: build/dist
IF (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    SET(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/dist CACHE PATH "" FORCE)
ENDIF()

# Find Nektar++
FIND_PACKAGE(Nektar++ REQUIRED)
MESSAGE(STATUS "Found Nektar++: version ${NEKTAR++_VERSION}")

# Set RPATH for wherever Nektar++ is installed.
SET(CMAKE_INSTALL_RPATH "${NEKTAR++_LIBRARY_DIRS}" "${NEKTAR++_TP_LIBRARY_DIRS}")

IF(CMAKE_BUILD_TYPE STREQUAL "Debug")
  ADD_DEFINITIONS(-DDEBUG)
ENDIF()

set(COMMON_SRC_FILES
    src/BoundaryConditions/CFSBndCond.cpp
    src/BoundaryConditions/CWIPIBCs.cpp
    )

#==================== ADR Solver ====================
# Source files
set(ADRSOLVER_SRC_FILES
    src/ADRSolver.cpp
    src/UnsteadyDiffusion.cpp
    src/BoundaryConditions/CWIPIBCsReceiver.cpp
    src/BoundaryConditions/FileBasedBCs.cpp 
    ${COMMON_SRC_FILES}
    )

# Target
ADD_EXECUTABLE(ADRSolver ${ADRSOLVER_SRC_FILES})

# Compiler defs, includes, link libraries
TARGET_COMPILE_DEFINITIONS(ADRSolver PUBLIC ${NEKTAR++_DEFINITIONS})
TARGET_INCLUDE_DIRECTORIES(ADRSolver PUBLIC ${NEKTAR++_INCLUDE_DIRS} ${NEKTAR++_TP_INCLUDE_DIRS})
TARGET_LINK_LIBRARIES(ADRSolver ${NEKTAR++_LIBRARIES} ${NEKTAR++_TP_LIBRARIES})

# Install exec
INSTALL(TARGETS ADRSolver DESTINATION ${CMAKE_INSTALL_PREFIX})

#==================== BCProvider ====================
# Source files
set(BCPROVIDER_SRC_FILES
    src/BCProvider/BCProvider.cpp
    src/BCProvider/BCProviderSystem.cpp
    src/BoundaryConditions/CWIPIBCsSender.cpp 
    ${COMMON_SRC_FILES}
    )

# Target
ADD_EXECUTABLE(BCProvider ${BCPROVIDER_SRC_FILES})

# Target compiler defs, includes, link libraries for the BCProvider
TARGET_COMPILE_DEFINITIONS(BCProvider PUBLIC ${NEKTAR++_DEFINITIONS})
TARGET_INCLUDE_DIRECTORIES(BCProvider PUBLIC ${NEKTAR++_INCLUDE_DIRS} ${NEKTAR++_TP_INCLUDE_DIRS})
TARGET_LINK_LIBRARIES(BCProvider ${NEKTAR++_LIBRARIES} ${NEKTAR++_TP_LIBRARIES})

# Install exec
INSTALL(TARGETS BCProvider DESTINATION ${CMAKE_INSTALL_PREFIX})