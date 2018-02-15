"""Python Module to control the Franka Arm though simple method calls.

This module uses ``subprocess`` and ``os``.
"""
import subprocess
import os


class FrankaControl:
    """Class containing methods to control an instance of the Franka Arm.

    Will print debug information to the console when ``debug_flag=True`` argument is used. Class
    references C++ binaries to control the Franka.

    IP address of Franka in Robotics Lab already configured as default.
    """
    def __init__(self, ip='192.168.0.88', debug_flag=False):
        self.ip_address = ip
        self.debug = debug_flag
        self.path = os.path.dirname(os.path.realpath(__file__))  # gets working dir of this file

    def move_relative(self, dx: float=0.0, dy: float=0.0, dz: float=0.0):
        """Moves Franka Arm relative to its current position.

        Executes Franka C++ binary which moves the arm relative to its current position according
        to the to the delta input arguments. **Note: units of distance are in metres.**

        Returns the *exit code* of the C++ binary.
        """
        try:
            dx, dy, dz = float(dx), float(dy), float(dz)
        except ValueError:
            print("Arguments are invalid: must be floats")
            return

        dx, dy, dz = str(dx), str(dy), str(dz)

        program = './franka_move_to_relative'  # set executable to be used
        command = [program, self.ip_address, dx, dy, dz]
        command_str = " ".join(command)

        if self.debug:
            print("Working directory: ", self.path)
            print("Program: ", program)
            print("IP Address of robot: ", self.ip_address)
            print("dx: ", dx)
            print("dy: ", dy)
            print("dz: ", dz)
            print("Command being called: ", command_str)
            print("Running FRANKA code...")

        return_code = subprocess.call(command, cwd=self.path)

        if return_code == 0:
            if self.debug:
                print("No problems running ", program)
        else:
            print("Python has registered a problem with ", program)

        return return_code

    def get_pos(self):
        """Gets current joint postitions for Franka Arm.

        Longer msg here/
        """

        program = './print_joint_positions'  # set executable to be used
        command = [program, self.ip_address]
        command_str = " ".join(command)

        if self.debug:
            print("Working directory: ", self.path)
            print("Program: ", program)
            print("IP Address of robot: ", self.ip_address)
            print("dx: ", dx)
            print("dy: ", dy)
            print("dz: ", dz)
            print("Command being called: ", command_str)
            print("Running FRANKA code...")

        # return_code = subprocess.call(command, cwd=self.path)
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = process.communicate()
        new_str = out.decode("utf-8")
        # print("\nConvert into a string:", new_str)

        import ast
        new_str_list = new_str.split("\n")

        converted_list = []
        for idx, lit in enumerate(new_str_list):
            x = lit
            x = ast.literal_eval(x)
            # x = [n.strip() for n in x]
            converted_list.append(x)
            if idx == 7:
                break  # We have parsed all 8 items from ./get_joint_postitions
            

        # print("\nSo far:", converted_list)
        return converted_list


        if return_code == 0:
            if self.debug:
                print("No problems running ", program)
        else:
            print("Python has registered a problem with ", program)

        return return_code

    def move_absolute(self, coordinates: list):
        """Moves Franka Arm to an absolute coordinate position.

        Coordinates list should be in format: [x, y, z]

        This method will try to move straight to the coordinates given. These coordinates
        correspond to the internal origin defined by the Arm.

        Returns the *exit code* of the C++ binary.
        """
        if len(coordinates) > 3:
            raise ValueError("Invalid coordinates. There can only be three dimensions.")
        x, y, z = coordinates[0], coordinates[1], coordinates[2]

        # TODO: implement safety check for target coordinates

        program = './franka_move_to_absolute'
        command = [program, self.ip_address, x, y, z]
        command_str = " ".join(command)

        if self.debug:
            print("Working directory: ", self.path)
            print("Program: ", program)
            print("IP Address of robot: ", self.ip_address)
            print("Go to x: ", x)
            print("Go to y: ", y)
            print("Go to z: ", z)
            print("Command being called: ", command_str)
            print("Running FRANKA code...")

        return_code = subprocess.call(command, cwd=self.path)

        if return_code == 0:
            if self.debug:
                print("No problems running ", program)
        else:
            print("Python has registered a problem with ", program)

        return return_code


def main():
    """Used to test if module is working and can control arm.

    When ``caller.py`` is run from the command line it will test to see if the Franka Arm can be
    controlled with a simple forward and backward motion control along the x axis. Follow on
    screen examples for usage."""

    while True:
        testing = input("Is this program being tested with the arm? [N/y]: ")
        if testing == '' or testing.lower() == 'n':
            testing = False
            break
        elif testing.lower() == 'y':
            testing = True
            break
        else:
            print("Invalid response.")
    print("Testing mode: ", testing)

    while True:
        direction = input("Enter 0 to move along x slightly, 1 for backwards: ")
        if direction in ['0', '1']:
            break
        else:
            print("Invalid input. Must be 0/1.")

    if testing:
        arm = FrankaControl(debug_flag=True)

        if direction == '0':
            arm.move_relative(dx=0.05)
        elif direction == '1':
            arm.move_relative(dx=-0.05)

    else:
        dx = '0'
        dy = '0'
        dz = '0'
        if direction == '0':
            dx = 0.05
        elif direction == '1':
            dx = -0.05
        print("dx: ", dx)
        print("dy: ", dy)
        print("dz: ", dz)

        program = './franka_move_to_relative'
        ip_address = '192.168.0.88'

        print("Program being run is: ", program)
        print("IP Address of robot: ", ip_address)

        command = [program, ip_address, dx, dy, dz]
        command_str = " ".join(command)

        print("Command being called: ", command_str)


if __name__ == '__main__':
    main()
