
ls=$(ls *.png)
for l in $ls
do
	python maximum_variance_method.py $l
done  
