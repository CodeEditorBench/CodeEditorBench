leetcode_template="/home/judge/leetcode_template/java" 
if [ $# -ne 1 ]; then
    echo "Usage: $0 <run_dir>"
    exit 1
fi
run_dir="$1"
mkdir -p "${run_dir}/com"
cp -r "${leetcode_template}/com/template" "${run_dir}/com/template"
cp -r "${leetcode_template}/lib" "${run_dir}/lib"
echo "Files and directories have been copied to ${run_dir}."