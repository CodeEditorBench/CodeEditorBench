log_dir="/home/judge/log"
if [ ! -d "$log_dir" ]; then
    mkdir -p "$log_dir"
    echo "Created log directory: $log_dir"
fi
judged /home/judge
while true; do
    current_time=$(date +%s)
    four_minutes_ago=$((current_time - 360))
    ps aux | grep 'java -Xmx512M -cp .:lib/gson-2.9.1.jar Main' | while read -r line; do
        pid=$(echo "$line" | awk '{print $2}')
        start_time=$(echo "$line" | awk '{print $9}')
        start_hour=$(echo "$start_time" | cut -d':' -f1)
        start_minute=$(echo "$start_time" | cut -d':' -f2)
        start_timestamp=$(date -d "$start_hour:$start_minute" +%s)
        if [ "$start_timestamp" -lt "$four_minutes_ago" ]; then
            kill -9 "$pid"
            echo "Killed process $pid started at $start_time"
        fi
    done
    sleep 60
done