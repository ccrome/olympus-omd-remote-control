
## Here's some script I found online
http://ameblo.jp/delphinus1024/entry-12168908704.html


```
curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/switch_cammode.cgi?mode=rec&lvqty=0320x0240"

curl -v -X POST --header 'Content-Length: 49' --header 'Content-Type: text/plain; charset=ISO-8859-1' --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' -d 'A' "http://192.168.0.10/set_camprop.cgi?com=set&propname=takemode"

curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_takemisc.cgi?com=startliveview&port=37789"

curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_takemotion.cgi?com=assignafframe&point=0160x0120"

sleep 1 

while : 
do
    curl -v --header 'Host: 192.168.0.10' --header 'Connection: Keep-Alive' --header 'User-Agent: OI.Share v2' "http://192.168.0.10/exec_takemotion.cgi?com=starttake"
    sleep 5
done
```