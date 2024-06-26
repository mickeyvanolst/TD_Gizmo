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

#def onExampleCallback(Event, PrevEvent, interactionEngine, geoCOMP):
#	return

def DoubleClick(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def Click(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def RightClick(Event, PrevEvent, interacitonEngine, geoCOMP):
	pass

def SelectEnd( Event, PrevEvent, interactionEngine, geoCOMP):

	parent.gizmo.par.ptx = anchor.worldTransform.decompose()[2][0]
	parent.gizmo.par.pty = anchor.worldTransform.decompose()[2][1]
	parent.gizmo.par.ptz = anchor.worldTransform.decompose()[2][2]

	parent.gizmo.par.prx = anchor.worldTransform.decompose()[1][0]
	parent.gizmo.par.pry = anchor.worldTransform.decompose()[1][1]
	parent.gizmo.par.prz = anchor.worldTransform.decompose()[1][2]

	#parent.gizmo.setTransform(tdu.Matrix())
	parent.gizmo.par.tx = 0
	parent.gizmo.par.ty = 0
	parent.gizmo.par.tz = 0
	parent.gizmo.par.rx = 0
	parent.gizmo.par.ry = 0
	parent.gizmo.par.rz = 0
	anchor.setTransform(tdu.Matrix())

	for PrevEvent.PickSop in [tx, ty, tz, sx, sy, sz, rx, ry, rz]:
		setDragging(PrevEvent.PickSop, False)
	for PrevEvent.PickSop in [txy, tzy, tzx, sxy, szy, szx]:
		setDragging(PrevEvent.PickSop.parent(), False)
	pass

def SelectStart( Event, PrevEvent, interactionEngine, geoCOMP):
	parent.gizmo.SelectStartAxisXPos = intersection_point_plane_x
	parent.gizmo.SelectStartAxisYPos = intersection_point_plane_y
	parent.gizmo.SelectStartAxisZPos = intersection_point_plane_z

	parent.gizmo.SelectStartGizmoPos = tdu.Position(anchor.worldTransform.decompose()[2][0], anchor.worldTransform.decompose()[2][1], anchor.worldTransform.decompose()[2][2])

	parent.gizmo.SelectStartGizmoRotation = tdu.Vector(parent.gizmo.worldTransform.decompose()[1][0], parent.gizmo.worldTransform.decompose()[1][1], parent.gizmo.worldTransform.decompose()[1][2])
	
	parent.gizmo.SelectStartGizmoScale = tdu.Vector(parent.gizmo.worldTransform.decompose()[0][0], parent.gizmo.worldTransform.decompose()[0][1], parent.gizmo.worldTransform.decompose()[0][2])

	parent.gizmo.SelectStartCursorPos = tdu.Vector(op('panel1')['insideu'], op('panel1')['insidev'], 0)

	if Event.PickSop in [tx, ty, tz, sx, sy, sz, rx, ry, rz]:
		setDragging(Event.PickSop, True)
	pass

def Moving(Event:"InteractionEvent", PrevEvent, interactionEngine:"extInteractionFramework", geoCOMP):	
	s, r, t = anchor_master.worldTransform.decompose()
	mt = tdu.Position(t)

	ofsx:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisXPos 
	ofsy:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisYPos 
	ofsz:tdu.Position = parent.gizmo.SelectStartGizmoPos - parent.gizmo.SelectStartAxisZPos 
	if interactionEngine.SelectStartEvent.PickSop == tx:
		anchor.par.tx = (intersection_point_plane_x.x - mt.x) + ofsx.x
		parent.gizmo.par.tx = anchor.par.tx
	if interactionEngine.SelectStartEvent.PickSop == ty:
		anchor.par.ty = (intersection_point_plane_y.y - mt.y) + ofsy.y
		parent.gizmo.par.ty = anchor.par.ty
	if interactionEngine.SelectStartEvent.PickSop == tz:
		anchor.par.tz = (intersection_point_plane_z.z - mt.z) + ofsz.z
		parent.gizmo.par.tz = anchor.par.tz
	if interactionEngine.SelectStartEvent.PickSop == txy:
		anchor.par.tx = (intersection_point_plane_x.x - mt.x) + ofsx.x
		anchor.par.ty = (intersection_point_plane_y.y - mt.y) + ofsy.y
		parent.gizmo.par.tx = anchor.par.tx
		parent.gizmo.par.ty = anchor.par.ty
	if interactionEngine.SelectStartEvent.PickSop == tzy:
		anchor.par.tz = (intersection_point_plane_z.z - mt.z) + ofsz.z
		anchor.par.ty = (intersection_point_plane_y.y - mt.y) + ofsy.y
		parent.gizmo.par.tz = anchor.par.tz
		parent.gizmo.par.ty = anchor.par.ty
	if interactionEngine.SelectStartEvent.PickSop == tzx:
		anchor.par.tz = (intersection_point_plane_z.z - mt.z) + ofsz.z
		anchor.par.tx = (intersection_point_plane_x.x - mt.x) + ofsx.x
		parent.gizmo.par.tz = anchor.par.tz
		parent.gizmo.par.tx = anchor.par.tx
	

	#cursor_cur = tdu.Vector(op('panel1')['insideu'], op('panel1')['insidev'], 0)
	cursor_start = parent.gizmo.SelectStartCursorPos
	print(cursor_start)

	if interactionEngine.SelectStartEvent.PickSop == rx:
		v = (parent.gizmo.SelectStartAxisXPos.x - intersection_point_plane_x.x) * 0.2
		v = max(-2, min(v, 2))
		anchor.par.ry += v #remappedU#intersection_point_plane_x.x
		#anchor.par.ry = parent.gizmo.SelectSTartGizmoRotation.y + tdu.Vector(parent.gizmo.SelectStartGizmoPos.x + ofsx.x, parent.gizmo.SelectStartGizmoPos.y + ofsx.y, parent.gizmo.SelectStartGizmoPos.z + ofsx.z).distance(tdu.Vector(intersection_point_plane_y.x, intersection_point_plane_y.y, intersection_point_plane_y.z))# ((intersection_point_plane_y.y -mt.y) + ofsy.y)
		parent.gizmo.par.ry = anchor.par.ry
	if interactionEngine.SelectStartEvent.PickSop == ry:
		v = (parent.gizmo.SelectStartAxisYPos.z - intersection_point_plane_y.y) * 0.2
		v = max(-2, min(v, 2))
		anchor.par.rz -= v #remappedU#intersection_point_plane_y.y
		parent.gizmo.par.rz = anchor.par.rz
	if interactionEngine.SelectStartEvent.PickSop == rz:
		v = (parent.gizmo.SelectStartAxisZPos.x - intersection_point_plane_z.z) * 0.2
		v = max(-2, min(v, 2))
		anchor.par.rx -= v #remappedV#intersection_point_plane_z.z
		parent.gizmo.par.rx = anchor.par.rx
	
	if interactionEngine.SelectStartEvent.PickSop == sx:
		anchor_scale.par.sx = parent.gizmo.SelectStartGizmoScale.x + (intersection_point_plane_x.x - mt.x)
	if interactionEngine.SelectStartEvent.PickSop == sy:
		anchor_scale.par.sy = parent.gizmo.SelectStartGizmoScale.y + (intersection_point_plane_y.y - mt.y)
	if interactionEngine.SelectStartEvent.PickSop == sz:
		anchor_scale.par.sz = parent.gizmo.SelectStartGizmoScale.z + (intersection_point_plane_z.z - mt.z)

	if interactionEngine.SelectStartEvent.PickSop == sxy:
		anchor_scale.par.sx = parent.gizmo.SelectStartGizmoScale.x + (intersection_point_plane_x.x - mt.x)
		anchor_scale.par.sy = parent.gizmo.SelectStartGizmoScale.y + (intersection_point_plane_y.y - mt.y)
	if interactionEngine.SelectStartEvent.PickSop == szy:
		anchor_scale.par.sz = parent.gizmo.SelectStartGizmoScale.z + (intersection_point_plane_z.z - mt.z)
		anchor_scale.par.sy = parent.gizmo.SelectStartGizmoScale.y + (intersection_point_plane_y.y - mt.y)
	if interactionEngine.SelectStartEvent.PickSop == szx:
		anchor_scale.par.sz = parent.gizmo.SelectStartGizmoScale.z + (intersection_point_plane_z.z - mt.z)
		anchor_scale.par.sx = parent.gizmo.SelectStartGizmoScale.x + (intersection_point_plane_x.x - mt.x)
		

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
	
	
	