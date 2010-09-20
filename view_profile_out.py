import pstats

p = pstats.Stats('profiler_out.pro')
p.strip_dirs().sort_stats("time").print_stats()

raw_input("Press enter to exit...")
