pdftoppm -r 300 -tiff *.pdf document
for f in *.tif; do
	tesseract $f $(basename $f .tiff) -l fra+cos+ita
	tesseract $f $(basename $f .tiff) -l fra+cos+ita alto
done
cat *.txt > document-total.txt