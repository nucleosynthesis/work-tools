
#Simplified Likelihood

This repository can be used to construct the simplified likelihood from experimental inputs as described in [CMS-NOTE-2017-001](https://cds.cern.ch/record/2242860/).

1) Checkout SL code using sparse checkout 

curl -s https://raw.githubusercontent.com/nucleosynthesis/work-tools/master/stats-tools/SLpython/sparse-checkout-SL-ssh.sh  > sc.sh
chmod +x sc.sh 
./sc.sh 
cd work-tools/stats-tools/SLpython

2) The inputs for the simplified likelihood are defined in the configuration file `mymodel.py`. They are as follows 

 * `data` : A python array of observed data, one entry per bin.
 * `background` : A python array of expected background, one entry per bin. 
 * `covariance` : A pyhon array of the covariance between expected backgrounds. The format is a flat array which is converted into a 2D array inside the tool
 * `signal` : A python array of the expected signal, one entry per bin. This should be replaced with whichever signal model you are testing. 

You can replace the model with whichever search you like, provided the format is the same. 

3) Run the code with `python sl-python.py --model mymodel`. This will produce a scan of  $$-2*\Log(L(\mu))$$, where $$L$$ is the **profiled** likelihood and $$\mu$$ is 
the signal strength parameter which multiplies the expected signal in each bin. 

Use `--help` for options on setting the range of the parameter and number of points to scan
