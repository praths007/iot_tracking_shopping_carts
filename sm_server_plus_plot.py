from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import pylab
import os
import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://192.168.1.2:50001")
# Bind to a socket to keep reading

#os.remove("/home/musigma/Sac/test/run/co_ordinates.txt")


# Interactive plotting is possible with ion function. This is important to keep updating the charts in real time
plt.ion()
try:
    
    previos_timestamp = 0
    list_of_timestamps = []
    beacon_id = []
    recv_id = []


    while True:
        msg = socket.recv()
#        print (msg.decode('utf-8'))
        socket.send(msg) 		# Send a msg back to client as acknowledgement of received data
        
        
        line = msg.decode('utf-8')
        
        current_timestamp = line[58:77]

        list_of_timestamps.append(line)
        if current_timestamp != previos_timestamp:
            new_val = list_of_timestamps[-1]
            new_listoftimestamps = list_of_timestamps[:-1]
            appendedlines = []

            
            #print(new_listoftimestamps)
            
    #            print("inside loop")
    #            print(new_listoftimestamps)
    #            output_file = open("values_time","w")
            for elements in new_listoftimestamps:
                fields = str(elements).strip().split(',')
                beacon_id.append(fields[3])
                recv_id.append(fields[0])
                
            distinct_beaconids = set(beacon_id)
            distinct_recv=set(recv_id)
            
            no_of_recv=len(distinct_recv)
            
#            print("############")
    #            print(len(list_of_timestamps))
            
            no_of_beacons = (len(distinct_beaconids))
            
#            for data_elements in new_listoftimestamps:
#                lines = str(data_elements).strip().split(",")
#                appendedlines.append(lines)
#                        lines.sort(key=lambda x: x[1])
#            appendedlines.sort(key = lambda x:x[5],reverse = False)
                    
            ####SCREWUP here       
#            new_listoftimestamps = appendedlines[:3]
            
            #print("\n\n")
            print("############")
			
			# Initiating plotting
            plt.clf()
            ax = plt.axes()
            plt.ylim((-2,10))
            plt.xlim((-2,10))
            plt.plot([0,6,7,1],[0,1,7,7], 'ro')
            plt.plot([1,6,6,1,1],[4,4,5.5,5.5,4])
            plt.plot([1,6,6,1,1],[1,1,2.5,2.5,1])        
            
            for bid in distinct_beaconids:
                distance_values = []
                recv_values =[]
                x_coord = []
                y_coord = []
                sorted_beacon = [] 
                appendedlines = []
                
                for data_elements in new_listoftimestamps:
                    if str(data_elements).find(bid) != -1:
                        lines = str(data_elements).strip().split(",")
                        appendedlines.append(lines)
    #                        lines.sort(key=lambda x: x[1])
                appendedlines.sort(key = lambda x: (x[5], x[1]),reverse = False)
                    
            ####SCREWUP here       
                sorted_beacon = appendedlines[:3]            
                
                
                for lines in sorted_beacon:

                        if str(lines).find(bid) != -1:
#                            print(fields2)
                            #print("matched")
                            recv_values.append(str(lines).split(',')[0][2:-1])
                            distance_values.append(float(str(lines).split(',')[5][2:-1]))
                            x_coord.append(float(str(lines).split(',')[1][2:-1]))
                            y_coord.append(float(str(lines).split(',')[2][2:-1]))
                            
                            
                try:
                    xa = float(x_coord[0])
                except IndexError:
                    xa = 0.0
                
                try:
                    xb = float(x_coord[1])
                except IndexError:
                    xb = 0.0
                    
                try:
                    xc = float(x_coord[2])
                except IndexError:
                    xc = 0.0
                
                try:
                    ya = float(y_coord[0])
                except IndexError:
                    ya = 0.0
                    
                try:
                    yb = float(y_coord[1])
                except IndexError:
                    yb = 0.0
                    
                try:
                    yc = float(y_coord[2])
                except IndexError:
                    yc = 0.0
                
                try:
                    ra = float(distance_values[0])
                except IndexError:
                    ra = 0.0
                    
                try:
                    rb = float(distance_values[1])
                except IndexError:
                    rb = 0.0
                    
                try:
                    rc = float(distance_values[2])
                except IndexError:
                    rc = 0.0
                
                    
                    
                
                S = ((xc**2.0) - (xb**2.0) + (yc**2.0) - (yb**2.0) + (rb**2.0) - (rc**2.0)) / 2.0
                T = ((xa**2.0) - (xb**2.0) + (ya**2.0) - (yb**2.0) + (rb**2.0) - (ra**2.0)) / 2.0
            
            
                try:
                    Y = ((T * (xb - xc)) - (S * (xb - xa))) / (((ya - yb) * (xb - xc)) - ((yc -yb) * (xb - xa)))
                    X = ((Y * (ya -yb)) - T) / (xb -xa)
                    
                except ZeroDivisionError:
                    X = 0
                    Y = 0
                    
                output=str(str(bid)+","+str(previos_timestamp)+","+str(X)+","+str(Y)+","+str(recv_values[0])+","+str(distance_values[0]))   
                #print("############################")  
                #print(str(distance_values))
                #print(str(x_coord))
                #print(str(y_coord))
                print(str(bid)+","+str(previos_timestamp)+","+str(X)+","+str(Y)+","+str(recv_values[0])+","+str(distance_values[0]))
                f=open("/home/musigma/Sac/test/run/co_ordinates.txt", "a")                
                f.write(output)
                f.write("\n")
                f.close()
                circle1 = plt.Circle((float(x_coord[0]),float(y_coord[0])), radius=float(distance_values[0]), alpha =.2)

                ax.add_patch(circle1)
                #print("\n\n")                       
        
            plt.draw()    
            list_of_timestamps = []
            list_of_timestamps.append(new_val)
            new_listoftimestamps = []
            beacon_id = []
            recv_id=[]
            previos_timestamp=current_timestamp

#        print(current_timestamp)
        
finally:
    pass

