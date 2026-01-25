import math

def get_project_mode_index(kloc):
    """Determines project mode index based on size (KLoC)."""
    if kloc < 2:
        # Default to Organic for very small projects rather than exiting
        return 0
    elif kloc <= 50:
        return 0  # Organic
    elif kloc <= 300:
        return 1  # Semi-detached
    else:
        return 2  # Embedded

def run_cocomo_estimate(table, kloc):
    modes = ["Organic", "Semi-Detached", "Embedded"]

    # Get mode index
    idx = get_project_mode_index(kloc)
    a, b, c, d = table[idx]

    effort = a * math.pow(kloc, b)
    time = c * math.pow(effort, d)
    staff = effort / time

    # Output with clean, scannable formatting
    print(f"Selected Mode: {modes[idx]}")
    print(f"{'-'*30}")
    print(f"Effort: {round(effort, 2)} Person-Months")
    print(f"Formula: {a} * ({kloc}^{b})")
    
    print(f"\nDevelopment Time: {round(time, 2)} Months")
    print(f"Formula: {c} * ({round(effort, 2)}^{d})")
    print(f"\nAverage Staffing: {round(staff, 1)} Person(s)")
    print(f"{'-'*30}")

# Constants

# Row 0: Organic | Row 1: Semi-Detached | Row 2: Embedded
cocomo_table = [
    [2.4, 1.05, 2.5, 0.38],
    [3.0, 1.12, 2.5, 0.35],
    [3.6, 1.20, 2.5, 0.32]
]

run_cocomo_estimate(cocomo_table, kloc=9)