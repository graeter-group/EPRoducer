#!/bin/bash

#SBATCH -N 1                   # number of nodes
#SBATCH -n 4
#SBATCH --cpus-per-task=1
#SBATCH -t 48:00:00
#SBATCH --output=%x-%j.o
#SBATCH --error=%x-%j.e

# ----- definition of functions -----------------------------------------------
print_help() {
echo "
Extract the EPR absorption spectrum from an orca output file.

  -a  <float> modulation amplitude in mT.
  -d  <disturb g-tensor='[ 0 0 0 ]'> disturbance to the g-tensor. It can vary
      because of thermal effects or interactions not considered in the QM
      calculations (like solvent).
  -e  <file.dat> experimental field vs absorption file.
  -f  Use this flag to take into account hyperfine corrections. This uses a lot
      of RAM memory. Be sure that you have enough memory or that you filtered
      the nuclei to compute hyperfine correction.
  -O  <file.out='epr_info.out'> orca output file with computed EPR quantities. 
  -o  <output.dat='spectrum_wo_hyFiCorr.dat'> dat output file where you want to
      save the field vs spectrum.
  -l  <lwpp=1> linewidth
  -s  <gStrain> g-strain (EasySpin's Sys.gStrain), i.e. FWHM of the
      distribution of each g-value, in the same order as the g-values read from
      the orca output (the same order used by -d), which is increasing. It
      broadens each principal direction separately, e.g. '[0,0,0.0015]' smooths
      only the low-field edge (largest g-value). If not given, no g-strain is
      applied.
  -m  <float=179.813> experimental value of the microwave frequency. The
      default value corresponds to G-band experiments.
  -n  <int=401> number of data points used to predict the absorption spectrum. 
  -t  <int=0> type of spectrum. 0 for absorption, 1 for first derivative, 2 for
      second derivative.

  -v  verbose.
  -h  prints this message.
"
exit 0
}

# ----- set up starts ---------------------------------------------------------
# General variables
orca_output="epr_info.out"
MicroWaveExper=179.813
ndpoints=401
hyperfine='false'
output="spectrum_wo_hyFiCorr.dat"
experiment=''
lwpp=1
disturb='[ 0 0 0 ]'
verbose='false'
type=0
ModAmp=''
gstrain=''
while getopts 'a:d:e:fO:o:l:s:m:n:t:vh' flag;
do
  case "${flag}" in
    a) ModAmp=${OPTARG} ;;
    d) disturb=${OPTARG} ;;
    e) experiment=${OPTARG} ;;
    f) hyperfine='true' ;;
    O) orca_output=${OPTARG} ;;
    o) output=${OPTARG} ;;
    m) MicroWaveExper=${OPTARG} ;;
    l) lwpp=${OPTARG} ;;
    s) gstrain=${OPTARG} ;;
    n) ndpoints=${OPTARG} ;;
    t) type=${OPTARG} ;;

    v) verbose='true' ;;
    h) print_help ;;
    *) echo "for usage check: eproducer <function> -h" >&2 ; exit 1 ;;
  esac
done

source "$(eproducer basics -path)" ExtGVals $verbose
load_modules

# starting information
verbose "JOB information"
echo " * Date:"
date
echo " * Command:"
echo "$0" "$@"

if [ ! -f $experiment ]
then
  fail "you have to give the mat file of the field of the experiment using the
    flag -e. Check 'eproducer extract_EPRspec -h' for details."
fi


if [ -z "$ModAmp" ]
then
  mod_amp_info=""
else
  mod_amp_info="Exp.ModAmp = $ModAmp ;"
fi

if [ -z "$gstrain" ]
then
  gstrain_info=""
  gstrain_header=""
else
  gstrain_info="Sys.gStrain = $gstrain ;"
  gstrain_header="'# gStrain=$gstrain\n' "
fi
# ---- BODY --------------- ----------------------------------------------------
cat << EOF > ${output%.dat}.m
clear, clf, clc
data = readmatrix('${experiment}');
field = data(:,1)
% ==== Experiment
Exp.mwFreq = $MicroWaveExper;
Exp.Range = [min(field) max(field)];
Exp.nPoints = $ndpoints;
Exp.Harmonic = $type;
$mod_amp_info

% ==== Theory
Sys = orca2easyspin('$orca_output');
Sys = rmfield(Sys, 'Nucs');
Sys = rmfield(Sys, 'A');
Sys = rmfield(Sys, 'AFrame');
Sys.lwpp = $lwpp ;
$gstrain_info

Sys.g = Sys.g + $disturb ;

% EasySpin 6.0.12 bug: for axial systems whose unique axis is not z (e.g.
% g = [a b b]), hamsymm returns Dinfh and pepper drops the unique component.
% Use the full Ci grid in the molecular frame in that case.
Opt = struct();
if strcmp(hamsymm(Sys), 'Dinfh')
  Opt.GridSymmetry = 'Ci';
  Opt.GridFrame = eye(3);
end
[ field, spec ] = pepper(Sys, Exp, Opt);
data = [field(:), spec(:) ];

% ==== create file
fid = fopen('$output', 'w');
fprintf(fid, ['# Theoretical spectrum\n' ...
              '# file: $(pwd)/$orca_output\n' ...
              '# mwFreq=$MicroWaveExper\n' ...
              '# lwpp=$lwpp\n' $gstrain_header...
              '# Field [mT] Intensity [A.U]\n']); % write header
fclose(fid);
writematrix(data, '$output', 'Delimiter', 'tab', 'WriteMode', 'append');

EOF

if [ "$hyperfine" == "true" ]
then
  sed -i "/rmfield(/d" ${output%.dat}.m
fi

matlab -softwareopengl -batch "run('${output%.dat}.m')" || fail "extracting spectrum"

rm ${output%.dat}.m
finish "finished"
