class Wall(object):
    """Represents an abstract wall out of which towers can be composed.
        Wall is sub classed to represent straight line walls and circles"""

    def get_collision(self,photon):
        """Determine wheter the given photon collides with the Wall.
        If so create and return a Record containing the relevant information."""
        return None
