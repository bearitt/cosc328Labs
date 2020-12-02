import matplotlib.pyplot as plt
import numpy as np

# calculate efficiency values for slotted aloha
def slotAloha(N, p):
    return N*p*pow((1-p),(N-1))
# calculate efficiency values for pure aloha
def aloha(N, p):
    return N*p*pow((1-p),(2*(N-1)))

# generate probabilities from 0-1
alohaProb = [p for p in np.arange(0,1,0.01)]
# calculate efficiency values under slotted aloha
# for N=15 and N=25
sAlohaEff15 = [slotAloha(15,p) for p in alohaProb]
sAlohaEff25 = [slotAloha(25,p) for p in alohaProb]
# calculate efficiency values under pure aloha
# for N=15 and N=25
alohaEff15 = [aloha(15,p) for p in alohaProb]
alohaEff25 = [aloha(25,p) for p in alohaProb]

# Plot 1 - Slotted Aloha
plt.subplot(211)
plt.axis([0,1,0,0.4])
plt.title('Slotted Aloha efficiency')
plt.plot(alohaProb, sAlohaEff15, label='N=15')
plt.plot(alohaProb, sAlohaEff25, label='N=25')
plt.legend()
plt.xlabel('probability p')
plt.ylabel('efficiency e')

# Plot 2 - Pure Aloha
plt.subplot(212)
plt.axis([0,1,0,0.2])
plt.title('Aloha efficiency')
plt.plot(alohaProb, alohaEff15, label='N=15')
plt.plot(alohaProb, alohaEff25, label='N=25')
plt.legend()
plt.xlabel('probability p')
plt.ylabel('efficiency e')

plt.show()
