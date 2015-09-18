##########################################################################
#
#  Copyright (c) 2015, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import os
import glob
import shutil
import unittest

import IECore

import Gaffer
import GafferTest

class WedgeTest( GafferTest.TestCase ) :

	def __dispatcher( self, frameRange = None ) :

		result = Gaffer.LocalDispatcher()
		result["jobsDirectory"].setValue( "/tmp/gafferWedgeTest/jobs" )

		if frameRange is not None :
			result["framesMode"].setValue( result.FramesMode.CustomRange )
			result["frameRange"].setValue( frameRange )

		return result

	def testStringList( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${name}.txt" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["variable"].setValue( "name" )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.StringList ) )
		script["wedge"]["strings"].setValue( IECore.StringVectorData( [ "tom", "dick", "harry" ] ) )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/tom.txt",
				"/tmp/gafferWedgeTest/dick.txt",
				"/tmp/gafferWedgeTest/harry.txt",
			}
		)

	def testIntList( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:value}.txt" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.IntList ) )
		script["wedge"]["ints"].setValue( IECore.IntVectorData( [ 1, 21, 44 ] ) )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/1.txt",
				"/tmp/gafferWedgeTest/21.txt",
				"/tmp/gafferWedgeTest/44.txt",
			}
		)

	def testFloatList( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:index}.txt" )
		script["writer"]["text"].setValue( "${wedge:value}" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.FloatList ) )
		script["wedge"]["floats"].setValue( IECore.FloatVectorData( [ 1.25, 2.75, 44.0 ] ) )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/0.txt",
				"/tmp/gafferWedgeTest/1.txt",
				"/tmp/gafferWedgeTest/2.txt",
			}
		)

		self.assertEqual( next( open( "/tmp/gafferWedgeTest/0.txt" ) ), "1.25" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/1.txt" ) ), "2.75" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/2.txt" ) ), "44" )

	def testIntRange( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${number}.txt" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["variable"].setValue( "number" )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.IntRange ) )
		script["wedge"]["intMin"].setValue( 3 )
		script["wedge"]["intMax"].setValue( 7 )
		script["wedge"]["intStep"].setValue( 2 )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/3.txt",
				"/tmp/gafferWedgeTest/5.txt",
				"/tmp/gafferWedgeTest/7.txt",
			}
		)

	def testFloatRange( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:index}.txt" )
		script["writer"]["text"].setValue( "${wedge:value}" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.FloatRange ) )
		script["wedge"]["floatMin"].setValue( 0 )
		script["wedge"]["floatMax"].setValue( 1 )
		script["wedge"]["floatSteps"].setValue( 5 )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/0.txt",
				"/tmp/gafferWedgeTest/1.txt",
				"/tmp/gafferWedgeTest/2.txt",
				"/tmp/gafferWedgeTest/3.txt",
				"/tmp/gafferWedgeTest/4.txt",
			}
		)

		self.assertEqual( next( open( "/tmp/gafferWedgeTest/0.txt" ) ), "0" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/1.txt" ) ), "0.25" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/2.txt" ) ), "0.5" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/3.txt" ) ), "0.75" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/4.txt" ) ), "1" )

	def testFloatByPointOne( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:index}.txt" )
		script["writer"]["text"].setValue( "${wedge:value}" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.FloatRange ) )
		script["wedge"]["floatMin"].setValue( 0 )
		script["wedge"]["floatMax"].setValue( 1 )
		script["wedge"]["floatSteps"].setValue( 11 )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/0.txt",
				"/tmp/gafferWedgeTest/1.txt",
				"/tmp/gafferWedgeTest/2.txt",
				"/tmp/gafferWedgeTest/3.txt",
				"/tmp/gafferWedgeTest/4.txt",
				"/tmp/gafferWedgeTest/5.txt",
				"/tmp/gafferWedgeTest/6.txt",
				"/tmp/gafferWedgeTest/7.txt",
				"/tmp/gafferWedgeTest/8.txt",
				"/tmp/gafferWedgeTest/9.txt",
				"/tmp/gafferWedgeTest/10.txt",
			}
		)

		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/0.txt" ) ) ), 0 )
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/1.txt" ) ) ), 0.1 )
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/2.txt" ) ) ), 0.2 )
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/3.txt" ) ) ), 0.3 )
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/4.txt" ) ) ), 0.4 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/5.txt" ) ) ), 0.5 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/6.txt" ) ) ), 0.6 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/7.txt" ) ) ), 0.7 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/8.txt" ) ) ), 0.8 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/9.txt" ) ) ), 0.9 )	
		self.assertAlmostEqual( float( next( open( "/tmp/gafferWedgeTest/10.txt" ) ) ), 1 )	

	def testColorRange( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:index}.txt" )

		script["expression"] = Gaffer.Expression()
		script["expression"].setExpression( 'c = context["wedge:value"]; parent["writer"]["text"] = "%.1f %.1f %.1f" % ( c[0], c[1], c[2] )' )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.ColorRange ) )
		script["wedge"]["colorSteps"].setValue( 3 )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/0.txt",
				"/tmp/gafferWedgeTest/1.txt",
				"/tmp/gafferWedgeTest/2.txt",
			}
		)

		self.assertEqual( next( open( "/tmp/gafferWedgeTest/0.txt" ) ), "0.0 0.0 0.0" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/1.txt" ) ), "0.5 0.5 0.5" )
		self.assertEqual( next( open( "/tmp/gafferWedgeTest/2.txt" ) ), "1.0 1.0 1.0" )

	def test2DRange( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${wedge:x}.${wedge:y}.txt" )

		script["wedgeX"] = Gaffer.Wedge()
		script["wedgeX"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedgeX"]["variable"].setValue( "wedge:x" )
		script["wedgeX"]["mode"].setValue( int( Gaffer.Wedge.Mode.IntRange ) )
		script["wedgeX"]["intMin"].setValue( 1 )
		script["wedgeX"]["intMax"].setValue( 3 )
		script["wedgeX"]["intStep"].setValue( 1 )

		script["wedgeY"] = Gaffer.Wedge()
		script["wedgeY"]["requirements"][0].setInput( script["wedgeX"]["requirement"] )
		script["wedgeY"]["variable"].setValue( "wedge:y" )
		script["wedgeY"]["mode"].setValue( int( Gaffer.Wedge.Mode.IntRange ) )
		script["wedgeY"]["intMin"].setValue( 1 )
		script["wedgeY"]["intMax"].setValue( 2 )
		script["wedgeY"]["intStep"].setValue( 1 )

		self.__dispatcher().dispatch( [ script["wedgeY"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/1.1.txt",
				"/tmp/gafferWedgeTest/1.2.txt",
				"/tmp/gafferWedgeTest/2.1.txt",
				"/tmp/gafferWedgeTest/2.2.txt",
				"/tmp/gafferWedgeTest/3.1.txt",
				"/tmp/gafferWedgeTest/3.2.txt",
			}
		)

	def testContext( self ) :

		script = Gaffer.ScriptNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${name}.####.txt" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["variable"].setValue( "name" )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.StringList ) )
		script["wedge"]["strings"].setValue( IECore.StringVectorData( [ "tom", "dick", "harry" ] ) )

		self.__dispatcher( frameRange = "21-22" ).dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/tom.0021.txt",
				"/tmp/gafferWedgeTest/tom.0022.txt",
				"/tmp/gafferWedgeTest/dick.0021.txt",
				"/tmp/gafferWedgeTest/dick.0022.txt",
				"/tmp/gafferWedgeTest/harry.0021.txt",
				"/tmp/gafferWedgeTest/harry.0022.txt",
			}
		)

	def testUpstreamConstant( self ) :

		script = Gaffer.ScriptNode()

		script["constant"] = GafferTest.CountingExecutableNode()

		script["writer"] = GafferTest.TextWriter()
		script["writer"]["requirements"][0].setInput( script["constant"]["requirement"] )
		script["writer"]["fileName"].setValue( "/tmp/gafferWedgeTest/${name}.txt" )

		script["wedge"] = Gaffer.Wedge()
		script["wedge"]["requirements"][0].setInput( script["writer"]["requirement"] )
		script["wedge"]["variable"].setValue( "name" )
		script["wedge"]["mode"].setValue( int( Gaffer.Wedge.Mode.StringList ) )
		script["wedge"]["strings"].setValue( IECore.StringVectorData( [ "tom", "dick", "harry" ] ) )

		self.__dispatcher().dispatch( [ script["wedge"] ] )

		self.assertEqual(
			set( glob.glob( "/tmp/gafferWedgeTest/*.txt" ) ),
			{
				"/tmp/gafferWedgeTest/tom.txt",
				"/tmp/gafferWedgeTest/dick.txt",
				"/tmp/gafferWedgeTest/harry.txt",
			}
		)

		# Even though the constant node is upstream from the wedge,
		# it should only execute once because it doesn't reference
		# the wedge variable at all.
		self.assertEqual( script["constant"].executionCount, 1 )

	def tearDown( self ) :

		GafferTest.TestCase.tearDown( self )

		if os.path.exists( "/tmp/gafferWedgeTest" ) :
			shutil.rmtree( "/tmp/gafferWedgeTest" )

if __name__ == "__main__":
	unittest.main()
