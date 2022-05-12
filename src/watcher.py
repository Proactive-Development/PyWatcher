"""
This script is for watching the system for changes in the file system and tasks running on the system.

When a change is detected, the script will send a notification to the user.
"""
import os
import psutil
import sys
import time
import datetime
try:
    from notifypy import Notify
except ImportError:
    print("Please install notifypy: pip install notifypy")
    print("This is a required dependency to give the notifications. ")
    sys.exit(1)

logo = """
 *******           **       **             **           **                    
/**////**  **   **/**      /**            /**          /**                    
/**   /** //** ** /**   *  /**  ******   ******  ***** /**       *****  ******
/*******   //***  /**  *** /** //////** ///**/  **///**/******  **///**//**//*
/**////     /**   /** **/**/**  *******   /**  /**  // /**///**/******* /** / 
/**         **    /**** //**** **////**   /**  /**   **/**  /**/**////  /**   
/**        **     /**/   ///**//********  //** //***** /**  /**//******/***   
//        //      //       //  ////////    //   /////  //   //  ////// ///    """

def snapshot_processes():
    processes = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['cmdline'] = proc.cmdline()
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes
def snapshot_files(path):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            files.append(full_path)
    return files



if __name__ == "__main__":
    print(logo)
    print("Welcome to py watcher this will watch and allert you when a change is detected on the process and and the folder you instruct pywatcher to watch\nPrivacy Note: None of you network, process or file system data is sent to us.")
    print("The logos used in this project are from Icons8 https://icons8.com/")
    folder = input("Enter the folder you want to watch:")
    Process_a = snapshot_processes()
    Files_a = snapshot_files(folder)
    while True:
        Processes_b = snapshot_processes()
        Files_b = snapshot_files(folder)
        if Processes_b != Process_a:
            for i in Processes_b:
                if i not in Process_a:
                    print("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "]New process:", i['name'], " Cmdline:", i['cmdline'])
                    notification = Notify()
                    notification.title = "New Process Detected"
                    notification.message = "New process: " + i['name'] + " Cmdline: " + str(i['cmdline'])
                    notification.icon = "./warn.png"
                    notification.application_name = "Watcher"
                    notification.send()
        if Files_b != Files_a:
            for i in Files_b:
                if i not in Files_a:
                    print("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "]New file:", i)
                    notification = Notify()
                    notification.title = "New File Detected"
                    notification.message = "New file: " + i
                    notification.icon = "./warn.png"
                    notification.application_name = "Watcher"
                    notification.send()
            for i in Files_a:
                if i not in Files_b:
                    print("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "]File removed:", i)
                    notification = Notify()
                    notification.title = "File Removed"
                    notification.message = "File removed: " + i
                    notification.icon = "./warn.png"
                    notification.application_name = "Watcher"
                    notification.send()
        time.sleep(0.5)
        Process_a = snapshot_processes()
        Files_a = snapshot_files(folder)