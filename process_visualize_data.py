import matplotlib
matplotlib.use('Agg')
import csv
import matplotlib.pyplot as plt

metrics = {}

for i in range(1, 11):
    filename = f"benchmark_data_{i}.csv"
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row['metric']
            if metric not in metrics:
                metrics[metric] = {'fork_shell': [], 'spork_shell': []}
            metrics[metric]['fork_shell'].append(float(row['fork_shell']))
            metrics[metric]['spork_shell'].append(float(row['spork_shell']))

means = {}
for metric, values in metrics.items():
    means[metric] = {
        'fork_shell': sum(values['fork_shell']) / len(values['fork_shell']),
        'spork_shell': sum(values['spork_shell']) / len(values['spork_shell'])
    }

# Metrics to plot (excluding total_runs)
plot_metrics = ['total_time_us', 'exec_time_us', 'avg_exec_us', 'max_rss_kb', 'page_faults', 'context_switches']

for metric in plot_metrics:
    fig, ax = plt.subplots()
    
    fork_val = means[metric]['fork_shell']
    spork_val = means[metric]['spork_shell']
    
    bars = ax.bar(['fork_shell', 'spork_shell'], [fork_val, spork_val])
    
    # Add data labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom')
    
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} Comparison')
    
    plt.tight_layout()
    plt.savefig(f'{metric}_comparison.png')
    plt.close()

print("Saved 6 comparison charts")
