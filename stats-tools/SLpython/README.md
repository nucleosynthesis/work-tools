
# Simplified Likelihood

This repository can be used to construct the simplified likelihood from experimental inputs as described in [CMS-NOTE-2017-001](https://cds.cern.ch/record/2242860/).

## Checkout SL code using sparse checkout 

```
curl -s https://raw.githubusercontent.com/nucleosynthesis/work-tools/master/stats-tools/SLpython/sparse-checkout-SL-ssh.sh  > sc.sh
chmod +x sc.sh 
./sc.sh 
cd work-tools/stats-tools/SLpython
```

## The inputs for the simplified likelihood are defined in the configuration file `mymodel.py`. They are as follows 

 * `data` : A python array of observed data, one entry per bin.
 * `background` : A python array of expected background, one entry per bin. 
 * `covariance` : A pyhon array of the covariance between expected backgrounds. The format is a flat array which is converted into a 2D array inside the tool
 * `signal` : A python array of the expected signal, one entry per bin. This should be replaced with whichever signal model you are testing. 

You can replace the model with whichever search you like, provided the format is the same. 

### Convert from ROOT

In case you are generating the inputs from combine, or from another source that produces them as `TGraph` or `TH1/TH2` objects, you can convert them to the python via the `convertSLRootToPython.py` script. Simply provide the following options;

  * `-O/--outname` : The output python file containing the model (default is `test.py`)
  * `-s/--signal` : The signal histogram, should be of format `file.root:location/to/histogram`
  * `-b/--background` : The background histogram, should be of format `file.root:location/to/histogram`
  * `-d/--data` : The data TGraph, should be of format `file.root:location/to/graph`
  * `-c/--covariance` : The covariance TH2 histogram, should be of format `file.root:location/to/histogram`

You can mix different ROOT files for these inputs. 

## Run the code with `python sl-python.py --model mymodel`. This will produce a scan of  L(mu), where ![](https://latex.codecogs.com/gif.latex?%5Cinline%20L)  is the **profiled** likelihood and ![](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Cmu) is 
the signal strength parameter which multiplies the expected signal in each bin. 

Use `--help` for options on setting the range of the parameter and number of points to scan. These will include, 

  * `--rMin(--rMax)` : To set the range of `mu` used for the scan
  * `--points` : The number of points in the scan
  * `--offset` : To plot the `2*deltaNLL` instead of `2*NLL`
  * `--toy` : To replace `data` with a Poisson toy generated from the `background` provided in each bin 
