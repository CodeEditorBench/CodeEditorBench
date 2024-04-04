pkill -f  -9 judge
pkill -f  -9 java
pkill -f  -9 Main

rm -r /home/judge/run[0-9]*
rm -r /home/judge/client*.pid

