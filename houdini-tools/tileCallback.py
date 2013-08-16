import sys,mantra

tile = mantra.property('tile:ncomplete')[0]
if tile == 1:
    # This is the first tile rendered in the image

    print mantra.property('renderer:name')
    ntiles = mantra.property('tile:ntiles')[0]
    prev_pct = -1
    lap = 0
    lsum = 0

lap += mantra.property('tile:laptime')[0]
pct = tile * 100 / ntiles

if pct != prev_pct:
    mem = mantra.property('tile:memory')[0]
    cords = mantra.property('tile:coords')[0]
    mem = float(mem/1024)/1024
    print cords
    print mem/1024
    total = mantra.property('tile:totaltime')[0]
    fpct = float(tile)/float(ntiles) # Percent complete
    prev_pct = pct

    print('%03d%% Complete - Laptime %g/%g - ETA %g seconds\n' %
            (pct, lap, total, total/fpct))

    lap = 0         # Reset the lap counter
