
#
#
#  curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=0320x0240"
#  
#  curl -v -X POST --header 'Content-Length: 49' --header 'Content-Type: text/plain; charset=ISO-8859-1' --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' -d 'A' "http://192.168.0.10/set_camprop.cgi?com=set&propname=takemode"
#  
#  curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_takemisc.cgi?com=startliveview&port=37789"
#  
#  curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_takemotion.cgi?com=assignafframe&point=0160x0120"
#  

import xml.etree.ElementTree as ET
import urllib2
import urllib
import time

ip = "192.168.0.10"
islive = True
save_files = True

def make_url(cmd):
    return "http://%s/%s.cgi" % (ip, cmd)

def remove_encoding(s):
    return s.replace('encoding="Shift-JIS"', '')

def get_url(url, save=None, body = None):
    if body == None:
        method = "get"
    else:
        method = "post"

    if save == None:
        save = save_files
    if islive:
        #url = make_url(cmd)
        headers = {
            'Host'        : '192.168.0.10',
            'Connection'  : 'Keep-Alive',
            'User-Agent'  : 'OI.Share v2',
            'Content-Type': 'text/xml',
        }
        req = urllib2.Request(url, headers=headers)
        req.add_data(body)
        
        response = urllib2.urlopen(req)
        txt = response.read()
    else:
        txt = open("%s.txt" % cmd).read()
    #return ET.fromstring(remove_encoding(txt))
    return remove_encoding(txt)


# Must be in rec mode to get & set settings
# must be in shutter mode to release the shutter

# Sequence of events:
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=0640x0480"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/get_camprop.cgi?com=desc&propname=artfilter"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/get_camprop.cgi?com=desc&propname=isospeedvalue"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/get_camprop.cgi?com=desc&propname=shutspeedvalue"
# curl -v --header 'Content-Type: text/xml'  --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/set_camprop.cgi?com=set&propname=isospeedvalue"  -X POST -d '<set><value>800</value></set>'

# Just for shutter release:
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/switch_cammode.cgi?mode=shutter"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_shutter.cgi?com=1st2ndpush"
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_shutter.cgi?com=2nd1strelease"

# Switch back to play mode
# curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/switch_cammode.cgi?mode=play"


def get_all_settings():
    switch_mode("rec")
    #return ET.fromstring(get_url("http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist"))
    print get_url("http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist")
    exit()
    return ET.fromstring(get_url("http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist"))
    
def switch_mode(mode):
    if mode == "rec":
        get_url("http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=0640x0480")
    elif mode == "shutter":
        get_url("http://192.168.0.10/switch_cammode.cgi?mode=shutter")
    else:
        raise Exception("Invalid camera mode")
def set_shutter(speed):
    switch_mode("rec")
    get_url("http://192.168.0.10/set_camprop.cgi?com=set&propname=shutspeedvalue", body = "<set><value>%d</value></set>" % speed)
    
def set_iso(iso):
    switch_mode("rec")
    get_url("http://192.168.0.10/set_camprop.cgi?com=set&propname=isospeedvalue", body = "<set><value>%d</value></set>" % iso)

def take_photo():
    switch_mode("shutter")
    get_url("http://192.168.0.10/exec_shutter.cgi?com=1st2ndpush")
    time.sleep(.5)
    get_url("http://192.168.0.10/exec_shutter.cgi?com=2nd1strelease")

# set_shutter(100)
# set_iso(200)
# take_photo()
#
root = get_all_settings()


##root = get_url('http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist')

print root, root.attrib
for child in root:
    print child, child.attrib


