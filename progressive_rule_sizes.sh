#!/bin/bash

k_min=2
k_max=2

other_text="$*"
end="_$k_min$k_max.txt"

python test.py $k_min $k_max "$other_text$end"

# k_max=$((k_max+1))
