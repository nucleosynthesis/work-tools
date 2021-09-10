# python mkQCD.py inputs/out_MTR_2017.root --function 1 --ymin 0.0001 --ymax 1000 --label "MTR 2017" --sr_cut 0.5 --logy --fit_min 0 --fit_max 1 --max_blind 1.2 --mjj_min 200 --mkworkspace
# python mkQCD.py inputs/out_VTR_2017.root --function 2 --ymin 0.0000001 --ymax 1 --label "VTR 2017" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.5 --max_blind 2 --mjj_min 900  --mkworkspace

# python mkQCD.py inputs/out_MTR_2018.root --function 1 --ymin 0.0001 --ymax 1000 --label "MTR 2018" --sr_cut 0.5 --logy --fit_min 0 --fit_max 1 --max_blind 1.2 --mjj_min 200 --background_scale_factor=1.0 --mkworkspace
# python mkQCD.py inputs/out_VTR_2018.root --function 2 --ymin 0.0000001 --ymax 1 --label "VTR 2018" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.5 --max_blind 2 --mjj_min 900 --background_scale_factor=1.0 --mkworkspace
 



vtrMIN=900

#NEW FROM NICK
python mkQCD_bkgtemplate.py inputs/out_MTR_2017.root --function 1 --ymin 0.0001 --ymax 1000 --label "MTR 2017" --sr_cut 0.5 --logy --fit_min 0 --fit_max 1.8 --max_blind 2.5 --mjj_min 200 --mkworkspace
python mkQCD_bkgtemplate.py inputs/out_VTR_2017.root --function 2 --ymin 0.0000001 --ymax 1 --label "VTR 2017" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.8 --max_blind 2.5 --mjj_min ${vtrMIN} --mkworkspace

python mkQCD_bkgtemplate.py inputs/out_MTR_2018.root --function 1 --ymin 0.0001 --ymax 1000 --label "MTR 2018" --sr_cut 0.5 --logy --fit_min 0 --fit_max 1.8 --max_blind 2.5 --mjj_min 200 --background_scale_factor=1.0 --mkworkspace
python mkQCD_bkgtemplate.py inputs/out_VTR_2018.root --function 2 --ymin 0.0000001 --ymax 1 --label "VTR 2018" --sr_cut 1.8 --logy --fit_min 0 --fit_max 1.8 --max_blind 2.5 --mjj_min ${vtrMIN} --background_scale_factor=1.0 --mkworkspace

