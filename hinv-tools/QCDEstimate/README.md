# QCD Fits 

The code is all inside `mkQCD.py` - this code takes histograms (provided by S. Webb) and produces workspaces containing the method B) QCD estimate. 
It also runs a "closure" check in the A/B regions where the JetHT data is used (lower MET). This closure is not great just yet but will be worked 
on in the future. 

To get the codes, run

`bash <(curl -s https://raw.githubusercontent.com/nucleosynthesis/work-tools/master/hinv-tools/QCDEstimate/sparse-checkout-VBFQCD-ssh.sh)`

# Example for running the VTR 2017 region 

Below is how the tool is run for the Run-2 analysis for the 4 regions 

```
python mkQCD_bkgtemplate.py out_VTR_2017.root  --function 2 --ymin 0.000001 --ymax 100 --label "VTR 2017" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.8 --max_blind 3.2 --mjj_min 900 --mkworkspace

python mkQCD_bkgtemplate.py out_VTR_2018.root  --function 2 --ymin 0.000001 --ymax 100 --label "VTR 2018" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.8 --max_blind 3.2 --mjj_min 900 --mkworkspace

python mkQCD_bkgtemplate.py out_MTR_2017.root  --function 1 --ymin 0.00001 --ymax 100 --label "MTR 2017" --sr_cut 0.5 --logy --fit_min 0 --fit_max 1.8 --max_blind 3.2 --mjj_min 200 --mkworkspace

python mkQCD_bkgtemplate.py out_MTR_2018.root  --function 1 --ymin 0.00001 --ymax 100 --label "MTR 2018"
```

where `out_X.root` are the histogram files produced from S. Webb. (see eg here [out_MTR_2017.root](https://gitlab.cern.ch/cms-hcg/cadi/hig-20-003/-/blob/master_UL/MTR_2017/out_MTR_2017.root)

You can run with `python mkQCD_bkgtemplate.py  -h` for more explanation on what the options are. 

# Outputs 

The code (following the above) will output the following 

  * `out_VTR_2017.root_qcdDD_normfit.pdf` - this shows the fit in the mindphi variable, it also has the uncertainty from the fit shown on the QCD Normalisation
  * `out_VTR_2017.root_qcdDD.pdf` - this has the final QCD estimate along with its uncertainty band plotted - it will also plot the QCD MC and the method A result (from S. Webb's file)
  * `out_VTR_2017.root_qcdEstimate_toys.pdf` - You can mostly ignore this one, except that in the top left, you see a Result like `N = XXX(1+YY)^theta` - the number `1+YY` is what should go in the datacard as the uncertainty on the normalisation from the fit
  * `out_MTR_2017.root_mjj_CR.pdf` - The data and non-qcd backgrounds plot in the QCD control region. 

Along with some other less important figures. 

When everything looks ok with the fits/plots etc, **you must add the option** `--mkworkspace`, which will finally produce the workspace (inside a file called `out_VTR_2017.root_qcdDD.root`), for combine. You **must make sure** that you are using the same version of CMSSW as combine otherwise the workspace in the end won't work - see here for the reccomended versions : http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#setting-up-the-environment-and-installation 

Note that all of the above plots will also be included in the root file with the workspace inside a folder called `Plots`. 

The inputs from the histogram files will also be copied over to the Folder `Inputs`. 

Note the naming convention is to just use the input file name with extensions, hopefully it is self explanatory 
