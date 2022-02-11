for f in *.tif; do
	do tesseract $f $f -l fra+cos+ita
done
cat *.txt > document.txt