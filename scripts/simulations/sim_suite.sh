for SIM_NUMBER in {000..100}
do
    mkdir logs/suite/$SIM_NUMBER
    python scripts/unitless.py $SIM_NUMBER
done
