from pickle import TRUE
import threading
import time
import numpy as np
import paho.mqtt.client as paho
import random

broker = 'pldindustries.com'
port = 1883
client_id = 'group10m'
username = 'app_client'
password = 'app@1234'

topic = "/group_10m"

previous_value = {}

def sensor_value(id="", lower=0, upper=0, mean=0, a=0, b=0):
    
    n = random. randint(lower,upper)            #genarate random number between low and high values
        
    if id not in previous_value:
        prev = (lower+upper)/4 + mean/2          #get begin value
        
    else:
        prev = previous_value[id]
        
    if id == "/group_10m/security01" or id == "/group_10m/security02" or id == "/group_10m/motion":     #on or off represent using 1,0
        val = n
        previous_value[id] = val
        return val, prev
    
    else:
        val = a*n + b*prev                       #get feedback from previous sensor value
        previous_value[id] = val
        val = round(val, 3)

    return val
        

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))


def thread_function1(name, seed):
    sensor_topic = topic + "/gas"

    while True:
      
        val = sensor_value(id=sensor_topic, lower=0, upper=10000, mean=300, a=0.3, b=0.7)        #set range 0 to 10000 ppm
        print("publishing " + sensor_topic +"-",val)                                                      #if sensor value greater than 3000, it means gas leak in kichen  
        client.publish(sensor_topic, val) 
        time.sleep(15)                                                                                    #sleep time 15s
        

def thread_function2(name, seed):
    sensor_topic = topic + "/smoke"

    while True:
       
        val = sensor_value(id=sensor_topic, lower=0, upper=10000, mean=7000, a=0.4, b=0.6)        #set range 0 to 10000 ppm
        print("publishing " + sensor_topic +"-",val)                                                       #if sensor value greater than 3000, it means fire in garage
        client.publish(sensor_topic, val) 
        time.sleep(15)                                                                                     #sleep time 15s     

#Non_Periodic Function
def thread_function3(name, seed):
    sensor_topic = topic + "/security01"

    while True:
      
        val, prev = sensor_value(id=sensor_topic, lower=0, upper=1, mean=0.5, a=0.2, b=0.8)              #set main_gate open, close 
        if val != prev:                                                                                      #Publish if there is change in the motion sensor reading
            print("publishing " + sensor_topic +"-",val)                                                     #if there is a motion-1, No_motion-0
            client.publish(sensor_topic, val)
        time.sleep(25)                                                                                   #sleep time 20s
        
#Non_Periodic Function
def thread_function4(name, seed):
    sensor_topic = topic + "/security02"

    while True:
       
        val, prev = sensor_value(id=sensor_topic, lower=0, upper=1, mean=0.5, a=0.1, b=0.9)                       #set back_door open, close
        if val != prev:                                                                                      #Publish if there is change in the motion sensor reading
            print("publishing " + sensor_topic +"-",val)                                                     #if there is a motion-1, No_motion-0
            client.publish(sensor_topic, val)
        time.sleep(25)
        time.sleep(20)                                                                                      #sleep time 20s


def thread_function5(name, seed):
    sensor_topic = topic + "/temp01"

    while True:
      
        val = sensor_value(id=sensor_topic, lower=20, upper=40, mean=25, a=0.4, b=0.6)                      #set room01 temperature sensor 20c to 40c
        print("publishing " + sensor_topic +"-",val)
        client.publish(sensor_topic, val) 
        time.sleep(15)                                                                                      #sleep time 15s    
        

def thread_function6(name, seed):
    sensor_topic = topic + "/temp02"

    while True:
       
        val = sensor_value(id=sensor_topic, lower=20, upper=40, mean=25, a=0.2, b=0.8)                      #set room02 temperature sensor 20c to 40c   
        print("publishing " + sensor_topic +"-",val)
        client.publish(sensor_topic, val) 
        time.sleep(15)                                                                                      #sleep time 15s    
        

def thread_function7(name, seed):
    sensor_topic = topic + "/temp03"

    while True:
      
        val = sensor_value(id=sensor_topic, lower=20, upper=40, mean=25, a=0.3, b=0.7)                      #set room03 temperature sensor 20c to 40c   
        print("publishing " + sensor_topic +"-",val)
        client.publish(sensor_topic, val) 
        time.sleep(15)                                                                                      #sleep time 15s    


def thread_function8(name, seed):
    sensor_topic = topic + "/humidity"

    while True:
      
        val = sensor_value(id=sensor_topic, lower=0, upper=100, mean=55, a=0.4, b=0.6)                       #set range for 0-100%    
        print("publishing " + sensor_topic +"-",val)                                                         #humidity sensor for small flower house       
        client.publish(sensor_topic, val)                                                                   
        time.sleep(20)                                                                                       #sleep time 20s   

#Non_Periodic Function
def thread_function9(name, seed):                                                    
    sensor_topic = topic + "/motion"

    while True:
      
        val, prev = sensor_value(id=sensor_topic, lower=0, upper=1, mean=0.5, a=0.4, b=0.6)                  #set at the main_gate  
        if val != prev:                                                                                      #Publish if there is change in the motion sensor reading
            print("publishing " + sensor_topic +"-",val)                                                     #if there is a motion-1, No_motion-0
            client.publish(sensor_topic, val)
        time.sleep(25)                                                                                       #sleep time 25s  


def thread_function10(name, seed):                                                                     
    sensor_topic = topic + "/power"

    while True:
       
        val = sensor_value(id=sensor_topic, lower=-30, upper=20, mean=10, a=0.2, b=0.8)                        #Power consumption of the small flower house per day(dBm)
        print("publishing " + sensor_topic +"-", val)
        client.publish(sensor_topic, val)  
        time.sleep(25)                                                                                        #sleep time 25s  


if True or _name_ == "_main_":
  
    client = paho.Client(client_id)
    client.username_pw_set(username, password)
    client.on_message = on_message
    print("connecting to broker ", broker)
    client.connect(broker)
    s1 = threading.Thread(target=thread_function1, args=(1, 1))
    s2 = threading.Thread(target=thread_function2, args=(2, 2))
    s3 = threading.Thread(target=thread_function3, args=(3, 3))
    s4 = threading.Thread(target=thread_function4, args=(4, 4))
    s5 = threading.Thread(target=thread_function5, args=(5, 5))
    s6 = threading.Thread(target=thread_function6, args=(6, 6))
    s7 = threading.Thread(target=thread_function7, args=(7, 7))
    s8 = threading.Thread(target=thread_function8, args=(8, 8))
    s9 = threading.Thread(target=thread_function9, args=(9, 9))
    s10 = threading.Thread(target=thread_function10, args=(10, 10))
   
    s1.start()
    s2.start()
    s3.start()
    s4.start()
    s5.start()
    s6.start()
    s7.start()
    s8.start()
    s9.start()
    s10.start()

    # client.disconnect()  # disconnect
    # x.join()
