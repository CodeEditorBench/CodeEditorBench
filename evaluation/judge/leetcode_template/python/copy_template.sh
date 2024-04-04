leetcode_template="/home/judge/leetcode_template/python" 
if [ $# -ne 1 ]; then
    echo "Usage: $0 <run_dir>"
    exit 1
fi

run_dir="$1"

cp "${leetcode_template}/leetcode_class.py" "${run_dir}"
cp "${leetcode_template}/parse_input.py" "${run_dir}"

echo "Files have been copied to ${run_dir}."