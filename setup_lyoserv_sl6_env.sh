#! /bin/bash

echo "Sourcing root"
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/lcg/root/5.34.07-cms/bin/thisroot.sh

echo "Sourcing gcc / gdb / python / boost"
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/xrootd/3.2.4-cms4/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/gcc/4.7.2-cms/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/gdb/7.6-cms/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/python/2.7.3-cms5/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/boost/1.51.0-cms5/etc/profile.d/init.sh

export BOOST_ROOT