import json
import matplotlib.pyplot as plt

### "load-results"
with open("results.json", 'r') as f:
    results = json.load(f)

print results

### "plot"
vals = [result['sold-out-in'] for result in results]
bars = range(len(vals))

plt.figure(figsize=(5,3))
spines = ["left", "bottom"]
spines = ["bottom"]
ax = plt.subplot(1, 1, 1)
for loc, spine in ax.spines.iteritems():
  if loc not in spines:
    spine.set_color('none')

ax.set_ylim([bars[0] - 0.2, bars[-1] + 0.2])

for i, result in enumerate(results):
    plt.text(1, i+0.05, result['name'])
    plt.text(result['sold-out-in'] + 1, i, "%.1f" % result['sold-out-in'])

ax.set_yticks([])
ax.xaxis.set_ticks_position('bottom')

plt.plot(vals, bars, 'o')
plt.hlines(bars, [0], vals, linestyles='dotted', lw=2)

plt.savefig("sold-out-in.png") 
