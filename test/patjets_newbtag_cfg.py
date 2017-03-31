import FWCore.ParameterSet.Config as cms

process = cms.Process("Diagnosis")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100000)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v8')

## Options and Output Report
process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )

## TFileService
output_file = 'histograms_patjets.root'
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(output_file)
)

# Updating jet collection

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
## b-tag discriminators
bTagDiscriminators = [
    'deepFlavourJetTags:probudsg',
    'deepFlavourJetTags:probb',
    'deepFlavourJetTags:probc',
    'deepFlavourJetTags:probbb',
    'deepFlavourJetTags:probcc',
]

## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets','','PAT'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators,
)


## ============ TRIGGER FILTER =============== 
## Enable below at cms.Path if needed 
process.trigger = cms.EDFilter( "TriggerResultsFilter",
    triggerConditions = cms.vstring('HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v*'),
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
    l1tResults = cms.InputTag( "" ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( False ),
    daqPartitions = cms.uint32( 1 ),
    throw = cms.bool( False )
)


process.patjets = cms.EDAnalyzer('PatJets',
   PatJets = cms.InputTag("selectedUpdatedPatJets"),
   PTMin = cms.double(-1),
   BTag = cms.string("deepFlavourJetTags:probb"),
)

process.p = cms.Path(
                     process.patjets 
                     )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)




readFiles.extend( [
       '/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToBB_NarrowWidth_M-120_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/2E5CD97C-DEC6-E611-9334-002590DE6E22.root',
] );


secFiles.extend( [
       ] )


# 
# ## ============ JSON Certified data ===============   BE CAREFUL!!!
# ## Don't use with CRAB!!!
# import FWCore.PythonUtilities.LumiList as LumiList
# import FWCore.ParameterSet.Types as CfgTypes
# process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
# JSONfile = 'json.txt'
# myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
# process.source.lumisToProcess.extend(myLumis)
