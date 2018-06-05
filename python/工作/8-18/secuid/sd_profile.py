# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import cProfile
import pstats
import os
import gprof2dot
import graphviz

Do_Profiling=True

def sd_profile(filename):
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            #Do_Profiling = os.getenv("PROFILING")
            if Do_Profiling:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                #dump to stat file
                ps.dump_stats(filename)
                #dump to png file
                os.system("gprof2dot -f pstats %s | dot -Tpng -o %s.png"%(filename, filename))
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper