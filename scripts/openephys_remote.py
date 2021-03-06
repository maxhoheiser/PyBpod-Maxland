import zmq
import os
import time


def run_client():

    # Basic start/stop commands
    start_cmd = 'StartRecord'
    stop_cmd = 'StopRecord'

    # Example settings
    #rec_dir = os.path.join(os.getcwd(), 'Output_RecordControl')
    rec_dir = r"C:\Users\max\Desktop"
    print("Saving data to:", rec_dir)

    # Some commands
    commands = [start_cmd + f"RecDir={rec_dir}",
                start_cmd + "PrependText=Session01 AppendText=Condition01",
                start_cmd + "PrependText=Session01 AppendText=Condition02",
                start_cmd + "PrependText=Session02 AppendText=Condition01",
                start_cmd,
                start_cmd + "CreateNewDir=1"
                ]

    # Connect network handler
    ip = '127.0.0.1'
    port = 5556
    timeout = 1.

    url = "tcp://%s:%d" % (ip, port)

    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            socket.RCVTIMEO = int(timeout * 1000)  # timeout in milliseconds
            socket.connect(url)

            # Finally, start data acquisition
            socket.send_string("StartAcquisition")
            answer = socket.recv()
            print(answer)
            time.sleep(5)

            for start_cmd in commands:

                for cmd in [start_cmd, stop_cmd]:
                    socket.send(cmd)
                    answer = socket.recv()
                    print(answer)

                    if 'StartRecord' in cmd:
                        # Record data for 5 seconds
                        time.sleep(5)
                    else:
                        # Stop for 1 second
                        time.sleep(1)

            # Finally, stop data acquisition; it might be a good idea to 
            # wait a little bit until all data have been written to hard drive
            time.sleep(0.5)
            socket.send_string("StopAcquisition")
            answer = socket.recv()
            print(answer)


run_client()