import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Diagnosis")

options = VarParsing.VarParsing ('analysis')
options.inputFiles =  '/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/SKIM/mc/2017/Neutrino/83x/L1Menu_Collisions2017_dev_r2/PU53to57/SingleNeutrino/Neutrino83x/170511_093734/0000/L1REPACK_FullMC_SKIM_99.root',
#options.inputFiles =  '/store/data/Run2016H/BTagCSV/MINIAOD/PromptReco-v2/000/282/800/00000/C812D088-0291-E611-832C-FA163EE3836A.root',
#options.inputFiles =  '/store/mc/RunIISummer16DR80/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/130000/08C6F278-E0A2-E611-BE0C-002590D9DA9C.root',
options.parseArguments()

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.source = cms.Source ("PoolSource",
                             fileNames      = cms.untracked.vstring (options.inputFiles),
                             )

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2017_TSG_Hcal_V3')

process.triggerinfo = cms.EDAnalyzer('TriggerInfo',
   PathName = cms.string("HLT_AK8PFHT750_TrimMass50_v1"),
   TriggerResults = cms.InputTag("TriggerResults","","SIM"),
   TriggerObjectsStandAlone  = cms.InputTag("selectedPatTrigger","","PAT"),
)


process.p = cms.Path(process.triggerinfo)

