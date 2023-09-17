import Controller_Data.Controller__249_AP as AP_249
import Controller_Data.Controller_249_Client as Client_249
import threading

threads = []
threads.append(threading.Thread(target = AP_249.start_Controller_249_AP(), args = ()))     
threads.append(threading.Thread(target = Client_249.start_Controller_249_AP(), args = ()))    
for i in range(len(threads)):
    threads[i].start()