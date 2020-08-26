
ls=$(ls *.png)
for l in $ls
do
	python deskew_maximum_variance_method.py $l
done  
