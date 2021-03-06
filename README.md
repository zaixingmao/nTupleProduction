####cmssw/cvs
```bash
scram project CMSSW_5_3_15
cd CMSSW_5_3_15/src
cmsenv

git clone https://github.com/zaixingmao/nTupleProduction.git

git clone https://github.com/elaird/uwa.git UWAnalysis
cd UWAnalysis

# http://cms-sw.github.io/faq.html#how-do-i-access-the-old-cvs-repository-to-check-what-was-really-there
kinit ${USER}@CERN.CH
export CVSROOT=":ext:${USER}@lxplus.cern.ch:/afs/cern.ch/user/c/cvscmssw/public/CMSSW"
export CVS_RSH=ssh
cd ..
UWAnalysis/recipe53X_v2.sh

cd nTupleProduction
source changeFiles.sh
cd ..
```

####build
```bash
export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=maybe-uninitialized"
#export USER_CXXFLAGS="${USER_CXXFLAGS} -Wno-error=sign-compare -Wno-error=reorder"
scram b -j 8
```

####run
```bash
cd UWAnalysis/CRAB/LTau
```

edit `SUB-TT.py` and `SUB-TT-data.py`, e.g.
```python
shift = 'tau'
embedded=True
```

```bash
# to test
cmsRun SUB-TT.py

# to submit jobs
source sub.sh
```

####TMVA Setup
```bash
cd CMSSW_5_3_15/src
wget http://sourceforge.net/projects/tmva/files/TMVA-v4.2.0.tgz
tar xfz TMVA-v4.2.0.tgz
cp -r ./nTupleProduction/TMVA-v4.2.0/test ./TMVA-v4.2.0
cd TMVA-v4.2.0/
make
cd test
source setup.sh #you need to do this before using any TMVA related training
```