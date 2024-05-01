def onHoverStart( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework"):
	interactionEngine.PushCallback("HoverStart")
	pass

def onHoverEnd( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework" ):
	interactionEngine.PushCallback("HoverEnd", PrevEvent.HoverComp)
	pass

def onHoverMove( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework" ):
	interactionEngine.PushCallback("HoverMove")
	pass

def onSelectStart(Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework" ):
	interactionEngine.PushCallback("SelectStart")
	pass

def onSelectEnd(Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework" ):
	interactionEngine.PushCallback("SelectEnd")
	if Event.HoverComp and Event.HoverComp != Event.SelectedComp:
		interactionEngine.PushCallback("DropOn")
	Event.InteractiveComp.par.Dragging.val = False
	pass

def onMove( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework" ):
	interactionEngine.PushCallback("InteractiveMove")
	distanceVector:tdu.Vector = tdu.Vector( Event.CameraProjection - interactionEngine.SelectStartEvent.CameraProjection )
	#print(distanceVector.length())
	if distanceVector.length() > 0.02 and not Event.InteractiveComp.par.Dragging.eval():
		interactionEngine.ResetClick()
		Event.InteractiveComp.par.Dragging.val = True
		interactionEngine.PushCallback("StartMove")
		
	if not Event.InteractiveComp.par.Dragging.eval(): return 
	interactionEngine.PushCallback("Moving")

def onClick (Event:"InteractionEvent", ClickCount:int, interactionEngine:"extInteractionFramework"):
	if ClickCount == 1 :
		interactionEngine.PushCallback("Click")
		if Event.Button == interactionEngine.Buttons.Right:
			interactionEngine.PushCallback("RightClick")
	if ClickCount == 2 :
		interactionEngine.PushCallback("DoubleClick")
	