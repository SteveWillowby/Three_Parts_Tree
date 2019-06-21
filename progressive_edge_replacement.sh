#!/bin/bash

r=0.0
increment=0.2

array=( $@ )
len=${#array[@]}
file=${array[$len-1]}
other_args=${array[@]:0:$len-1}

end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"

r=$(echo $r + $increment | bc)
end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"

r=$(echo $r + $increment | bc)
end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"

r=$(echo $r + $increment | bc)
end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"

r=$(echo $r + $increment | bc)
end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"

r=$(echo $r + $increment | bc)
end="_r=$r"

time python test.py $other_args -r $r > "output_files/$file$end"
