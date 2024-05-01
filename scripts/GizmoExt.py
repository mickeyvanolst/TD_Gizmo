"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

class GizmoExt:
	"""
	GizmoExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
						   readOnly=False)

		# attributes:
		self.a = 0 # attribute
		self.B = 1 # promoted attribute

		# stored items (persistent across saves and re-initialization):
		storedItems = [
			# Only 'name' is required...
			{'name': 'MasterMatrix', 'default': tdu.Matrix(), 'readOnly': False,
			 						'property': True, 'dependable': True},
			{'name': 'MasterScale', 'default': tdu.Matrix(), 'readOnly': False,
			 						'property': True, 'dependable': True},
		]
		# Uncomment the line below to store StoredProperty. To clear stored
		# 	items, use the Storage section of the Component Editor
		
		#self.stored = StorageManager(self, ownerComp, storedItems)
		
		
		self.SelectStartAxisXPos = tdu.Position()
		self.SelectStartAxisYPos = tdu.Position()
		self.SelectStartAxisZPos = tdu.Position()
		self.SelectStartGizmoPos = tdu.Position()
		
		#parent.gizmo.par.Mastermatrix = str(tdu.Matrix())
		parent.gizmo.op('anchor_scale').setTransform(tdu.Matrix())
		parent.gizmo.op('anchor_master').setTransform(tdu.Matrix())
		parent.gizmo.op('anchor').setTransform(tdu.Matrix())
		
		m = tdu.Matrix(*(float(parent().par.Mastermatrix.eval().replace(',', '').replace('[', '').replace(']', '').split()[i]) for i in [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]))
		parent.gizmo.op('anchor_scale').par.sx = m.decompose()[0][0]
		parent.gizmo.op('anchor_scale').par.sy = m.decompose()[0][1]
		parent.gizmo.op('anchor_scale').par.sz = m.decompose()[0][2]

		parent.gizmo.op('anchor_master').par.rx = m.decompose()[1][0]
		parent.gizmo.op('anchor_master').par.ry = m.decompose()[1][1]
		parent.gizmo.op('anchor_master').par.rz = m.decompose()[1][2]

		parent.gizmo.op('anchor_master').par.tx = m.decompose()[2][0]
		parent.gizmo.op('anchor_master').par.ty = m.decompose()[2][1]
		parent.gizmo.op('anchor_master').par.tz = m.decompose()[2][2]


	def myFunction(self, v):
		debug(v)

	def PromotedFunction(self, v):
		debug(v)
		
	def PrepareGeoComp(self, v):
		op(v).par.pxform = True
		op(v).par.xformmatrixop = parent.gizmo.op('out_matrix')
	
	def ResetMatrix(self):
		parent.gizmo.par.Mastermatrix = str(tdu.Matrix())
		parent.gizmo.op('anchor_master').setTransform(tdu.Matrix())
		parent.gizmo.op('anchor_scale').setTransform(tdu.Matrix())

"""	
	def SetMasterMatrix(self, m:tdu.Matrix):
		# tdu.Matrix(float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[0]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[4]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[8]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[12]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[1]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[5]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[9]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[13]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[2]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[6]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[10]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[14]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[3]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[7]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[11]), float(parent().par.Mastermatrix.eval().replace(',','').replace('[','').replace(']','').split()[15]))
		# tdu.Matrix(*[float(x) for x in parent().par.Mastermatrix.eval().replace(',', '').replace('[', '').replace(']', '').split()])
		# tdu.Matrix(*(float(parent().par.Mastermatrix.eval().replace(',', '').replace('[', '').replace(']', '').split()[i]) for i in [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]))
		#self.MasterMatrix = m
		
		print(m)
	
	def SetMasterScale(self, m:tdu.Matrix):
		#self.MasterScale = m
		#parent.gizmo.par.Mastermatrix = str(m)
		print(m)
"""