# MaxIntervalPy

Max Interval Method for Burst Detection for Python.

A Python- based Max Interval (MI) burst detection algorithm was created to identify individual bursts. MI is a fixed threshold-based method for identifying bursts that uses five fixed threshold parameters (maximum ISI at start of the burst, maximum ISI in burst, minimum burst duration, minimum IBI, and minimum number of spikes within burst) to identify, merge, and exclude potential bursts. The values for these parameters are chosen a priori.

The algorithm is separated into three phases:

Burst detection – where a burst is defined as starting when two consecutive spikes have an ISI less than the maximum ISI at start of the burst. The end of the burst is determined when two spikes have an ISI greater than the maximum ISI in burst. The last spike of the previous burst and the first spike of the current burst will be used to calculate the IBI. For the first burst, there is no previous IBI.
Merge bursts – any pair of bursts that have an IBI less than the minimum IBI will be merged into a single burst.
Quality control – removes any small burst less than the minimum burst duration or has less than minimum number of spikes in burst. This step can potentially delete all spikes. The bursts are stored in a MATLAB cell array to permit detailed analysis of burst dynamics.
