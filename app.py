import matplotlib.pyplot as plt
import numpy as np
import wfdb

path = 'physionet.org/files/chfdb/1.0.0/'

record_name = path + 'chf01'

record = wfdb.rdrecord(record_name)

signal = record.p_signal

channel_0 = signal[:, 0]

mean_value = np.mean(channel_0)

print(f"Media semnalului ECG (canalul 0) pentru {record_name} este: {mean_value:.4f}")

plt.figure(figsize=(12, 4))
plt.plot(channel_0, color='blue')
plt.title(f'Semnalul ECG (canalul 0) pentru {record_name}')
plt.xlabel('Sample')
plt.ylabel('Amplitude (mV)')
plt.grid(True)
plt.tight_layout()
plt.show()
