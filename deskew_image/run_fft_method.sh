ls=$(ls *.png)
for l in $ls
do
	python deskew_FFT_method.py $l
done  
