import numpy as np


def maxInterval(spiketrain, max_begin_ISI=0.17, max_end_ISI=0.3, min_IBI=0.2, min_burst_duration=0.01,
                min_spikes_in_burst=3):
    allBurstData = {}

    '''
    Phase 1 - Burst Detection
    Here a burst is defined as starting when two consecutive spikes have an
    ISI less than max_begin_ISI apart. The end of the burst is given when two
    spikes have an ISI greater than max_end_ISI.
    Find ISIs closer than max_begin_ISI and end with max_end_ISI.
    The last spike of the previous burst will be used to calculate the IBI.
    For the first burst, there is no previous IBI.
    '''
    inBurst = False
    burstNum = 0
    currentBurst = []
    for n in range(1, len(spiketrain)):
        ISI = spiketrain[n] - spiketrain[n - 1]
        if inBurst:
            if ISI > max_end_ISI:  # end the burst
                currentBurst = np.append(currentBurst, spiketrain[n - 1])
                allBurstData[burstNum] = currentBurst
                currentBurst = []
                burstNum += 1
                inBurst = False
            elif (ISI < max_end_ISI) & (n == len(spiketrain) - 1):
                currentBurst = np.append(currentBurst, spiketrain[n])
                allBurstData[burstNum] = currentBurst
                burstNum += 1
            else:
                currentBurst = np.append(currentBurst, spiketrain[n - 1])
        else:
            if ISI < max_begin_ISI:
                currentBurst = np.append(currentBurst, spiketrain[n - 1])
                inBurst = True
    # Calculate IBIs
    IBI = []
    for b in range(1, burstNum):
        prevBurstEnd = allBurstData[b - 1][-1]
        currBurstBeg = allBurstData[b][0]
        IBI = np.append(IBI, (currBurstBeg - prevBurstEnd))

    '''
    Phase 2 - Merging of Bursts
    Here we see if any pair of bursts have an IBI less than min_IBI; if so,
    we then merge the bursts. We specifically need to check when say three
    bursts are merged into one.
    '''
    tmp = allBurstData
    allBurstData = {}
    burstNum = 0
    for b in range(1, len(tmp)):
        prevBurst = tmp[b - 1]
        currBurst = tmp[b]
        if IBI[b - 1] < min_IBI:
            prevBurst = np.append(prevBurst, currBurst)
        allBurstData[burstNum] = prevBurst
        burstNum += 1
    if burstNum >= 2:
        allBurstData[burstNum] = currBurst

    '''
    Phase 3 - Quality Control
    Remove small bursts less than min_bursts_duration or having too few
    spikes less than min_spikes_in_bursts. In this phase we have the
    possibility of deleting all spikes.
    '''
    tooShort = 0
    tmp = allBurstData
    allBurstData = {}
    burstNum = 0
    if len(tmp) > 1:
        for b in range(len(tmp)):
            currBurst = tmp[b]
            if len(currBurst) <= min_spikes_in_burst:
                tooShort +=1
            elif currBurst[-1] - currBurst[0] <= min_burst_duration:
                tooShort += 1
            else:
                allBurstData[burstNum] = currBurst
                burstNum += 1

    '''
    plt.figure()
    plt.eventplot(spiketrain)
    for b in allBurstData:
        burst = allBurstData[b]
        plt.axvline(burst[0], color='green')
        plt.axvline(burst[-1], color='red')
    '''

    return allBurstData, tooShort


