#!/usr/bin/env bash
# this script automatically optimizes sieving parameters
# Usage: optimize.sh params.cxx cxx.polyselect2.poly
# Puts the optimized file in params.cxx.opt in the current directory.
# Remark: the 'nomad' binary must be in $PATH (see README)
# The CADO_BUILD environment variable must contain the CADO-NFS build
# directory (makefb and las are taken from $CADO_BUILD/sieve), i.e.,
# something like /xxx/cado-nfs/build/<some_name>

# Important: if lpb0 and/or lpb1 change, you need to recompute rels_wanted,
# which should be near from prime_pi(2^lpb0) + prime_pi(2^lpb1)

# Force the shell to bomb out in case a command fails in the script.
# set -e

# To limit the number of black-box evaluations to say 50:
# NOMAD_MAX_BB_EVAL=50 ./optimize.sh ...

: ${NOMAD_MAX_BB_EVAL=100}
export NOMAD_MAX_BB_EVAL

# To use nomad p-MADS set NOMAD_MPI to more than 1.
# This will run blackbox evaluations in parallel.

: ${NOMAD_MPI=1}
export NOMAD_MPI 

# To use say 8 threads:
# OPAL_NUM_THREADS=8 ./optimize.sh ...
# Note that when the number of threads increases, the estimated time reported
# by OPAL does increase. This is not really a problem if this time increases
# by the same factor between two sets of parameters. However this is no longer
# the case for a number of threads larger than 4. Here are examples on rsa140,
# with two different sets of parameters, lpb[01]=28 and lpb[01]=29:
#                  lpb[01]=28                     lpb[01]=29
# OPAL_NUM_THREADS=2      1.31e6                         1.35e6
# OPAL_NUM_THREADS=4      1.32e6                         1.35e6
# OPAL_NUM_THREADS=8      1.40e6                         1.43e6
# OPAL_NUM_THREADS=16     1.82e6                         1.78e6
# We thus see the estimated time indeed increases with OPAL_NUM_THREADS, and
# with OPAL_NUM_THREADS=16 the first set of parameters is worse than the second one.
# Thus for production use we recommend to use OPAL_NUM_THREADS <= 4.

: ${OPAL_NUM_THREADS=4}

# Set number of parallel instances of las.
# This can help to parallelize the optimization process, but the use of NOMAD_MPI is preferred.
# Set to 1 unless you understand what you're doing

: ${OPAL_NUM_WORKERS=1}

cwd=`pwd`

### Set params file from first argument
if [ -e "$1" ] ; then
  params=$1
else
  echo "Could not find params file '$1'"
  exit 1
fi

### Set poly file from second argument
if [ -e "$2" ] ; then
  poly=`basename $2`
else
  echo "Could not find poly file '$2'"
  exit 1
fi

### Check that CADO_BUILD contains the path to a directory
if [ -d "${CADO_BUILD}" ] ; then
  echo "CADO_BUILD = ${CADO_BUILD}"
else
  echo "CADO_BUILD does not contain the name of a directory: '${CADO_BUILD}'"
  ls -ld "${CADO_BUILD}"
  ls -l "${CADO_BUILD}"
  exit 1
fi

if ! [ -x "${CADO_BUILD}/sieve/makefb" ] || ! [ -x "${CADO_BUILD}/sieve/las" ] ; then
    echo "could not find ${CADO_BUILD}/sieve/makefb and ${CADO_BUILD}/sieve/las ; have you run \"make\" ?"
    exit 1
fi

### Set working directory
d=`mktemp -d`
echo "Working directory:" $d

# cleanup() { rm -rf "$d" ; }
# trap cleanup EXIT


### Copy las_optimize, report and poly file and replace its name in las_run
cp $2 las_optimize.py report.py $d
sed "s/c59.polyselect2.poly/$poly/g" las_run.py | \
sed "s/[0-9]\+,\? # number of threads for las/$OPAL_NUM_THREADS,/g" | \
sed "s/[0-9]\+,\? # number of workers for las/$OPAL_NUM_WORKERS,/g" > $d/las_run.py

### Parsing poly file (number of poly and rat/alg) (for now assume npoly == 2)
npoly=`grep -c "^poly[0-9]" $d/$poly || :`
if [ $npoly -eq 0 ] ; then # polys are given by Y[0-9] and (c[0-9] or X[0-9])
  if grep -q "^Y[2-9]" $d/$poly ; then
    poly0="alg"
  else
    poly0="rat"
  fi
  if grep -q "^[cX][2-9]" $d/$poly ; then
    poly1="alg"
  else
    poly1="rat"
  fi
elif [ $npoly -eq 2 ] ; then # polys are given by 'poly[0-9]:c0,c1,...'
  if [ `grep "^poly0" $d/$poly | tr -cd , | wc -c` -eq 1 ] ; then
    poly0="rat"
  else
    poly0="alg"
  fi
  if [ `grep "^poly1" $d/$poly | tr -cd , | wc -c` -eq 1 ] ; then
    poly1="rat"
  else
    poly1="alg"
  fi
else
  echo "Error, expected 2 polynomials, got $npoly"
  exit 1
fi
echo "Type of polynomials: $poly0, $poly1"
export OPAL_CADO_TYPE="$poly0,$poly1"
echo "OPAL_CADO_TYPE=${OPAL_CADO_TYPE}"

### Parse sqside parameter if present and set OPAL_CADO_SQSIDE env variable
# if not given, set to an empty string (it means we let las choose)
sqside=`grep "sqside.*=" $params | cut -d= -f2`
export OPAL_CADO_SQSIDE="$sqside"
echo "OPAL_CADO_SQSIDE=${OPAL_CADO_SQSIDE}"

### Get parameters from params file and set _min and _max
lim0=`grep "^\(tasks\.\(sieve\.\)\?\)\?lim0.*=" $params | cut -d= -f2`
lim1=`grep "^\(tasks\.\(sieve\.\)\?\)\?lim1.*=" $params | cut -d= -f2`
qmin=`grep "^\(tasks\.\(sieve\.\)\?\)\?qmin.*=" $params | cut -d= -f2`
bkthresh1=`grep "^\(tasks\.\(sieve\.\)\?\)\?bkthresh1.*=" $params | cut -d= -f2`
lpb0=`grep "^\(tasks\.\(sieve\.\)\?\)\?lpb0.*=" $params | cut -d= -f2`
lpb1=`grep "^\(tasks\.\(sieve\.\)\?\)\?lpb1.*=" $params | cut -d= -f2`
mfb0=`grep "^\(tasks\.\(sieve\.\)\?\)\?mfb0.*=" $params | cut -d= -f2`
mfb1=`grep "^\(tasks\.\(sieve\.\)\?\)\?mfb1.*=" $params | cut -d= -f2`
ncurves0=`grep "^\(tasks\.\(sieve\.\)\?\)\?ncurves0.*=" $params | cut -d= -f2`
ncurves1=`grep "^\(tasks\.\(sieve\.\)\?\)\?ncurves1.*=" $params | cut -d= -f2`
I=`grep "^\(tasks\.\(sieve\.\)\?\)\?I.*=" $params | cut -d= -f2`
echo lim01 $lim0 $lim1
if [ "$qmin" ] ; then
   has_qmin=1
else
   qmin=$lim1
   has_qmin=0
fi
if [ "$bkthresh1" ] ; then
   has_bkthresh1=1
else
   # factor base primes larger than bkthresh (default 2^I) are bucket-sieved
   # factor base primes between bkthresh1 and lim[01] are 2-level
   # bucket-sieved. If bkthresh1 = lim[01], then we only have one level.
   # The default value bkthresh1 = 0 is mapped to bkthresh1 = lim[01].
   # A similar behaviour is obtained when bkthresh1 = max(lim0,lim1).
   bkthresh1=0
   has_bkthresh1=0
fi
echo lpb01 $lpb0 $lpb1
echo mfb01 $mfb0 $mfb1
if [ "$ncurves0" ] ; then
   has_ncurves0=1
else
   ncurves0=10
   has_ncurves0=0
fi
if [ "$ncurves1" ] ; then
   has_ncurves1=1
else
   ncurves1=10
   has_ncurves1=0
fi
echo ncurves01 $ncurves0 $ncurves1
echo I $I
qmin_min=`expr $qmin / 2`
qmin_max=`expr $qmin \* 2`
echo $qmin_min $qmin_max
# integer parameters are limited to 2147483645 in OPAL
if [ $qmin_max -gt 2147483645 ] ; then
   qmin_max=2147483645
fi
# unset set -ex locally since bkthresh1_min can be 0,
# in which case the shell will exit...
set +ex
bkthresh1_min=`expr $bkthresh1 / 2`
echo $bkthresh1_min
bkthresh1_max=`expr $bkthresh1 \* 2`
set -ex
lim0_min=`expr $lim0 / 2`
lim0_max=`expr $lim0 \* 2`
# integer parameters are limited to 2147483645 in OPAL
if [ $lim0_max -gt 2147483645 ] ; then
   lim0_max=2147483645
fi
lim1_min=`expr $lim1 / 2`
lim1_max=`expr $lim1 \* 2`
if [ $lim1_max -gt 2147483645 ] ; then
   lim1_max=2147483645
fi
echo "lim0" $lim0_min $lim0_max
lpb0_min=`expr $lpb0 - 1`
lpb0_max=`expr $lpb0 + 1`
echo $lpb0_min $lpb0_max
lpb1_min=`expr $lpb1 - 1`
lpb1_max=`expr $lpb1 + 1`
mfb0_min=$lpb0_min
mfb0_max=`expr $lpb0_max \* 3`
if [ $mfb0 -gt $mfb0_max ] ; then
   mfb0_max=$mfb0
fi
mfb1_min=$lpb1_min
mfb1_max=`expr $lpb1_max \* 3`
if [ $mfb1 -gt $mfb1_max ] ; then
   mfb1_max=$mfb1
fi
echo $mfb0_min $mfb0_max
echo $mfb1_min $mfb1_max
if [ $ncurves0 -gt 3 ] ; then
ncurves0_min=`expr $ncurves0 - 3`
else
ncurves0_min=0
fi
ncurves0_max=`expr $ncurves0 + 3`
if [ $ncurves1 -gt 3 ] ; then
ncurves1_min=`expr $ncurves1 - 3`
else
ncurves1_min=0
fi
ncurves1_max=`expr $ncurves1 + 3`
I_min=`expr $I - 1`
I_max=`expr $I + 1`

### Replace parameters values in template
sed "s/lim0_def/$lim0/g" las_decl_template.py | \
sed "s/lim0_min/$lim0_min/g" | sed "s/lim0_max/$lim0_max/g" | \
sed "s/qmin_def/$qmin/g" | sed "s/qmin_min/$qmin_min/g" | \
sed "s/qmin_max/$qmin_max/g" | \
sed "s/bkthresh1_def/$bkthresh1/g" | sed "s/bkthresh1_min/$bkthresh1_min/g" | \
sed "s/bkthresh1_max/$bkthresh1_max/g" | \
sed "s/lim1_def/$lim1/g" | sed "s/lim1_min/$lim1_min/g" | \
sed "s/lim1_max/$lim1_max/g" | \
sed "s/lpb0_def/$lpb0/g" | sed "s/lpb0_min/$lpb0_min/g" | \
sed "s/lpb0_max/$lpb0_max/g" | \
sed "s/lpb1_def/$lpb1/g" | sed "s/lpb1_min/$lpb1_min/g" | \
sed "s/lpb1_max/$lpb1_max/g" | \
sed "s/mfb0_def/$mfb0/g" | sed "s/mfb0_min/$mfb0_min/g" | \
sed "s/mfb0_max/$mfb0_max/g" | \
sed "s/mfb1_def/$mfb1/g" | sed "s/mfb1_min/$mfb1_min/g" | \
sed "s/mfb1_max/$mfb1_max/g" | \
sed "s/ncurves0_def/$ncurves0/g" | sed "s/ncurves0_min/$ncurves0_min/g" | \
sed "s/ncurves0_max/$ncurves0_max/g" | \
sed "s/ncurves1_def/$ncurves1/g" | sed "s/ncurves1_min/$ncurves1_min/g" | \
sed "s/ncurves1_max/$ncurves1_max/g" | \
sed "s/I_def/$I/g" | sed "s/I_min/$I_min/g" | sed "s/I_max/$I_max/g" \
> $d/las_declaration.py
echo $d/las_declaration.py

### Go to working directory and execute las_optimize.py
cd $d
echo $d
python las_optimize.py

### Parse the solutions from nomad
# optimized parameters are in nomad-solution.nnn.txt
f=`ls -t nomad-solution.*.txt | head -1`
I_opt=`head -1 $f`
qmin_opt=`head -2 $f | tail -1`
lim0_opt=`head -3 $f | tail -1`
lim1_opt=`head -4 $f | tail -1`
bkthresh1_opt=`head -5 $f | tail -1`
lpb0_opt=`head -6 $f | tail -1`
lpb1_opt=`head -7 $f | tail -1`
mfb0_opt=`head -8 $f | tail -1`
mfb1_opt=`head -9 $f | tail -1`
ncurves0_opt=`head -10 $f | tail -1`
ncurves1_opt=`head -11 $f | tail -1`
echo "Optimal parameters:"
echo "lim0=" $lim0_opt " min=" $lim0_min " max=" $lim0_max
echo "lim1=" $lim1_opt " min=" $lim1_min " max=" $lim1_max
echo "lpb0=" $lpb0_opt " min=" $lpb0_min " max=" $lpb0_max
echo "lpb1=" $lpb1_opt " min=" $lpb1_min " max=" $lpb1_max
echo "mfb0=" $mfb0_opt " min=" $mfb0_min " max=" $mfb0_max
echo "mfb1=" $mfb1_opt " min=" $mfb1_min " max=" $mfb1_max
echo "ncurves0=" $ncurves0_opt " min=" $ncurves0_min " max=" $ncurves0_max
echo "ncurves1=" $ncurves1_opt " min=" $ncurves1_min " max=" $ncurves1_max
echo "I=" $I_opt " min=" $I_min " max=" $I_max
echo "qmin=" $qmin_opt " min=" $qmin_min " max=" $qmin_max
echo "bkthresh1=" $bkthresh1_opt " min=" $bkthresh1_min " max=" $bkthresh1_max
cd $cwd
sed "s/lim0.*=.*$/lim0 = $lim0_opt/g" $params | \
sed "s/lim1.*=.*$/lim1 = $lim1_opt/g" | \
sed "s/qmin.*=.*$/qmin = $qmin_opt/g" | \
sed "s/bkthresh1.*=.*$/bkthresh1 = $bkthresh1_opt/g" | \
sed "s/lpb0.*=.*$/lpb0 = $lpb0_opt/g" | \
sed "s/lpb1.*=.*$/lpb1 = $lpb1_opt/g" | \
sed "s/mfb0.*=.*$/mfb0 = $mfb0_opt/g" | \
sed "s/mfb1.*=.*$/mfb1 = $mfb1_opt/g" | \
sed "s/ncurves0.*=.*$/ncurves0 = $ncurves0_opt/g" | \
sed "s/ncurves1.*=.*$/ncurves1 = $ncurves1_opt/g" | \
sed "s/I.*=.*$/I = $I_opt/g" > $params.opt
if [ $has_qmin -eq 0 ] ; then
   echo "tasks.qmin = $qmin_opt" >> $params.opt
fi
if [ $has_bkthresh1 -eq 0 ] ; then
   echo "tasks.sieve.bkthresh1 = $bkthresh1_opt" >> $params.opt
fi
if [ $has_ncurves0 -eq 0 ] ; then
   echo "tasks.sieve.ncurves0 = $ncurves0_opt" >> $params.opt
fi
if [ $has_ncurves1 -eq 0 ] ; then
   echo "tasks.sieve.ncurves1 = $ncurves1_opt" >> $params.opt
fi
# /bin/rm -fr $d
