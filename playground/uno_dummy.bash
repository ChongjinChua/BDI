
(soffice --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager") &

echo "hello"

sleep 4

netstat -nap | grep soffice

echo "world"

