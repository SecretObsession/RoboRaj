"""
Command to show how many points you have
"""


def points(roboraj):
    Points = roboraj['Points']
    current_points = str(Points.get_points(username=roboraj["command_info"]["user"],
                                           channel=roboraj["command_info"]["channel"]))

    response = "You have %s points!" % current_points
    return response