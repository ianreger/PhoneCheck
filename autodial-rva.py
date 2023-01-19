from email import header
import os
from twilio.rest import Client
import csv
from csv import reader
import time



def printspacing():
    print("\n--------------------------\n")

# Initialize Twilio Client
client = Client()


# Open list of numbers
with open('C:\WORKSPACE\AUTODIALER\phonelists\zdrva-phonelist.csv', 'r') as read_obj:
    # list of numbers
    csv_reader = reader(read_obj)
    # CSV file to write to
    csv_file = open("check-results-zdrva.csv", "w")
    
    # Iterate through numbers
    for row in csv_reader:
        # Remove the : in front of the number
        number = row[0].replace(':', '')
        

        # Initialize Call
        print("\n" + "Calling: " + number)
        curr_call = client.calls.create(
            from_ = '+1 951 749 9174',
            to = number, # current number in the CSV
            url ='https://handler.twilio.com/twiml/EHed780fe004fd5fed8f828ef65f4d96e8'
        )


        # Call loop
        call_in_session = True
        while call_in_session:
            # Get updated call info
            call_info = curr_call.sid
            get_call = client.calls(call_info).fetch()
            status = str(get_call.status)
                
            # Call fails
            if (status == "busy" or status == "failed" or status == "canceled" or status == "no-answer" or status == "failed"):
                print("Call Failed to: " + get_call.to)
                print("Call status: " + status)
                time.sleep(5)
                row_data = get_call.to + ", " + get_call.status + "\n"
                csv_file.write(row_data)
                call_in_session = False
                printspacing()
                
            
            # Call succeeds
            elif (status == "in-progress"  or status == "completed"):
                print("Call to " + get_call.to + " was successful")
                print("Call status: " + status)
                time.sleep(5)
                row_data = get_call.to + ", " + get_call.status + "\n"
                csv_file.write(row_data)
                call_in_session = False
                printspacing()

            
            # Call ringing
            else:
                # Dummy data to continue the loop
                z = 12
    csv_file.close()