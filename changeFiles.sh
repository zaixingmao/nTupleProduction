D=${CMSSW_BASE}/src/JetMETCorrections/METPUSubtraction

cp mvaPFMET_cff.py ${D}/python/
cp mvaPFMET_leptons_cff.py ${D}/python/
cp mvaPFMET_leptons_data_cff.py ${D}/python/
cp mvaPFMET_leptons_PAT_cfi.py ${D}/python/
cp mvaPFMET_leptons_PAT_old_cfi.py ${D}/python/
cp PFMETAlgorithmMVA.cc ${D}/src/

cp classes.h ${D}/src/
cp classes_def.xml ${D}/src/
cp MVAMETPairProducer.cc ${D}/plugins/
cp MVAMETPairProducer.hh ${D}/plugins/
cp BuildFile.xml ${D}/
