



import sys
import os 
import time


IS_PC = False
IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_ESP32 = (os.uname().sysname == 'esp32')
IS_LORA_OLED = None
IS_RPi = not (IS_MICROPYTHON or IS_PC)


def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:] 
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:] 
    

if IS_MICROPYTHON:
            
    # Node Name
    import machine
    import ubinascii 
    uuid = ubinascii.hexlify(machine.unique_id()).decode()  
        
    if IS_ESP8266:
        NODE_NAME = 'ESP8266_'
    if IS_ESP32:
        NODE_NAME = 'ESP32_'
        import esp
        IS_LORA_OLED = True#(esp.flash_size() > 5000000)
        
    NODE_EUI = mac2eui(uuid)
    NODE_NAME = NODE_NAME + uuid
    
    # millisecond
    millisecond = time.ticks_ms
    
    # Controller
    SOFT_SPI = None
    if IS_LORA_OLED:
        from controller_esp_lora_oled import Controller
        SOFT_SPI = False#True
    else:
        from controller_esp import Controller
    
    
        
if IS_RPi:
    
    # Node Name
    import socket
    NODE_NAME = 'RPi_' + socket.gethostname()
    
    # millisecond
    millisecond = lambda : time.time() * 1000
    
    # Controller
    from controller_rpi import Controller
    
    
    
if IS_PC:
        
    # Node Name
    import socket
    NODE_NAME = 'PC_' + socket.gethostname()
    
    # millisecond
    millisecond = lambda : time.time() * 1000
    
    # Controller
    from controller_pc import Controller  





