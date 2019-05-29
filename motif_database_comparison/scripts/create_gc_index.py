import os
from gimmemotifs.config import CACHE_DIR
from gimmemotifs.background import create_gc_bin_index
import sys

genome = sys.argv[1]
GC_INDEX =  os.path.join(CACHE_DIR, "{}.gcfreq.100.feather".format(os.path.basename(genome)))

if not os.path.exists(GC_INDEX):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    create_gc_bin_index(genome, GC_INDEX, min_bin_size=100)
