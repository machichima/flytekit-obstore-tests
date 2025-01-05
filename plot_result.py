import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data_path = "./runtime_measure_minio.csv"

df = pd.read_csv(data_path)

origin_runtime = df.origin
obstore_rutime = df.obstore
x = list(range(len(origin_runtime)))

plt.figure(figsize=(10, 6))
plt.plot(x, origin_runtime, label='Origin', marker='o')
plt.plot(x, obstore_rutime, label='Obstore', marker='s')
plt.title('put file runtime')
plt.xlabel('File Size (mb)')
plt.ylabel('Runtime (second)')
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.legend()
plt.grid(True)
plt.savefig("./put_file_runtime.png")
plt.show()
