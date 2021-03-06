import datetime, time
import sys

spd = float(60*60*24)

start = "2015-01-05-01h13m57s"
start = datetime.datetime.strptime(start, "%Y-%m-%d-%Hh%Mm%Ss")
last = ""

dayssince = []
pages = []

# the template starts with 0 pages.
dayssince.append(0)
pages.append(0)

with open("scripts/pages.md") as file:
    for line in file.readlines():
        
        line = line.strip()
        if not line:
            continue
        if not line.count(" ") == 2:
            sys.exit("what the fuck")
            
        _, date, pagecount = line.split(" ")
        date = date.replace("[", "")
        date = date.replace("]", "")

        current = datetime.datetime.strptime(date, "%Y-%m-%d-%Hh%Mm%Ss")
        delta = current - start
        dayssince.append(delta.days + delta.seconds/spd)
        pages.append(int(pagecount))
        lasttime, lastpages = current, pagecount

import numpy as np
dayssince = np.array(dayssince)
pages = np.array(pages)

#having trouble with Helvetica font
from matplotlib import rcParams,rc
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Helvetica"]
rcParams["font.size"] = "20"
rc('text.latex', preamble=r'\usepackage{cmbright}')

import matplotlib.pyplot as plt

now = datetime.datetime.now()
maxdayssince = (now - start).days + (now - start).seconds/spd

ax = plt.gca()
ax.xaxis.set_label_coords(0.74, -0.07)
ax.yaxis.set_label_coords(-0.07, 0.9)

plt.xlabel("Days since start (5 Jan)")
plt.ylabel("Pages")
plt.title("")
plt.text(1, 0.90*max(pages), r"Latest compile: %s pages" % (lastpages))
plt.text(1, 0.80*max(pages), r"%s" % (lasttime))
plt.axis([-1, maxdayssince+1, 0, 1.1*max(pages)])
plt.grid(False)
plt.plot(dayssince, pages, "-")
plt.plot(dayssince, pages, "rd")
plt.fill_between(dayssince, 0, pages, facecolor='blue', interpolate=True)
plt.savefig("scripts/pages.png")
#plt.savefig("scripts/pages.pdf")
