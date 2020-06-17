# Simple plotter

This simple plotter just runs over trees to make plots (stacked histograms) from samples 
The main python is in `plots2.py`, and you run by providing a config file (eg `example_VBFHinv2018.py`)

The script should be run in stages eg. 

`1. python plots2.py example_VBFHinv2018 MKHISTOS `
`2. python plots2.py example_VBFHinv2018 PLOTHISTOS` 

You can also split the tasks first and run parallel interative jobs 

`1. python plots2.py example_VBFHinv2018.py COUNTJOBS` 
`2. for i in {1..11} ; do python plots2.py example_VBFHinv2018 MKHISTOS $i & done `

(note the number of jobs, `{1..11}` here, should be taken from step 1. Then when they are all finished, you merge and plot 

`3. python plots2.py example_VBFHinv2018 MERGEJOBS `
`4. python plots2.py example_VBFHinv2018 PLOTHISTOS`

The histogram plots are stored in `odir` from the config (eg, in this example its `odir = "plots_2018_newVTR"`


