#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 04:30:30 2001

@author: prathmesh.savale
"""

import datetime
import sys
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)

# Define the server ip address below
#socket.connect("tcp://ip_address:port")
socket.connect("tcp://10.1.42.10:50001")



previos_timestamp = 0
list_of_timestamps = []
beacon_id = []

while 1:
    line = sys.stdin.readline().rstrip()
    
    # Extracting the timestamp from the current line being read
    current_timestamp = line[6:16]
    
    
    
    
    #    if line == '':
    #            break
    try:
    #        time.sleep(interval)
        # Appending the read line to an array
        list_of_timestamps.append(line)
        if current_timestamp != previos_timestamp:    # If the timestamp has changed i.e. after every 3 seconds
            new_listoftimestamps = list_of_timestamps[:-1]   # All elements of array except last entry containing the next timestamp
    #            print("inside loop")
    #            print(new_listoftimestamps)
    #            output_file = open("values_time","w")
            for elements in new_listoftimestamps:
                fields = elements.strip().split(',')
                beacon_id.append(fields[0])						# Beacon id i.e. 1st column is put in an array
            
            distinct_beaconids = set(beacon_id)					# Finding the no. of distinct beacons in the array
            
            
            print("############")
    #            print(len(list_of_timestamps))
            
    #            print(len(distinct_beaconids))
            for bid in distinct_beaconids:
                    rssi = []
                    
                    
    #                    cnt = 0
                    for lines in new_listoftimestamps:
    #                        cnt = cnt + 1
    #                        print("############")
    #                        print(lines)
    #                        print(cnt)
                        fields2 = lines.strip().split(",")
    #                        print("############")
    #                        print(fields2[0])
    #                        print(bid)
    #                        print("############")
    #                        if lines.find(str(bid)) != -1:
                        if str(fields2[0]) == str(bid):
#                            print(fields2)
    #                            print("matched")
                            rssi.append(int(lines.split(',')[5]))
                            
                            
                    
#                    print(rssi)
                    
                    
                    
                    tx_pow = lines.split(',')[4]
                    recv_id = lines.split(',')[7]
                    recv_x_coor = lines.split(',')[8]
                    recv_y_coor = lines.split(',')[9]
                    beaconid = bid[16:62]
                    
                    
                    
                    # Kalman Filter initial params
                    iteration_count = len(rssi)
                    #actual_values = [-0.37727 + j * j * 0.00001 for j in xrange(iteration_count)]
                    noisy_measurement = rssi
                    
                    process_variance = 1e-4  # process variance or process noise
                    
                    estimated_measurement_variance = 4  # estimate of measurement variance, change to see effect, s.d. of the measurements to be calculated manually
                    
                    # allocate space for arrays
                    posteri_estimate_for_graphing = []
                    
                    # intial guesses
                    posteri_estimate = -62
                    posteri_error_estimate = 1.0
                    
#                    print(recv_id+","+recv_x_coor+","+recv_y_coor+","+beaconid+","+previos_timestamp+","+",")
            
                                        
                    
                    for iteration in range(1, iteration_count):
                        # time update
                        priori_estimate = posteri_estimate
                        priori_error_estimate = posteri_error_estimate + process_variance
                    
                        # measurement update
                        blending_factor = priori_error_estimate / (priori_error_estimate + estimated_measurement_variance)
                        posteri_estimate = priori_estimate + blending_factor * (noisy_measurement[iteration] - priori_estimate)
                        posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
                        posteri_estimate_for_graphing.append(posteri_estimate)
                    
                    rssi_val=posteri_estimate_for_graphing[-1]
                    
                    # Kalman filter ends
                    
                    # Distance conversion formula : Can be tweaked to find a better distance estimate for rssi
                    dist = (1.837 * (rssi_val/-66)**6.448) + 0.111
                    #dist = (2.4 * (rssi_val/-66)**8.44) + 0.111
                            
                            
                    t = datetime.datetime.fromtimestamp(float(previos_timestamp))
                    
					# Output printed to terminal
                    print(str(recv_id)+","+str(recv_x_coor)+","+str(recv_y_coor)+","+str(beaconid)+","+str(t)+","+str(dist)+","+str(rssi_val)) 
                    
					# Output put in a variable to be sent to the server ip and port
                    tosend = str((str(recv_id)+","+str(recv_x_coor)+","+str(recv_y_coor)+","+str(beaconid)+","+str(t)+","+str(dist)+","+str(rssi_val)))
            
					# Send the variable to socket/ server
                    #sock.connect((host,port))      
                    socket.send_string(tosend)
                    print >>sys.stderr, 'sent'
					# Client will not send the next value until it receives a message at msg_in hence server to send back msg
                    msg_in = socket.recv()

 
                    
##################################################                        
            
#            print(new_listoftimestamps)
            list_of_timestamps = []
            new_listoftimestamps = []
            beacon_id = []
            
            
    #            output_file.write(str(list_of_timestamps))
            
            
    #            output_file.close()
            
            
    #        print(line)
    except:
        pass
    #    print("prev=current")
        
        
    
    previos_timestamp = current_timestamp    # Update the value of previous timestamp for the next iteration



#sock.close()   	 # Socket not to be closed


    
    
    
    
    
    
    
