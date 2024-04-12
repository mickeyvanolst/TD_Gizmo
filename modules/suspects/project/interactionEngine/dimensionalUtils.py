'''Info Header Start
Name : dimensionalUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from dataclasses import dataclass

def CompPosition(targetComp:COMP) -> tdu.Vector:
	return targetComp.worldTransform * tdu.Position( 0,0,0 )

@dataclass
class Plane():
	somePoint   : tdu.Position #p0
	normal      : tdu.Vector #n
	def __post_init__(self):
		self.normal.normalize()
		
@dataclass
class Ray():
	startPoint  : tdu.Position #l0
	direction   : tdu.Vector #l
	def __post_init__(self):
		self.direction.normalize()
		
	def ProjectOnPlane(self, targetPlane:Plane) -> tdu.Position:
		distance = ((targetPlane.somePoint - self.startPoint).dot( targetPlane.normal))/self.direction.dot( targetPlane.normal )
		return self.startPoint + self.direction * distance