#!/bin/bash

r=0.0
increase=2.0

array=( $@ )
len=${#array[@]}
file=${array[$len-1]}
other_args=${array[@]:0:$len-1}

end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=0.0025
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=$(echo "$(($r * $increase))" | bc -l)
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"

r=1.0
end="_r=$r"

{ time python test.py $other_args -r $r; } &> "output_files/$file$end"
