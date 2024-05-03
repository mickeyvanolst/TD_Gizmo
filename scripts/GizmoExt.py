from TDStoreTools import StorageManager
import TDFunctions as TDF

class GizmoExt:
	"""
	GizmoExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp	
		
		self.SelectStartAxisXPos = tdu.Position()
		self.SelectStartAxisYPos = tdu.Position()
		self.SelectStartAxisZPos = tdu.Position()
		self.SelectStartGizmoPos = tdu.Position()
		
		self.IsHovering = False