


import time
import config_lora


from connectWiFi import do_connect
import urequests
#https://thingspeak.com/channels/1035244
API_KEY='SO3W20EMSKIEJN4E'

ssid = "Makerfabs"
pswd = "20160704"

wlan = do_connect(ssid, pswd)
s = wlan.config("mac")
wifimac = ('MAC:%02x-%02x-%02x-%02x-%02x-%02x ').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
print(wifimac)

if not wlan.isconnected():
        print('connecting to network...' + ssid)
        wlan.connect(ssid, psw)



msgCount = 0            # count of outgoing messages
INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
 

def duplexCallback(lora):
    print("LoRa Duplex with callback")
    lora.onReceive(on_receive)  # register the receive callback
    do_loop(lora)


def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0
    
    while True:
        now = config_lora.millisecond()
        if now < lastSendTime: lastSendTime = now
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            #message = "{} {}".format(config_lora.NODE_NAME, '#'+str(msgCount))
            message = "{} {}".format('Hello world ', '#'+str(msgCount))
            sendMessage(lora, message)                              # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    # print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    lora.blink_led()   
    rssi = lora.packetRssi()        
    try:

        length=len(payload)-1   
        myStr=str((payload[4:length]),'utf-8')
        length1=myStr.find(':')
        myNum1=myStr[(length1+1):(length1+6)]
        #print('%s\n'%(myStr))
        #print('Num1:%.2f\n'%(float)(myNum1))
        myNum2=myStr[(length1+20):(length1+25)]
        #print('Num2:%.2f\n'%(float)(myNum2))
        
        print("*** Received message ***\n{}".format(payload))
        #if config_lora.IS_LORA_OLED: lora.show_packet(payload_string, rssi)
        #if config_lora.IS_LORA_OLED: lora.show_packet(payload, rssi)
        
        if config_lora.IS_LORA_OLED: lora.show_packet(("{}".format(payload[4:length])), rssi)
        #print(payload_string.find(':'))
        #print('\r\n')
        #strlist=payload_string.split(':')
        #print(strlist)
        #for value in strlist:
        #    print value
        if wlan.isconnected():
            global msgCount
            print('Sending to network...')
            #URL="https://api.thingspeak.com/update?api_key="+API_KEY+"&field1="+str(msgCount)
            URL="https://api.thingspeak.com/update?api_key="+API_KEY+"&field1="+myNum1+"&field2="+myNum2
            res=urequests.get(URL)
            
            print(res.text)

        
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(rssi))










