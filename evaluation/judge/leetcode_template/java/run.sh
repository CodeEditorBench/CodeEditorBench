work_dir="$1"
mem_lmt="$2"
java_xmx="-Xmx${mem_lmt}M"
cd "$work_dir" || exit
java $java_xmx -cp ".:lib/gson-2.9.1.jar" Main
