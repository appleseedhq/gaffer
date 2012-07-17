//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2011-2012, John Haddon. All rights reserved.
//  Copyright (c) 2011-2012, Image Engine Design Inc. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#include "GafferUI/StandardNodule.h"
#include "GafferUI/Style.h"
#include "GafferUI/ConnectionGadget.h"
#include "GafferUI/NodeGadget.h"

#include "Gaffer/Plug.h"
#include "Gaffer/UndoContext.h"
#include "Gaffer/ScriptNode.h"

#include "boost/bind.hpp"
#include "boost/bind/placeholders.hpp"

using namespace GafferUI;
using namespace Imath;
using namespace std;

IE_CORE_DEFINERUNTIMETYPED( StandardNodule );

Nodule::NoduleTypeDescription<StandardNodule> StandardNodule::g_noduleTypeDescription( Gaffer::Plug::staticTypeId() );

StandardNodule::StandardNodule( Gaffer::PlugPtr plug )
	:	Nodule( plug ), m_hovering( false ), m_dragging( false )
{
	enterSignal().connect( boost::bind( &StandardNodule::enter, this, ::_1, ::_2 ) );
	leaveSignal().connect( boost::bind( &StandardNodule::leave, this, ::_1, ::_2 ) );
	buttonPressSignal().connect( boost::bind( &StandardNodule::buttonPress, this, ::_1,  ::_2 ) );
	dragBeginSignal().connect( boost::bind( &StandardNodule::dragBegin, this, ::_1, ::_2 ) );
	dragUpdateSignal().connect( boost::bind( &StandardNodule::dragUpdate, this, ::_1, ::_2 ) );
	dragEnterSignal().connect( boost::bind( &StandardNodule::dragEnter, this, ::_1, ::_2 ) );
	dragLeaveSignal().connect( boost::bind( &StandardNodule::dragLeave, this, ::_1, ::_2 ) );
	dragEndSignal().connect( boost::bind( &StandardNodule::dragEnd, this, ::_1, ::_2 ) );

	dropSignal().connect( boost::bind( &StandardNodule::drop, this, ::_1, ::_2 ) );
}

StandardNodule::~StandardNodule()
{
}

Imath::Box3f StandardNodule::bound() const
{
	return Box3f( V3f( -0.5, -0.5, 0 ), V3f( 0.5, 0.5, 0 ) );
}

void StandardNodule::doRender( const Style *style ) const
{
	if( m_dragging )
	{
		int renderMode = GL_RENDER;
		glGetIntegerv( GL_RENDER_MODE, &renderMode );
		if( renderMode != GL_SELECT )
		{
			V3f srcTangent( 0.0f, 1.0f, 0.0f );
			const NodeGadget *nodeGadget = ancestor<NodeGadget>();
			if( nodeGadget )
			{
				srcTangent = nodeGadget->noduleTangent( this );
			}
			style->renderConnection( V3f( 0 ), srcTangent, m_dragPosition, -srcTangent );
		}
	}
	
	float radius = 0.5f;
	Style::State state = Style::NormalState;
	if( m_hovering )
	{
		state = Style::HighlightedState;
		radius = 1.0f;
	}

	style->renderNodule( radius, state );
}

void StandardNodule::enter( GadgetPtr gadget, const ButtonEvent &event )
{
	m_hovering = true;
	renderRequestSignal()( this );
}

void StandardNodule::leave( GadgetPtr gadget, const ButtonEvent &event )
{
	m_hovering = false;
	renderRequestSignal()( this );
}

bool StandardNodule::buttonPress( GadgetPtr gadget, const ButtonEvent &event )
{
	// we handle the button press so we can get the dragBegin event.
	return true;
}

IECore::RunTimeTypedPtr StandardNodule::dragBegin( GadgetPtr gadget, const ButtonEvent &event )
{
	m_dragging = true;
	m_dragPosition = event.line.p0;
	renderRequestSignal()( this );
	return plug();
}

bool StandardNodule::dragUpdate( GadgetPtr gadget, const DragDropEvent &event )
{
	m_dragPosition = event.line.p0;
	renderRequestSignal()( this );
	return true;
}

bool StandardNodule::dragEnter( GadgetPtr gadget, const DragDropEvent &event )
{
	Gaffer::PlugPtr input, output;
	connection( event, input, output );
	if( input )
	{
		m_hovering = true;
		renderRequestSignal()( this );
	}
	return true;
}

bool StandardNodule::dragLeave( GadgetPtr gadget, const DragDropEvent &event )
{
	if( event.source != this )
	{
		m_hovering = false;
		renderRequestSignal()( this );
	}
	return true;
}

bool StandardNodule::dragEnd( GadgetPtr gadget, const DragDropEvent &event )
{
	m_dragging = false;
	renderRequestSignal()( this );
	return true;
}

bool StandardNodule::drop( GadgetPtr gadget, const DragDropEvent &event )
{
	Gaffer::PlugPtr input, output;
	connection( event, input, output );
	
	if( input )
	{	
		Gaffer::UndoContext undoEnabler( input->ancestor<Gaffer::ScriptNode>() );

			ConnectionGadgetPtr connection = IECore::runTimeCast<ConnectionGadget>( event.source );
			if( connection && plug()->direction()==Gaffer::Plug::In )
			{
				connection->dstNodule()->plug()->setInput( 0 );
			}

			input->setInput( output );
			
		return true;
	}
	return false;
}

void StandardNodule::connection( const DragDropEvent &event, Gaffer::PlugPtr &input, Gaffer::PlugPtr &output )
{	
	Gaffer::PlugPtr dropPlug = IECore::runTimeCast<Gaffer::Plug>( event.data );
	if( dropPlug )
	{
		Gaffer::PlugPtr thisPlug = plug();
		if( thisPlug->direction()!=dropPlug->direction() )
		{
			if( thisPlug->direction()==Gaffer::Plug::In )
			{
				input = thisPlug;
				output = dropPlug;
			}
			else
			{
				input = dropPlug;
				output = thisPlug;
			}
						
			if( input->acceptsInput( output ) )
			{
				// success
				return;
			}
		}
	}

	input = output = 0;
	return;
}

