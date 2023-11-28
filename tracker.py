class Tracker:
    def __init__(self, id=-1, x=0, y=0, z=0, theta_x=0, theta_y=0, theta_z=0):
        self.id = id # Tracker number
        self.x = x # Distances in meters
        self.y = y
        self.z = z
        self.theta_x = theta_x # Angles in degrees
        self.theta_y = theta_y
        self.theta_z = theta_z

    def __str__(self):
        return f"Tracker {self.id} at (x={self.x}, y={self.y}, z={self.z}, theta_x={self.theta_x}, theta_y={self.theta_y}, theta_z={self.theta_z})"

    def update_position(self, x=0, y=0, z=0, theta_x=0, theta_y=0, theta_z=0):
        self.x = x
        self.y = y
        self.z = z
        self.theta_x = theta_x
        self.theta_y = theta_y
        self.theta_z = theta_z

    def get_position(self):
        return {x, y, z, theta_x, theta_y, theta_z, id}