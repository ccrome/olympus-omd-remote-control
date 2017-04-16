import pprint
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

# Must be in rec mode to get & set settings
# must be in shutter mode to release the shutter

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem        

class OMDNotThere(Exception):
    pass

class OMD:
    def __init__(self):
        self.ip = "192.168.0.10"
        self.settings, self.settables = self.get_all_settings()
        #pp = pprint.PrettyPrinter()
        #pp.pprint(self.settables)
        
    def make_url(self, cmd):
        return "http://%s/%s.cgi" % (self.ip, cmd)

    def remove_encoding(self, s):
        return s.replace('encoding="Shift-JIS"', '')

    def get_url(self, url, save=None, body = None):
        try:
            if body == None:
                method = "get"
            else:
                method = "post"

            if save == None:
                save = save_files
            if islive:
                headers = {
                    'Host'        : '192.168.0.10',
                    'Connection'  : 'Keep-Alive',
                    'User-Agent'  : 'OI.Share v2',
                    'Content-Type': 'text/xml',
                }
                req = urllib2.Request(url, headers=headers)
                req.add_data(body)

                response = urllib2.urlopen(req, timeout=2)
                txt = response.read()
            else:
                txt = open("%s.txt" % cmd).read()
            #return ET.fromstring(remove_encoding(txt))
            return self.remove_encoding(txt)
        except urllib2.URLError as e:
            raise OMDNotThere("Could not connect to the OM-D camera at 192.168.0.10. This is probably because you're not connected to the camera's wifi network.")
        
    def get_all_settings(self):
        self.switch_mode("rec")
        root = ET.fromstring(self.get_url("http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist"))
        settings = {}
        for child in root:
            if child.tag == "desc":
                propname  = child.find("propname").text  # property name
                attribute = child.find("attribute").text # get or getset
                value     = child.find("value").text     # the current value
                try:
                    enum      = child.find("enum").text      # the list of possible values
                    enum = enum.split(" ")
                except AttributeError:
                    enum = None
                settings[propname] = {
                    "attribute" : attribute,
                    "value"     : value,
                    "enum"      : enum,
                }
        settable_settings = {}
        for setting in settings:
            if settings[setting]["attribute"] == "getset":
                settable_settings[setting] = settings[setting]
        return settings, settable_settings
        #indent(root)
        #ET.dump(root)
        exit()
    
    def switch_mode(self, mode):
        if mode == "rec":
            self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=0640x0480")
        elif mode == "shutter":
            self.get_url("http://192.168.0.10/switch_cammode.cgi?mode=shutter")
        else:
            raise Exception("Invalid camera mode")

    def is_settable(self, settingname):
        return self.settings[settingname]["attribute"] == "getset"
    
    def get_setting(self, settingname):
        current_value  = self.settings[settingname]["value"]
        allowed_values = self.settings[settingname]["enum"]
        return current_value, allowed_values
        
    def set_shutter(self, speed):
        self.switch_mode("rec")
        self.get_url("http://192.168.0.10/set_camprop.cgi?com=set&propname=shutspeedvalue", body = "<set><value>%s</value></set>" % speed)

    def set_iso(self, iso):
        self.switch_mode("rec")
        self.get_url("http://192.168.0.10/set_camprop.cgi?com=set&propname=isospeedvalue", body = "<set><value>%d</value></set>" % iso)

    def take_photo(self):
        self.switch_mode("shutter")
        self.get_url("http://192.168.0.10/exec_shutter.cgi?com=1st2ndpush")
        time.sleep(.5)
        self.get_url("http://192.168.0.10/exec_shutter.cgi?com=2nd1strelease")
    
# set_shutter(100)
# set_iso(200)
# take_photo()
#
omd = OMD()
print omd.get_setting("shutspeedvalue")
print omd.is_settable("shutspeedvalue")
omd.take_photo()
#omd.set_shutter('1"')
#omd.take_photo()

#root = omd.get_all_settings()
#
###root = get_url('http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist')
#
#print root, root.attrib
#for child in root:
#    print child, child.attrib


