import pandas as pd
import solver
import time


print("Loading database...")
ts = time.perf_counter()
data = pd.read_parquet('resources/data.parquet')
te = time.perf_counter()
print(f"Loaded database in {te-ts:2.4f} sec")

# Assuming the word is "crimp"
MYS = "crimp"
observations = []
sol_size = data.shape[0]
print(f"Started with {sol_size} possible words.")

while sol_size > 2:
    guess, ent = solver.get_optimal_guess(data, observations)
    print(f"Guess \"{guess}\" with entropy {ent:.2f}")

    observations.append((guess, solver.evaluate_guess(guess, MYS)))
    partition = solver.get_partition(data, observations)

    sol_size = partition.shape[0]
    print(f"Reduced the number of possible words to {sol_size}")

sols = [f"\"{w}\"" for w in partition.index]
if sol_size == 2:
    print(f"Choose randomly from {', '.join(sols)}")
else:
    print(f"Choose {', '.join(sols)}")
