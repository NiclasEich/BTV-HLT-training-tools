###
#
# Quick script to match btaganalyzer (bta) and deepntuplizer (dnt) jets
# Not efficient, made for O(100) events (236 jets in dnt, 539 in bta)
# date: 2020-09-18
#
###

# TODO: - run DeepCSV in DJC on small_deepntuplizer.root
#	- get probb and probbb from the resulting tree (uhh friend, in bta it is probb+probbb)
#	- do plotting (2D)
#	- also save not matched jets -> get an idea why there are so many more jets in bta than in dnt

from ROOT import *
import sys

f_bta = TFile("JetTree_mc.root")
###f_dnt = TFile("small_deepntuples_merged.root")
f_dnt = TFile("pred_ntuple_merged_0.root")

t_bta = f_bta.Get("btagana/ttree")
t_dnt = f_dnt.Get("tree")
###t_dnt = f_dnt.Get("deepntuplizer/tree")
###t_dnt.AddFriend("tree","small_deepntuples_merged_predicted.root")

#t_dnt.Print()
#sys.exit()

ne_bta = t_bta.GetEntries()
nj_dnt = t_dnt.GetEntries()

print(ne_bta)
print(nj_dnt)

# matching values
# resolve ambiguity: sum(deta, dphi) smaller, then dpt smaller
mm_deta = 0.01
mm_dphi = 0.01
mm_dpt = 5

# for identification
is_bta = []
es_bta = []

# storing
store_bta_pt = []
store_bta_eta = []
store_bta_phi = []
store_bta_evtno = []
store_bta_DeepCSVBDisc = []

store_dnt_pt = []
store_dnt_eta = []
store_dnt_phi = []
store_dnt_evtno = []

# have to take these from the predition tree (TODO)
store_dnt_probb = []
store_dnt_probbb = []
store_dnt_probbb_sum = []

# loop over deepntuplizer (less jets)
# JET loop
i_dnt = 0
i_bta = 0
e_bta = 0 # unique identifier needs also event number for bta
for dnt_entry in t_dnt:
  if (i_dnt % 20 == 0): print("DeepNtuplizer entry: "+str(i_dnt) )

  jet_pt_dnt = dnt_entry.jet_pt
#  jet_pt_dnt = dnt_entry.jet_corr_pt
  jet_eta_dnt = dnt_entry.jet_eta
  jet_probb_dnt = dnt_entry.prob_isB
  jet_probbb_dnt = dnt_entry.prob_isBB
###  jet_phi_dnt = dnt_entry.jet_phi
###  jet_evtno_dnt = dnt_entry.event_no

  if(jet_pt_dnt < 20.):
    continue

  # min values for matching
  min_dpt  = 1000.
  min_dphi = 1000.
  min_deta = 1000.
  matched = False
  matched_i_bta = -1
  matched_e_bta = -1
  matched_bta_jet_pt   = -999
  matched_bta_jet_eta  = -999
  matched_bta_jet_phi  = -999
  matched_bta_jet_disc = -999
  matched_bta_evtno = -999


  # loop over btaganalyzer (more jets)
  # EVENT loop
  e_bta=0
  for bta_event in t_bta:
    jet_pt_bta_ev = bta_event.Jet_uncorrpt
    jet_eta_bta_ev = bta_event.Jet_eta
###    jet_phi_bta_ev = bta_event.Jet_phi
    jet_evtno_bta_ev = bta_event.Evt
    jet_disc_bta_ev = bta_event.Jet_DeepCSVBDisc

    # sanity checks
    if (len(jet_pt_bta_ev)  != len(jet_eta_bta_ev)): print("jet_pt_bta_ev    and    jet_eta_bta_ev   not the same length")
###    if (len(jet_pt_bta_ev)  != len(jet_phi_bta_ev)): print("jet_pt_bta_ev    and    jet_phi_bta_ev   not the same length")
###    if (len(jet_phi_bta_ev) != len(jet_eta_bta_ev)): print("jet_phi_bta_ev   and    jet_eta_bta_ev   not the same length")

    # JET loop
    n_jets_bta_ev = len(jet_pt_bta_ev)
    i_bta=0
    for jet_bta in range(n_jets_bta_ev):
      jet_pt_bta = jet_pt_bta_ev[jet_bta]
      jet_eta_bta = jet_eta_bta_ev[jet_bta]
###      jet_phi_bta = jet_phi_bta_ev[jet_bta]
      jet_disc_bta = jet_disc_bta_ev[jet_bta]

      # now matching
      dpt = abs(jet_pt_bta  - jet_pt_dnt )
      deta= abs(jet_eta_bta - jet_eta_dnt)
###      dphi= abs(jet_phi_bta - jet_phi_dnt)
###      if ( (dpt <= mm_dpt) and (deta <= mm_deta) and dphi <= (mm_dphi) ):
      if ( (dpt <= mm_dpt) and (deta <= mm_deta) ):
        if(matched): # ambiguous
###          if( (deta+dphi) < (min_deta + min_dphi) and (dpt < min_dpt) ): # update
          if( (deta) < (min_deta) and (dpt < min_dpt) ): # update
            min_deta = deta
###            min_dphi = dphi
            min_dpt = dpt
            matched_i_bta = i_bta
            matched_e_bta = e_bta
            matched_bta_jet_pt = jet_pt_bta
            matched_bta_jet_eta = jet_eta_bta
###            matched_bta_jet_phi = jet_phi_bta
            matched_bta_jet_disc = jet_disc_bta
            matched_bta_evtno = jet_evtno_bta_ev
        else: # first match
          matched = True
          min_deta = deta
###          min_dphi = dphi
          min_dpt = dpt
          matched_i_bta = i_bta
          matched_e_bta = e_bta
          matched_bta_jet_pt = jet_pt_bta
          matched_bta_jet_eta = jet_eta_bta
###          matched_bta_jet_phi = jet_phi_bta
          matched_bta_jet_disc = jet_disc_bta
          matched_bta_evtno = jet_evtno_bta_ev


#        if (i_dnt % 20 == 0):
#          print "pt:", jet_pt_bta, jet_pt_dnt, min_dpt
#          print "eta:", jet_eta_bta, jet_eta_dnt, min_deta
#          print "phi:", jet_phi_bta, jet_phi_dnt, min_dphi
 
      i_bta+=1
      # end jet loop bta

    e_bta+=1
    # end event loop bta

  # check if was matched before
  if ( (matched_i_bta in is_bta) ):
    if( matched_e_bta == es_bta[is_bta.index(matched_i_bta)]):
      print("ohoh!", matched_i_bta, matched_e_bta) 
      print "pt:", jet_pt_bta, jet_pt_dnt, min_dpt
      print "eta:", jet_eta_bta, jet_eta_dnt, min_deta
###      print "phi:", jet_phi_bta, jet_phi_dnt, min_dphi

  store_bta_pt.append(matched_bta_jet_pt)
  store_bta_eta.append(matched_bta_jet_eta)
###  store_bta_phi.append(matched_bta_jet_phi)
  store_bta_evtno.append(matched_bta_evtno)
  store_bta_DeepCSVBDisc.append(matched_bta_jet_disc)


  store_dnt_pt.append(jet_pt_dnt)
  store_dnt_eta.append(jet_eta_dnt)
  store_dnt_probb.append(jet_probb_dnt)
  store_dnt_probbb.append(jet_probbb_dnt)
  store_dnt_probbb_sum.append(jet_probbb_dnt+jet_probb_dnt)
###  store_dnt_phi.append(jet_phi_dnt)
###  store_dnt_evtno.append(jet_evtno_dnt)
  i_dnt+=1
  # end jet loop dnt

  # the unique bta IDs
  is_bta.append(matched_i_bta)
  es_bta.append(matched_e_bta)

  if (not matched):
    print("NOT MATCHED!!!!!!!")
#    sys.exit()
  if (i_dnt % 20 == 0):
    print("matched: " + str(matched))

#print len(is_bta), is_bta
#print len(es_bta), es_bta

###header_list = ['uncor bta_pt', 'uncor dnt_pt', 'bta_eta', 'dnt_eta', 'bta_phi', 'dnt_phi', 'bta_evtno', 'dnt_evtno','bta_deepcsv']
#header_list = ['uncor bta_pt', 'uncor dnt_pt', 'bta_eta', 'dnt_eta', 'bta_evtno', 'bta_deepcsv', 'dnt_probbb_sum', 'dnt_probb', 'dnt_probbb']
header_list = ['uncor bta_pt', 'uncor dnt_pt', 'bta_eta', 'dnt_eta', 'bta_evtno', 'bta_deepcsv', 'dnt_probb_probbb', 'delta_bta_dnt']
row_format ="{:>20}" * (len(header_list))
print(row_format.format(*header_list))
###for data in zip(store_bta_pt, store_dnt_pt, store_bta_eta, store_dnt_eta, store_bta_phi, store_dnt_phi, store_bta_evtno, store_dnt_evtno, store_bta_DeepCSVBDisc):
#for data in zip(store_bta_pt, store_dnt_pt, store_bta_eta, store_dnt_eta, store_bta_evtno, store_bta_DeepCSVBDisc, store_dnt_probbb_sum, store_dnt_probb, store_dnt_probbb):
for data in zip(store_bta_pt, store_dnt_pt, store_bta_eta, store_dnt_eta, store_bta_evtno, store_bta_DeepCSVBDisc, store_dnt_probbb_sum, [a_i - b_i for a_i, b_i in zip(store_bta_DeepCSVBDisc, store_dnt_probbb_sum)]):
  print(row_format.format(*data))

#sys.exit()

f_out = TFile("small_comparison.root","RECREATE")
hpxpy  = TH2F( 'hpxpy', 'bta vs dnt', 100, 0, 1, 100, 0, 1 )
for i in range(len(store_dnt_probbb_sum)):
  hpxpy.Fill(store_bta_DeepCSVBDisc[i], store_dnt_probbb_sum[i])

hpxpy.SetDirectory(f_out)
hpxpy.Write()
f_out.Close()

