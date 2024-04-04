work_dir="$1"

cd "$work_dir" || exit

javac -cp ".:lib/gson-2.9.1.jar" com/template/*.java Main.java
