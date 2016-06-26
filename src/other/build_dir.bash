
param_num=$#
param_val=$@
output_dir="../../input_files/htmls"

if (($param_num != 1)); then
    echo "USAGE: ./build_dir.bash <input file path>"
    exit 1
fi

input_files=$(cat $param_val)
#echo $test_files

for I in $input_files; do
    if [[ ! -e $output_dir/$I ]]; then
	mkdir $output_dir/$I
    fi

    if [[ ! -e $output_dir/$I/MS_url1.txt ]]; then
	touch $output_dir/$I/MS_url1.txt
    fi
    if [[ ! -e $output_dir/$I/MS_url2.txt ]]; then
	touch $output_dir/$I/MS_url2.txt
    fi
    if [[ ! -e $output_dir/$I/MS_url3.txt ]]; then
	touch $output_dir/$I/MS_url3.txt
    fi
    if [[ ! -e $output_dir/$I/MS_url4.txt ]]; then
	touch $output_dir/$I/MS_url4.txt
    fi
    if [[ ! -e $output_dir/$I/R_url1.txt ]]; then
	touch $output_dir/$I/R_url1.txt
    fi
    if [[ ! -e $output_dir/$I/R_url2.txt ]]; then
	touch $output_dir/$I/R_url2.txt
    fi

done

