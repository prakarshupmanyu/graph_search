testCases=`ls ${1}*`
echo $testCases
for file in $testCases
do
	outputName="output_"${file}
	echo "Running file : ${file}"
	cp $file input.txt
	python homework.py > /dev/null
	diff=`comm -3 output.txt ${outputName}`
	if [ ! -z "$diff" ]; then
		echo $diff
		echo "output :"
		cat output.txt
		echo "Expected output:"
		cat $outputName
	else
		echo "Case PASSED"
	fi
done
exit
