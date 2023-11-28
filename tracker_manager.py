import socket
import time
import struct
from coordinate import Coordinate
import binascii

def calculate_checksum(data):
    """Use to validate recieved data"""
    #print("Calculating checksum for data: " + str(data))
    format_string = '>H'
    data_fields = {
        "x_first_half": int(struct.unpack(format_string, data[2:4])[0]),
        "x_second_half": int(struct.unpack(format_string, data[0:2])[0]),
        "y_first_half": int(struct.unpack(format_string, data[6:8])[0]),
        "y_second_half": int(struct.unpack(format_string, data[4:6])[0]),
        "z_first_half": int(struct.unpack(format_string, data[10:12])[0]),
        "z_second_half": int(struct.unpack(format_string, data[8:10])[0]),
        "theta_x_first_half": int(struct.unpack(format_string, data[14:16])[0]),
        "theta_x_second_half": int(struct.unpack(format_string, data[12:14])[0]),
        "theta_y_first_half": int(struct.unpack(format_string, data[18:20])[0]),
        "theta_y_second_half": int(struct.unpack(format_string, data[16:18])[0]),
        "theta_z_first_half": int(struct.unpack(format_string, data[22:24])[0]),
        "theta_z_second_half": int(struct.unpack(format_string, data[20:22])[0]),
        "uid_first_half": int(struct.unpack(format_string, data[26:28])[0]),
        "uid_second_half": int(struct.unpack(format_string, data[24:26])[0]),
    }

    # Calculate the checksum
    checksum = 0
    for key in data_fields:
        checksum += data_fields[key]
    return checksum    
    
class TrackerManager:
    """A class to interface with a set of MoCAP Trackers"""
    # A list of all connected trackers
    UDP_IP = "0.0.0.0"  # Listen on all interfaces
    UDP_PORT = 3333  # Match the port used by the ESP32 client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    trackers = []

    def get_trackers(self):
        return trackers

    def poll_trackers(self):
        """This must be run in an infinite loop where this class is implemented!!!"""
        data, addr = self.sock.recvfrom(128)
        if len(data) < 32:
            print("incomplete packet recieved")
            return
        #print("Recieved data {} from {}".format(str(binascii.hexlify(data)), addr)) 
        #print("Incomplete packet received. Found len=" + str(len(data)) + " but expected " + str(struct.calcsize('<6f')))
        # Parse out the data from the packet
        # Format: X, Y, Z, ThetaX, ThetaY, ThetaZ, UID, Checksum
        # Define the format string for unpacking

        # For floats
        format_string = '>f'  # '>' for big-endian, 'f' for float, 'I' for unsigned int

        #Unpack x position only
        x_raw = data[2:4] + data[0:2]
        x = struct.unpack(format_string, x_raw)
        print("Found x="  + str(x))

        #Unpack y position
        y_raw = data[6:8] + data[4:6]
        y = struct.unpack(format_string, y_raw)
        print("Found y="  + str(y))
         
        #Unpack z position
        z_raw = data[10:12] + data[8:10]
        z = struct.unpack(format_string, z_raw)
        print("Found z="  + str(z))

        #Unpack theta_x
        theta_x_raw = data[14:16] + data[12:14]
        theta_x = struct.unpack(format_string, theta_x_raw)
        print("Found theta_x="  + str(theta_x))

        #Unpack theta_y
        theta_y_raw = data[18:20] + data[16:18]
        theta_y = struct.unpack(format_string, theta_y_raw)
        #print("Found theta_y="  + str(theta_y))


        #Unpack theta_z
        theta_z_raw = data[22:24] + data[20:22]
        theta_z = struct.unpack(format_string, theta_z_raw)
        #print("Found theta_z="  + str(theta_z))

        # Change for UINT32
        format_string = '>I'

        # Unpack UID
        uid_raw = data[26:28] + data[24:26]
        uid = struct.unpack(format_string, uid_raw)
        #print("Found uid=" + str(uid))

        # Unpack checksum
        checksum_raw = data[30:32] + data[28:30]
        checksum = struct.unpack(format_string, checksum_raw)
        #print("Found checksum=" + str(checksum))
        


        #print("Unpacked: x=" + str(x) + ", y=" + str(y) + ", z=" + str(z) + ", theta_x=" + str(theta_x) + ", theta_y=" + str(theta_y) + ", theta_z=" + str(theta_z) + ", uid=" + str(uid))
        # Validate checksum
        
        expected_checksum = calculate_checksum(data)
        if (checksum[0] != expected_checksum):
            #print("Checksum mismatch for tracker {" + str(uid) + "}: Recieved {" + str(checksum[0]) + "} but calculated {" + str(expected_checksum) + "}")
            return

        found = False
        for tracker in trackers:
            if tracker.id == uid:
                # Update the tracker
                tracker.update_position(x[0], y[0], z[0], theta_x[0], theta_y[0], theta_z[0])
                #print ("Updated: " + str(tracker))
                found = True
                break
        if(found == False):
            # Create a new tracker
            new_tracker = Tracker(uid[0], x[0], y[0], z[0], theta_x[0], theta_y[0], theta_z[0])
            trackers.append(new_tracker)
            #print("New:     " + str(new_tracker))