global_branches = ['jet_pt', 'jet_eta',
'nCpfcand','nNpfcand',
'nsv','npv',
'TagVarCSV_trackSumJetEtRatio',
'TagVarCSV_trackSumJetDeltaR',
'TagVarCSV_vertexCategory',
'TagVarCSV_trackSip2dValAboveCharm',
'TagVarCSV_trackSip2dSigAboveCharm',
'TagVarCSV_trackSip3dValAboveCharm',
'TagVarCSV_trackSip3dSigAboveCharm',
'TagVarCSV_jetNSelectedTracks',
'TagVarCSV_jetNTracksEtaRel']

cpf_branches = ['Cpfcan_BtagPf_trackEtaRel',
'Cpfcan_BtagPf_trackPtRel',
'Cpfcan_BtagPf_trackPPar',
'Cpfcan_BtagPf_trackDeltaR',
'Cpfcan_BtagPf_trackPParRatio',
'Cpfcan_BtagPf_trackSip2dVal',
'Cpfcan_BtagPf_trackSip2dSig',
'Cpfcan_BtagPf_trackSip3dVal',
'Cpfcan_BtagPf_trackSip3dSig',
'Cpfcan_BtagPf_trackJetDistVal',
'Cpfcan_ptrel',
'Cpfcan_drminsv',
'Cpfcan_VTX_ass',
'Cpfcan_puppiw',
'Cpfcan_chi2',
'Cpfcan_quality']
n_cpf = 25

npf_branches = ['Npfcan_ptrel','Npfcan_deltaR','Npfcan_isGamma','Npfcan_HadFrac','Npfcan_drminsv','Npfcan_puppiw']
n_npf = 25

vtx_branches = ['sv_pt','sv_deltaR',
'sv_mass',
'sv_ntracks',
'sv_chi2',
'sv_normchi2',
'sv_dxy',
'sv_dxysig',
'sv_d3d',
'sv_d3dsig',
'sv_costhetasvpv',
'sv_enratio',
]

n_vtx = 4

reduced_truth = ['isB','isBB','isLeptonicB','isC','isUDS','isG']

DeepFlavour_all_branches = global_branches + cpf_branches + vtx_branches


"""
DeepCSV
"""

DeepCSV_global_branches = ['jet_pt', 'jet_eta',
                            'TagVarCSV_jetNSecondaryVertices', 
                            'TagVarCSV_trackSumJetEtRatio',
                            'TagVarCSV_trackSumJetDeltaR',
                            'TagVarCSV_vertexCategory',
                            'TagVarCSV_trackSip2dValAboveCharm',
                            'TagVarCSV_trackSip2dSigAboveCharm',
                            'TagVarCSV_trackSip3dValAboveCharm',
                            'TagVarCSV_trackSip3dSigAboveCharm',
                            'TagVarCSV_jetNSelectedTracks',
                            'TagVarCSV_jetNTracksEtaRel']

DeepCSV_track_branches = ['TagVarCSVTrk_trackJetDistVal',
                          'TagVarCSVTrk_trackPtRel', 
                          'TagVarCSVTrk_trackDeltaR', 
                          'TagVarCSVTrk_trackPtRatio', 
                          'TagVarCSVTrk_trackSip3dSig', 
                          'TagVarCSVTrk_trackSip2dSig', 
                          'TagVarCSVTrk_trackDecayLenVal']

DeepCSV_eta_rel_branches = ['TagVarCSV_trackEtaRel']

DeepCSV_vtx_branches = ['TagVarCSV_vertexMass', 
                          'TagVarCSV_vertexNTracks', 
                          'TagVarCSV_vertexEnergyRatio',
                          'TagVarCSV_vertexJetDeltaR',
                          'TagVarCSV_flightDistance2dVal', 
                          'TagVarCSV_flightDistance2dSig', 
                          'TagVarCSV_flightDistance3dVal', 
                          'TagVarCSV_flightDistance3dSig']

DeepCSV_all_branches = DeepCSV_global_branches + DeepCSV_track_branches + DeepCSV_eta_rel_branches + DeepCSV_vtx_branches

new_ntuple_keys =  ['PuppiJet.Jet_pt',
                     'PuppiJet.Jet_eta',
                     'PuppiJet.TagVarCSV_jetNSecondaryVertices',
                     'PuppiJet.TagVarCSV_trackSumJetEtRatio',
                     'PuppiJet.TagVarCSV_trackSumJetDeltaR',
                     'PuppiJet.TagVarCSV_vertexCategory',
                     'PuppiJet.TagVarCSV_trackSip2dValAboveCharm',
                     'PuppiJet.TagVarCSV_trackSip2dSigAboveCharm',
                     'PuppiJet.TagVarCSV_trackSip3dValAboveCharm',
                     'PuppiJet.TagVarCSV_trackSip3dSigAboveCharm',
                     'PuppiJet.TagVarCSV_jetNTracksEtaRel',
                     'PuppiJet.TagVarCSV_trackEtaRel',
                     'PuppiJet.TagVarCSV_vertexMass',
                     'PuppiJet.TagVarCSV_vertexNTracks',
                     'PuppiJet.TagVarCSV_vertexEnergyRatio',
                     'PuppiJet.TagVarCSV_vertexJetDeltaR',
                     'PuppiJet.TagVarCSV_flightDistance2dVal',
                     'PuppiJet.TagVarCSV_flightDistance2dSig',
                     'PuppiJet.TagVarCSV_flightDistance3dVal',
                     'PuppiJet.TagVarCSV_flightDistance3dSig',
                     'PuppiJet.TagVarCSV_trackDecayLenVal',
                     'PuppiJet.TagVarCSV_trackSip2dSig',
                     'PuppiJet.TagVarCSV_trackSip3dSig',
                     'PuppiJet.TagVarCSV_trackPtRatio',
                     'PuppiJet.TagVarCSV_trackDeltaR',
                     'PuppiJet.TagVarCSV_jetNTracks',
                     'PuppiJet.TagVarCSV_trackPtRel',
                     'PuppiJet.TagVarCSV_trackJetDistVal',
                     'PuppiJet.Jet_isB',
                     'PuppiJet.Jet_isBB',
                     'PuppiJet.Jet_isGBB',
                     'PuppiJet.Jet_isLeptonicB',
                     'PuppiJet.Jet_isLeptonicB_C',
                     'PuppiJet.Jet_isC',
                     'PuppiJet.Jet_isGCC',
                     'PuppiJet.Jet_isCC',
                     'PuppiJet.Jet_isUD',
                     'PuppiJet.Jet_isS',
                     'PuppiJet.Jet_isG',
                     'PuppiJet.Jet_isG',
                     'PuppiJet.Jet_isUndefined',
                     'PuppiJet.Jet_DeepFlavourBDisc',
                     'PuppiJet.Jet_DeepFlavourCvsLDisc',
                     'PuppiJet.Jet_DeepFlavourCvsBDisc',
                     'PuppiJet.Jet_DeepFlavourB',
                     'PuppiJet.Jet_DeepFlavourBB',
                     'PuppiJet.Jet_DeepFlavourLEPB',
                     'PuppiJet.Jet_DeepFlavourC',
                     'PuppiJet.Jet_DeepFlavourUDS',
                     'PuppiJet.Jet_DeepFlavourG',
                     'PuppiJet.Jet_DeepCSVBDisc',
                     'PuppiJet.Jet_DeepCSVBDiscN',
                     'PuppiJet.Jet_DeepCSVCvsLDisc',
                     'PuppiJet.Jet_DeepCSVCvsLDiscN',
                     'PuppiJet.Jet_DeepCSVCvsBDisc',
                     'PuppiJet.Jet_DeepCSVCvsBDiscN',
                     'PuppiJet.Jet_DeepCSVb',
                     'PuppiJet.Jet_DeepCSVc',
                     'PuppiJet.Jet_DeepCSVl',
                     'PuppiJet.Jet_DeepCSVbb',
                     'PuppiJet.Jet_DeepCSVcc',
                     'PuppiJet.Jet_DeepCSVbN',
                     'PuppiJet.Jet_DeepCSVcN',
                     'PuppiJet.Jet_DeepCSVlN',
                     'PuppiJet.Jet_DeepCSVbbN',
                     'PuppiJet.Jet_DeepCSVccN',
                     'Jet_pt',
                     'Jet_eta',
                     'TagVarCSV_jetNSecondaryVertices',
                     'TagVarCSV_trackSumJetEtRatio',
                     'TagVarCSV_trackSumJetDeltaR',
                     'TagVarCSV_vertexCategory',
                     'TagVarCSV_trackSip2dValAboveCharm',
                     'TagVarCSV_trackSip2dSigAboveCharm',
                     'TagVarCSV_trackSip3dValAboveCharm',
                     'TagVarCSV_trackSip3dSigAboveCharm',
                     'TagVarCSV_jetNTracksEtaRel',
                     'TagVarCSV_trackEtaRel',
                     'TagVarCSV_vertexMass',
                     'TagVarCSV_vertexNTracks',
                     'TagVarCSV_vertexEnergyRatio',
                     'TagVarCSV_vertexJetDeltaR',
                     'TagVarCSV_flightDistance2dVal',
                     'TagVarCSV_flightDistance2dSig',
                     'TagVarCSV_flightDistance3dVal',
                     'TagVarCSV_flightDistance3dSig',
                     'TagVarCSV_trackDecayLenVal',
                     'TagVarCSV_trackSip2dSig',
                     'TagVarCSV_trackSip3dSig',
                     'TagVarCSV_trackPtRatio',
                     'TagVarCSV_trackDeltaR',
                     'TagVarCSV_jetNTracks',
                     'TagVarCSV_trackPtRel',
                     'TagVarCSV_trackJetDistVal',
                     'Jet_isUndefined',
                     'Jet_isB',
                     'Jet_isBB',
                     'Jet_isGBB',
                     'Jet_isLeptonicB',
                     'Jet_isLeptonicB_C',
                     'Jet_isC',
                     'Jet_isGCC',
                     'Jet_isCC',
                     'Jet_isUD',
                     'Jet_isG',
                     'Jet_isS',
                     'Jet_DeepFlavourBDisc',
                     'Jet_DeepFlavourCvsLDisc',
                     'Jet_DeepFlavourCvsBDisc',
                     'Jet_DeepFlavourB',
                     'Jet_DeepFlavourBB',
                     'Jet_DeepFlavourLEPB',
                     'Jet_DeepFlavourC',
                     'Jet_DeepFlavourUDS',
                     'Jet_DeepFlavourG',
                     'Jet_DeepCSVBDisc',
                     'Jet_DeepCSVBDiscN',
                     'Jet_DeepCSVCvsLDisc',
                     'Jet_DeepCSVCvsLDiscN',
                     'Jet_DeepCSVCvsBDisc',
                     'Jet_DeepCSVCvsBDiscN',
                     'Jet_DeepCSVb',
                     'Jet_DeepCSVc',
                     'Jet_DeepCSVl',
                     'Jet_DeepCSVbb',
                     'Jet_DeepCSVcc',
                     'Jet_DeepCSVbN',
                     'Jet_DeepCSVcN',
                     'Jet_DeepCSVlN',
                     'Jet_DeepCSVbbN',
                     'Jet_DeepCSVccN']


key_lookup = {'jet_pt': 'Jet_pt',
        'jet_eta': 'Jet_eta',
        'TagVarCSV_jetNSecondaryVertices': 'TagVarCSV_jetNSecondaryVertices',
        'TagVarCSV_trackSumJetEtRatio': 'TagVarCSV_trackSumJetEtRatio',
        'TagVarCSV_trackSumJetDeltaR': 'TagVarCSV_trackSumJetDeltaR',
        'TagVarCSV_vertexCategory': 'TagVarCSV_vertexCategory',
        'TagVarCSV_trackSip2dValAboveCharm': 'TagVarCSV_trackSip2dValAboveCharm',
        'TagVarCSV_trackSip2dSigAboveCharm': 'TagVarCSV_trackSip2dSigAboveCharm',
        'TagVarCSV_trackSip3dValAboveCharm': 'TagVarCSV_trackSip3dValAboveCharm',
        'TagVarCSV_trackSip3dSigAboveCharm': 'TagVarCSV_trackSip3dSigAboveCharm',
        'TagVarCSV_jetNTracksEtaRel': 'TagVarCSV_jetNTracksEtaRel',
        'TagVarCSV_trackEtaRel': 'TagVarCSV_trackEtaRel',
        'TagVarCSV_vertexMass': 'TagVarCSV_vertexMass',
        'TagVarCSV_vertexNTracks': 'TagVarCSV_vertexNTracks',
        'TagVarCSV_vertexEnergyRatio': 'TagVarCSV_vertexEnergyRatio',
        'TagVarCSV_vertexJetDeltaR': 'TagVarCSV_vertexJetDeltaR',
        'TagVarCSV_flightDistance2dVal': 'TagVarCSV_flightDistance2dVal',
        'TagVarCSV_flightDistance2dSig': 'TagVarCSV_flightDistance2dSig',
        'TagVarCSV_flightDistance3dVal': 'TagVarCSV_flightDistance3dVal',
        'TagVarCSV_flightDistance3dSig': 'TagVarCSV_flightDistance3dSig',
        'TagVarCSVTrk_trackDecayLenVal': 'TagVarCSV_trackDecayLenVal',
        'TagVarCSVTrk_trackSip2dSig': 'TagVarCSV_trackSip2dSig',
        'TagVarCSVTrk_trackSip3dSig': 'TagVarCSV_trackSip3dSig',
        'TagVarCSVTrk_trackPtRatio': 'TagVarCSV_trackPtRatio',
        'TagVarCSVTrk_trackDeltaR': 'TagVarCSV_trackDeltaR',
        'TagVarCSV_jetNSelectedTracks': 'TagVarCSV_jetNTracks',
        'TagVarCSVTrk_trackPtRel': 'TagVarCSV_trackPtRel',
        'TagVarCSVTrk_trackJetDistVal': 'TagVarCSV_trackJetDistVal',
        'isB': 'Jet_isB',
        'isBB': 'Jet_isBB',
        'isGBB': 'Jet_isGBB',
        'isLeptonicB': 'Jet_isLeptonicB',
        'isLeptonicB_C': 'Jet_isLeptonicB_C',
        'isC': 'Jet_isC',
        'isGCC': 'Jet_isGCC',
        'isCC': 'Jet_isCC',
        'isUD': 'Jet_isUD',
        'isS': 'Jet_isS',
        'isG': 'Jet_isG',
        }


file_comparison = [ {"QCD_PT_470to600": ( ["/eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_Pt470to600_14TeV_PU140_HLT_TRKv06p1_TICL_cutsV2.root", "/eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_Pt470to600_14TeV_PU200_HLT_TRKv06p1_TICL_cutsV2.root"], ["/eos/cms/store/group/phys_btag/HLTRetraining/offline_training_files/QCD_Pt_470to600_TuneCP5_14TeV_pythia8.root"])
    },
    {"TT_TuneCP5_14TeV-powheg-pythia8": ( ["eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv00_TICL/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_TICL_default.root"], ["/eos/cms/store/group/phys_btag/HLTRetraining/offline_training_files/TT_TuneCP5_14TeV-powheg-pythia8.root"])}
    ]

