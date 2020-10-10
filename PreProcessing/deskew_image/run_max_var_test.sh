
ls=$(ls *.png)
for l in $ls
do
	python3 maximum_variance_method.py $l
done  
