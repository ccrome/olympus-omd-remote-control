
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

ip = "192.168.0.10"
islive = True
save_files = True

def make_url(cmd):
    return "http://%s/%s.cgi" % (ip, cmd)

def remove_encoding(s):
    return s.replace('encoding="Shift-JIS"', '')

def get_url(url, save=None):
    if save == None:
        save = save_files
    if islive:
        #url = make_url(cmd)
        headers = {
            'Host'       : '192.168.0.10',
            'Connection' : 'Keep-Alive',
            'User-Agent' : 'OI.Share v2'}
        req = urllib2.Request(url, headers=headers)
        print req
        response = urllib2.urlopen(req)
        txt = response.read()
        if save:
            open("%s.txt" % cmd, "w").write(txt);
    else:
        txt = open("%s.txt" % cmd).read()
    return ET.fromstring(remove_encoding(txt))


root = get_url('http://192.168.0.10/get_camprop.cgi?com=desc&propname=desclist')

print root, root.attrib
for child in root:
    print child, child.attrib


