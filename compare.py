import matplotlib.pyplot as plt


def plot_results(generations_to_success, selection_method, folder):
    seeds = list(range(1, len(generations_to_success) + 1))
    values = [
        value if value is not None else 0
        for value in generations_to_success
    ]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(seeds, values)

    for seed, result in zip(seeds, generations_to_success):
        if result is None:
            ax.text(seed, 0, "×", ha="center", fontsize=16)

    ax.set_xticks(seeds)
    ax.set_xlabel("Seed")
    ax.set_ylabel("Počet generácií do nájdenia všetkých pokladov")
    ax.set_title(f"Selekcia: {selection_method} (× = bez úspechu)")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(folder / f"graph_{selection_method}.png", dpi=300)
    plt.show()
    plt.close(fig)


def plot_fitness(all_histories, selection_method, folder):
    longest_run = max(len(history) for history in all_histories)

    best_runs = []
    average_runs = []

    for history in all_histories:
        best = [row[1] for row in history]
        average = [row[2] for row in history]

        # Carry the final values forward when a run ends early.
        best += [best[-1]] * (longest_run - len(best))
        average += [average[-1]] * (longest_run - len(average))

        best_runs.append(best)
        average_runs.append(average)

    mean_best = [
        sum(values) / len(values)
        for values in zip(*best_runs)
    ]

    mean_average = [
        sum(values) / len(values)
        for values in zip(*average_runs)
    ]

    generations = range(1, longest_run + 1)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        generations, mean_best,
        label="Priemer najlepšej fitness z behov"
    )
    ax.plot(
        generations, mean_average,
        label="Priemer priemernej fitness populácie"
    )

    ax.set_xlabel("Generácia")
    ax.set_ylabel("Fitness")
    ax.set_title(f"Vývoj fitness – {selection_method}")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(folder / f"fitness_{selection_method}.png", dpi=300)
    plt.show()
    plt.close(fig)    