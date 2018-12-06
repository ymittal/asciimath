#!/usr/bin/env bash

# sample usage:
# ./pretext.sh -o <output_dir> <stylesheet> <xml>

bash_dir=$(dirname $0)

stylesheet=${@:$#-1:1}
xml_file=${@:$#}
other_args=${@:1:$#-2}

xml_dir=$(dirname $xml_file)
latex_dir=$xml_dir-latex
cp -R $xml_dir/. $latex_dir

echo "Converting AsciiMath to LaTeX for..."
# find all files with .xml/.ptx extension
files=$(find $latex_dir/ -name '*.xml' -o -name '*.ptx')
for filename in $files; do
	echo $filename
	python $bash_dir/replace.py --xml $filename
done
echo "LaTeX conversion done. Output saved at $latex_dir"

output_xml=$latex_dir/$(basename $xml_file)
xsltproc $other_args $stylesheet $output_xml
