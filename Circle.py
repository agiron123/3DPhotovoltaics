import Wall
import numpy as np

class Circle(Wall):
    """Subclass of wall. Represents a circle"""
    def __init__(self,center,radius):
        """Create a circle with the given center and radius
        :param center: The center of the circle.
        :param radius: The radius of the circle.
        """
        self.center=center
        self.radius=radius

    def get_collision(self):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        return None