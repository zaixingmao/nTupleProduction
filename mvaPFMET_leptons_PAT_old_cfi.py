import FWCore.ParameterSet.Config as cms

# 
# isomuons = cms.EDFilter("PATMuonSelector",
#   				src = cms.InputTag("cleanPatMuons"),
#   				cut = cms.string('pt>10&&' +
#   								'abs(eta)<2.4&&' +
#   								'userInt("tightID")>0&&' +
#   								'abs(userFloat("dz"))<0.2&&' +
#   								'abs(userFloat("ipDXY"))<0.045&&' +
#   								'isGlobalMuon&&' +
#   								'(userIso(0)+max(photonIso+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()<0.3'
#   								),
#   				filter = cms.bool(False)
#   				)
# 
# isoelectrons = cms.EDFilter("PATElectronSelector",
# 				src = cms.InputTag("cleanPatElectrons"),
# 				cut = cms.string('pt>10&&' +
# 								 'abs(eta)<2.5&&' +
# 								 'userInt("mvaidwp")>0&&' +
# 								 'abs(userFloat("dz"))<0.2&&' +
# 								 'abs(userFloat("ipDXY"))<0.045&&' +
# 								 '(!(userInt("HasMatchedConversion")>0))&&' +
# 								 'userInt("missingHits")==0&&' +
# 								 '(userIso(0)+max(userIso(1)+neutralHadronIso()-0.5*userIso(2),0.0))/pt()<0.3'
# 								 ),
# 				filter = cms.bool(False)
#   				)
  										
isomuons = cms.EDFilter(
        "PATMuonSelector",
            src = cms.InputTag("cleanPatMuons"),
        cut = cms.string(    "(isTrackerMuon) && abs(eta) < 2.5 && pt > 9.5"+#17. "+
                             "&& isPFMuon"+
                             "&& globalTrack.isNonnull"+
                             "&& innerTrack.hitPattern.numberOfValidPixelHits > 0"+
                             "&& innerTrack.normalizedChi2 < 10"+
                             "&& numberOfMatches > 0"+
                             "&& innerTrack.hitPattern.numberOfValidTrackerHits>5"+
                             "&& globalTrack.hitPattern.numberOfValidHits>0"+
#                             "&& (isolationR03.sumPt/pt) < 0.2"+
                             "&& (pfIsolationR03.sumChargedHadronPt+pfIsolationR03.sumNeutralHadronEt+pfIsolationR03.sumPhotonEt)/pt < 0.3"+
                             "&& abs(innerTrack().dxy)<2.0"
                             ),
        filter = cms.bool(False)
        )

isoelectrons = cms.EDFilter(
    "PATElectronSelector",
            src = cms.InputTag("cleanPatElectrons"),
            cut = cms.string(
            "abs(eta) < 2.5 && pt > 9.5"                               +
            "&& gsfTrack.trackerExpectedHitsInner.numberOfHits == 0"   +
            #"&& (pfIsolationVariables.chargedHadronIso)/et  < 0.2"     +
            "&& (isolationVariables03.tkSumPt)/et              < 0.2"  +
            "&& ((abs(eta) < 1.4442  "                                 +
            "&& abs(deltaEtaSuperClusterTrackAtVtx)            < 0.007"+
            "&& abs(deltaPhiSuperClusterTrackAtVtx)            < 0.8"  +
            "&& sigmaIetaIeta                                  < 0.01" +
            "&& hcalOverEcal                                   < 0.15" +
            "&& abs(1./superCluster.energy - 1./p)             < 0.05)" +
            "|| (abs(eta)  > 1.566 "+
            "&& abs(deltaEtaSuperClusterTrackAtVtx)            < 0.009"+
            "&& abs(deltaPhiSuperClusterTrackAtVtx)            < 0.10" +
            "&& sigmaIetaIeta                                  < 0.03" +
            "&& hcalOverEcal                                   < 0.10" +
            "&& abs(1./superCluster.energy - 1./p)             < 0.05))" 
            ),
        filter = cms.bool(False)
        )

isotaus = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("cleanPatTaus"),
    cut = cms.string('pt > 19 &&' +
    				 ' abs(eta) < 2.3 &&' +
    				 ' tauID("decayModeFinding") &&' +
    				 ' tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")<1.5 &&' +
    				 ' tauID("againstElectronLoose") &&' +
    				 ' tauID("againstMuonLoose2")'
    				 ),
    filter = cms.bool(False)
)

isomuonseq     = cms.Sequence(isomuons)
isoelectronseq = cms.Sequence(isoelectrons)
isotauseq      = cms.Sequence(isotaus)

leptonSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring(
    'isomuonseq',
    'isoelectronseq',
    'isotauseq')
    )
    )


