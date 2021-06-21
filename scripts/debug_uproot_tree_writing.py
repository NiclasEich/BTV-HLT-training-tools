import numpy as np
import awkward as ak
import uproot3 as ur
import root_numpy as rn

print("Version:\nuproot: {}\nawkward: {}\nroot_numpy: {}".format(ur.__version__, ak.__version__, rn.__version__))

f_path = "/tmp/test_uproot_writing.root"
# keys = ["key_a", "key_b", "key_c"]
keys = ["key-a"]

branch_dict = {}
branch_reg = {}

print("Creating New root-file with uproot")

with ur.recreate( f_path ) as out_file:
    # for key in keys:

        # arr = ak.to_awkward0( ak.Array( [np.zeros( (20))[:np.random.randint(4, 20)] for i in range(100)] ) )

        # dtype = ur.newbranch( np.dtype("f8"), size="{}-counts".format(key) )

        # counts = arr.counts
        # branch_dict["{}-counts".format(key)] = counts

        # branch_reg[key] = dtype
        # branch_dict[key] = arr


    # out_file["ttree"] = ur.newtree(branch_reg)
    # out_file["ttree"].extend(branch_dict)
    arr = ak.to_awkward0( ak.Array([np.zeros( (20), dtype=np.dtype("f8"))[:np.random.randint(4, 20)] for i in range(100)] ) )
    # arr = ak.to_awkward0( ak.Array( [np.zeros( (20)) for i in range(100)] ) )
    # arr = ak.to_awkward0(  [np.zeros( (20), np.dtype("f4")) for i in range(100)] )
    # arr = ak.to_awkward0(  [np.zeros( (20), np.dtype("f4")) for i in range(100)] )
    # from IPython import embed;embed()

    out_file["ttree"] = ur.newtree( {"key-a": ur.newbranch(np.dtype("f8"), size="n")})
    out_file["ttree"].extend({"key-a": arr, "n": arr.counts})

    # out_file["ttree"] = ur.newtree( {"key-a": np.float32})
    # out_file["ttree"].extend( {"key-a": np.zeros( (200, 20), dtype=np.float32)} )


print("Trying to load the file with root_numpy")

nparr = rn.root2array( [f_path], treename="ttree", stop=None, branches=keys)
from IPython import embed;embed()
# for ar in nparr:
    # print(ar)
# print(nparr)
