# Copyright (c) 2012-2016 DreamWorks Animation LLC
#
# All rights reserved. This software is distributed under the
# Mozilla Public License 2.0 ( http://www.mozilla.org/MPL/2.0/ )
#
# Redistributions of source code must retain the above copyright
# and license notice and the following restrictions and disclaimer.
#
# *     Neither the name of DreamWorks Animation nor the names of
# its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# IN NO EVENT SHALL THE COPYRIGHT HOLDERS' AND CONTRIBUTORS' AGGREGATE
# LIABILITY FOR ALL CLAIMS REGARDLESS OF THEIR BASIS EXCEED US$250.00.
#

#-*-cmake-*-
# - Find ILMBase
#
# Author : Nicholas Yue yue.nicholas@gmail.com
#
# This auxiliary CMake file helps in find the ILMBASE headers and libraries
#
# ILMBASE_FOUND                  set if ILMBASE is found.
# ILMBASE_INCLUDE_DIR            ILMBASE's include directory
# ILMBASE_LIBRARYDIR            ILMBASE's include directory
# Ilmbase_HALF_LIBRARY           ILMBASE's Half libraries
# Ilmbase_IEX_LIBRARY            ILMBASE's Iex libraries
# Ilmbase_IEXMATH_LIBRARY        ILMBASE's IexMath libraries
# Ilmbase_ILMTHREAD_LIBRARY      ILMBASE's IlmThread libraries
# Ilmbase_IMATH_LIBRARY          ILMBASE's Imath libraries

FIND_PACKAGE ( PackageHandleStandardArgs )

FIND_PATH ( ILMBASE_LOCATION include/OpenEXR/IlmBaseConfig.h
  "$ENV{ILMBASE_ROOT}"
  ${ILMBASE_ROOT}
  NO_DEFAULT_PATH
  NO_SYSTEM_ENVIRONMENT_PATH
  )

FIND_PACKAGE_HANDLE_STANDARD_ARGS ( ILMBase
  REQUIRED_VARS ILMBASE_LOCATION
  )

OPTION ( ILMBASE_NAMESPACE_VERSIONING "Namespace versioning of libraries" ON )

IF ( ILMBASE_FOUND )

  FILE ( STRINGS "${ILMBASE_LOCATION}/include/OpenEXR/IlmBaseConfig.h" _ilmbase_version_major_string REGEX "#define ILMBASE_VERSION_MAJOR ")
  STRING ( REGEX REPLACE "#define ILMBASE_VERSION_MAJOR" "" _ilmbase_version_major_unstrip "${_ilmbase_version_major_string}")
  STRING ( STRIP ${_ilmbase_version_major_unstrip} ILMBASE_VERSION_MAJOR )

  FILE ( STRINGS "${ILMBASE_LOCATION}/include/OpenEXR/IlmBaseConfig.h" _ilmbase_version_minor_string REGEX "#define ILMBASE_VERSION_MINOR ")
  STRING ( REGEX REPLACE "#define ILMBASE_VERSION_MINOR" "" _ilmbase_version_minor_unstrip "${_ilmbase_version_minor_string}")
  STRING ( STRIP ${_ilmbase_version_minor_unstrip} ILMBASE_VERSION_MINOR )

  IF ( ILMBASE_NAMESPACE_VERSIONING )
	SET ( IEX_LIBRARY_NAME       Iex-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}       )
	SET ( IEXMATH_LIBRARY_NAME   IexMath-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}   )
	SET ( ILMTHREAD_LIBRARY_NAME IlmThread-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR} )
	SET ( IMATH_LIBRARY_NAME     Imath-${ILMBASE_VERSION_MAJOR}_${ILMBASE_VERSION_MINOR}     )
  ELSE ( ILMBASE_NAMESPACE_VERSIONING )
	SET ( IEX_LIBRARY_NAME       Iex       )
	SET ( IEXMATH_LIBRARY_NAME   IexMath   )
	SET ( ILMTHREAD_LIBRARY_NAME IlmThread )
	SET ( IMATH_LIBRARY_NAME     Imath     )
  ENDIF ( ILMBASE_NAMESPACE_VERSIONING )

  SET ( ILMBASE_INCLUDE_DIRS
    ${ILMBASE_LOCATION}/include
    ${ILMBASE_LOCATION}/include/OpenEXR
    CACHE STRING "ILMBase include directories")
  SET ( ILMBASE_LIBRARYDIR ${ILMBASE_LOCATION}/lib
    CACHE STRING "ILMBase library directories")
  SET ( ILMBASE_FOUND TRUE )
  
  SET ( ORIGINAL_CMAKE_FIND_LIBRARY_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})
  IF (Ilmbase_USE_STATIC_LIBS)
    IF (APPLE)
      SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY Iex PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY IlmThread PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY Imath PATHS ${ILMBASE_LIBRARYDIR} )
    ELSEIF (WIN32)
      # Link library
      SET(CMAKE_FIND_LIBRARY_SUFFIXES ".lib")
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half_static PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY Iex_static PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY IlmThread_static PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY Imath_static PATHS ${ILMBASE_LIBRARYDIR} )
    ELSE (APPLE)
      SET ( CMAKE_FIND_LIBRARY_SUFFIXES ".a")
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
		)
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY Iex PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
		)
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY IlmThread PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
		)
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY Imath PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
		)
    ENDIF (APPLE)
  ELSE (Ilmbase_USE_STATIC_LIBS)
    IF (APPLE)
      SET(CMAKE_FIND_LIBRARY_SUFFIXES ".dylib")
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY Iex PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY IlmThread PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY Imath PATHS ${ILMBASE_LIBRARYDIR} )
    ELSEIF (WIN32)
      # Link library
      SET(CMAKE_FIND_LIBRARY_SUFFIXES ".lib")
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY ${IEX_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IEXMATH_LIBRARY ${IEXMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY ${ILMTHREAD_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY ${IMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR} )
      # Load library
      SET(CMAKE_FIND_LIBRARY_SUFFIXES ".dll")
      FIND_LIBRARY ( Ilmbase_HALF_DLL Half PATHS ${ILMBASE_LOCATION}/bin
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IEX_DLL ${IEX_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IEXMATH_DLL ${IEXMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_DLL ${ILMTHREAD_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IMATH_DLL ${IMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
    ELSE (APPLE)
      FIND_LIBRARY ( Ilmbase_HALF_LIBRARY Half PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IEX_LIBRARY ${IEX_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IEXMATH_LIBRARY ${IEXMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_ILMTHREAD_LIBRARY ${ILMTHREAD_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
      FIND_LIBRARY ( Ilmbase_IMATH_LIBRARY ${IMATH_LIBRARY_NAME} PATHS ${ILMBASE_LIBRARYDIR}
		NO_DEFAULT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
        )
    ENDIF (APPLE)
  ENDIF ()
  # MUST reset
  SET(CMAKE_FIND_LIBRARY_SUFFIXES ${ORIGINAL_CMAKE_FIND_LIBRARY_SUFFIXES})

ELSE ( ILMBASE_FOUND )
  MESSAGE ( FATAL_ERROR "Unable to find ILMBase, ILMBASE_ROOT = $ENV{ILMBASE_ROOT}")
ENDIF ( ILMBASE_FOUND )
