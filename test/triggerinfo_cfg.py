import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Diagnosis")

options = VarParsing.VarParsing ('analysis')
options.inputFiles =  '/store/data/Run2017C/BTagCSV/MINIAOD/PromptReco-v1/000/299/368/00000/7ED71BDC-8D6D-E711-A6CE-02163E014491.root',
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
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v8')

process.triggerinfo = cms.EDAnalyzer('TriggerInfo',
   PathName = cms.string("HLT_Mu8_v8"),
   TriggerResults = cms.InputTag("TriggerResults","","HLT"),
   TriggerObjectsStandAlone  = cms.InputTag("selectedPatTrigger","","PAT"),
)


process.p = cms.Path(process.triggerinfo)

