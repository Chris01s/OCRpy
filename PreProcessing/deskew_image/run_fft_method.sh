ls=$(ls *.png)
for l in $ls
do
	python FFT_method.py $l
done  
