ls=$(ls *.png)
for l in $ls
do
	python bounding_box_method.py $l
done  
