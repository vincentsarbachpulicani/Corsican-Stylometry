pdftoppm -r 300 -tiff *.pdf document
for f in *.tif; do
<<<<<<< HEAD
	tesseract $f $(basename $f .tiff) -l fra+cos+ita
	tesseract $f $(basename $f .tiff) -l fra+cos+ita alto
=======
	tesseract $f $f -l fra+cos+ita
	tesseract $f $f -l fra+cos+ita alto
>>>>>>> be120a2822fa251a6fe9d542bd9239736fc2132f
done
cat *.txt > document-total.txt