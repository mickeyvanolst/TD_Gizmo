anchor = op('base/anchor')
anchor_master = op('base/anchor_master')
anchor_scale = op('base/anchor_scale')
anchor_out = op('base/anchor_out')

tx = anchor.op('tx/sop')
ty = anchor.op('ty/sop')
tz = anchor.op('tz/sop')

txy = anchor.op('tx/plane/sop')
tzy = anchor.op('ty/plane/sop')
tzx = anchor.op('tz/plane/sop')

rx = anchor.op('rx/sop')
ry = anchor.op('ry/sop')
rz = anchor.op('rz/sop')

sx = anchor.op('sx/sop')
sy = anchor.op('sy/sop')
sz = anchor.op('sz/sop')

sxy = anchor.op('sx/plane/sop')
szy = anchor.op('sy/plane/sop')
szx = anchor.op('sz/plane/sop')

def intersect_ray_plane(camera_transform, camera_dir, camera_projection_inverse, plane_transform):
	# Extract camera position and direction from camera transformation matrix
	camera_pos = tdu.Vector(camera_transform[0, 3], camera_transform[1, 3], camera_transform[2, 3])
	
	# Extract plane normal from plane transformation matrix
	plane_normal = tdu.Vector(plane_transform[0, 2], plane_transform[1, 2], plane_transform[2, 2])  # Assuming the normal of the plane is along its Z axis
	
	# Extract a point on the plane from plane transformation matrix
	plane_point = tdu.Vector(plane_transform[0, 3], plane_transform[1, 3], plane_transform[2, 3])

	# Calculate intersection point
	intersection_point = intersect_ray_plane_vectors(camera_pos, camera_dir, plane_normal, plane_point)
	return intersection_point

def intersect_ray_plane_vectors(camera_pos, camera_dir, plane_normal, plane_point):
	# Calculate plane equation parameters
	A, B, C = plane_normal
	x0, y0, z0 = plane_point
	
	# Calculate parameter t
	t = -((A * camera_pos.x + B * camera_pos.y + C * camera_pos.z - (A * x0 + B * y0 + C * z0)) /
	      (A * camera_dir.x + B * camera_dir.y + C * camera_dir.z))
	
	# Calculate intersection point
	intersection_point = camera_pos + t * camera_dir
	return intersection_point	

#def onExampleCallback(Event, PrevEvent, interactionEngine, geoCOMP):
#	return

def DoubleClick(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def Click(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def RightClick(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def SelectEnd( Event, PrevEvent, interactionEngine, geoCOMP):
	for PrevEvent.PickSop in [tx, ty, tz, sx, sy, sz, rx, ry, rz]:
		setDragging(PrevEvent.PickSop, False)
	for PrevEvent.PickSop in [txy, tzy, tzx, sxy, szy, szx]:
		setDragging(PrevEvent.PickSop.parent(), False)
	pass

def SelectStart( Event, PrevEvent, interactionEngine, geoCOMP):

	render_w = op(anchor.par.Target.eval().par.Rendertop).width
	render_h = op(anchor.par.Target.eval().par.Rendertop).height
		
	cam_wtf = anchor.par.Target.eval().par.Cameracomp.eval().worldTransform
	cam_pi = anchor.par.Target.eval().par.Cameracomp.eval().projectionInverse(render_w, render_h)
	
	u = anchor.par.Target.eval().par.Panelcomp.eval().panel.insideu
	v = anchor.par.Target.eval().par.Panelcomp.eval().panel.insidev
	remappedU     = tdu.remap( u, 0, 1, -1, 1)
	remappedV     = tdu.remap( v, 0, 1, -1, 1)
	pointNear     = cam_pi * tdu.Position(remappedU, remappedV, -1)
	pointFar      = cam_pi * tdu.Position(remappedU, remappedV, 1)
	dir           = cam_wtf * tdu.Vector( pointFar - pointNear )
	
	x_wtf = tx.parent().worldTransform
	y_wtf = ty.parent().worldTransform
	z_wtf = tz.parent().worldTransform

	intersection_point_plane_x = intersect_ray_plane(cam_wtf, dir, cam_pi, x_wtf)
	intersection_point_plane_y = intersect_ray_plane(cam_wtf, dir, cam_pi, y_wtf)
	intersection_point_plane_z = intersect_ray_plane(cam_wtf, dir, cam_pi, z_wtf)

	parent.gizmo.SelectStartAxisXPos = intersection_point_plane_x
	parent.gizmo.SelectStartAxisYPos = intersection_point_plane_y
	parent.gizmo.SelectStartAxisZPos = intersection_point_plane_z

	parent.gizmo.SelectStartGizmoPos = tdu.Position(anchor.worldTransform.decompose()[2][0], anchor.worldTransform.decompose()[2][1], anchor.worldTransform.decompose()[2][2])

	if Event.PickSop in [tx, ty, tz, sx, sy, sz, rx, ry, rz]:
		setDragging(Event.PickSop, True)
	pass

def Moving(Event:"InteractionEvent", PrevEvent, interactionEngine:"extInteractionFramework", geoCOMP):	
	render_w = op(anchor.par.Target.eval().par.Rendertop).width
	render_h = op(anchor.par.Target.eval().par.Rendertop).height
		
	cam_wtf = anchor.par.Target.eval().par.Cameracomp.eval().worldTransform
	cam_pi = anchor.par.Target.eval().par.Cameracomp.eval().projectionInverse(render_w, render_h)
	
	u = anchor.par.Target.eval().par.Panelcomp.eval().panel.insideu
	v = anchor.par.Target.eval().par.Panelcomp.eval().panel.insidev
	remappedU     = tdu.remap( u, 0, 1, -1, 1)
	remappedV     = tdu.remap( v, 0, 1, -1, 1)
	pointNear     = cam_pi * tdu.Position(remappedU, remappedV, -1)
	pointFar      = cam_pi * tdu.Position(remappedU, remappedV, 1)
	dir           = cam_wtf * tdu.Vector( pointFar - pointNear )
	
	#debug(interactionEngine.SelectStartEvent.PickSop)
	#off_x = interactionEngine.SelectStartEvent.WorldSpaceProjection.x - (gizmo_master.worldTransform  * tdu.Position( 0,0,0 )).x
	#off_y = interactionEngine.SelectStartEvent.WorldSpaceProjection.y - (gizmo_master.worldTransform  * tdu.Position( 0,0,0 )).y
	#off_z = interactionEngine.SelectStartEvent.WorldSpaceProjection.z - (gizmo_master.worldTransform  * tdu.Position( 0,0,0 )).z
	
	x_wtf = tx.parent().worldTransform
	y_wtf = ty.parent().worldTransform
	z_wtf = tz.parent().worldTransform
	intersection_point_plane_x = intersect_ray_plane(cam_wtf, dir, cam_pi, x_wtf)
	intersection_point_plane_y = intersect_ray_plane(cam_wtf, dir, cam_pi, y_wtf)
	intersection_point_plane_z = intersect_ray_plane(cam_wtf, dir, cam_pi, z_wtf)
	
	#debug(interactionEngine.SelectStartEvent.WorldSpaceProjection)

	#s, r, t = anchor_master.worldTransform.decompose()
	#mt = tdu.Position(t)

	ofsx:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisXPos 
	ofsy:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisYPos 
	ofsz:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisZPos 
	if interactionEngine.SelectStartEvent.PickSop == tx:
		anchor.par.tx = (intersection_point_plane_x.x) + ofsx.x
		anchor.par.ty = (intersection_point_plane_x.y) + ofsx.y
		anchor.par.tz = (intersection_point_plane_x.z) + ofsx.z
	if interactionEngine.SelectStartEvent.PickSop == ty:
		anchor.par.ty = (intersection_point_plane_y.y) + ofsy.y
	if interactionEngine.SelectStartEvent.PickSop == tz:
		anchor.par.tz = (intersection_point_plane_z.z) + ofsz.z
	if interactionEngine.SelectStartEvent.PickSop == txy:
		anchor.par.tx = (intersection_point_plane_x.x) + ofsx.x
		anchor.par.ty = (intersection_point_plane_y.y) + ofsy.y
	if interactionEngine.SelectStartEvent.PickSop == tzy:
		anchor.par.tz = (intersection_point_plane_z.z) + ofsz.z
		anchor.par.ty = (intersection_point_plane_y.y) + ofsy.y
	if interactionEngine.SelectStartEvent.PickSop == tzx:
		anchor.par.tz = (intersection_point_plane_z.z) + ofsz.z
		anchor.par.tx = (intersection_point_plane_x.x) + ofsx.x
	
	if interactionEngine.SelectStartEvent.PickSop == rx:
		anchor.par.ry += (parent.gizmo.SelectStartAxisXPos.x - intersection_point_plane_x.x) * 0.2#remappedU#intersection_point_plane_x.x
	if interactionEngine.SelectStartEvent.PickSop == ry:
		anchor.par.rz -= (parent.gizmo.SelectStartAxisYPos.z - intersection_point_plane_y.y) * 0.2#remappedU#intersection_point_plane_y.y
	if interactionEngine.SelectStartEvent.PickSop == rz:
		anchor.par.rx -= (parent.gizmo.SelectStartAxisZPos.x - intersection_point_plane_z.z) * 0.2#remappedV#intersection_point_plane_z.z
	
	if interactionEngine.SelectStartEvent.PickSop == sx:
		anchor_scale.par.sx = intersection_point_plane_x.x
	if interactionEngine.SelectStartEvent.PickSop == sy:
		anchor_scale.par.sy = intersection_point_plane_y.y
	if interactionEngine.SelectStartEvent.PickSop == sz:
		anchor_scale.par.sz = intersection_point_plane_z.z
	
	#parent.gizmo.setPreTransform(anchor_out.worldTransform)
		

def DropOn(Event, PrevEvent, interactionEngine, geoCOMP):
	#Event.HoverComp.par.material.val = Event.SelectedComp.par.material.eval()
	return

def setDragging( targetOp, state):
	targetOp.parent().par.Gizmodragging = state

def setHover( targetOp, state ):
	targetOp.parent().par.Hover = state

def HoverStart( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework", geoCOMP):
	if Event.PickSop in [tx, ty, tz, txy, tzy, tzx, sx, sy, sz, sxy, szy, szx, rx, ry, rz]:
		setHover(Event.PickSop, True)
	return
	
def HoverEnd( Event:"InteractionEvent", PrevEvent:"InteractionEvent", interactionEngine:"extInteractionFramework", geoCOMP):
	if PrevEvent.PickSop in [tx, ty, tz, txy, tzy, tzx, sx, sy, sz, sxy, szy, szx, rx, ry, rz]:
		setHover(PrevEvent.PickSop, False)
	return
	
	
	