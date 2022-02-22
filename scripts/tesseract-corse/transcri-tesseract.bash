pdftoppm -r 300 -tiff *.pdf document
for f in *.tif; do
	tesseract $f $f -l fra+cos+ita
	tesseract $f $f -l fra+cos+ita alto
done
cat *.txt > document-total.txt