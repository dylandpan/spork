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

# Time metrics chart
time_metrics = ['total_time_us', 'exec_time_us', 'avg_exec_us']
fig, ax = plt.subplots()
x = range(len(time_metrics))
width = 0.35
fork_vals = [means[m]['fork_shell'] for m in time_metrics]
spork_vals = [means[m]['spork_shell'] for m in time_metrics]
ax.bar([i - width/2 for i in x], fork_vals, width, label='fork_shell')
ax.bar([i + width/2 for i in x], spork_vals, width, label='spork_shell')
ax.set_xticks(x)
ax.set_xticklabels(time_metrics)
ax.set_ylabel('Microseconds')
ax.set_title('Time Metrics Comparison')
ax.legend()
plt.savefig('time_comparison.png')
plt.close()

# Memory metrics chart
memory_metrics = ['max_rss_kb', 'page_faults', 'context_switches']
fig, ax = plt.subplots()
x = range(len(memory_metrics))
fork_vals = [means[m]['fork_shell'] for m in memory_metrics]
spork_vals = [means[m]['spork_shell'] for m in memory_metrics]
ax.bar([i - width/2 for i in x], fork_vals, width, label='fork_shell')
ax.bar([i + width/2 for i in x], spork_vals, width, label='spork_shell')
ax.set_xticks(x)
ax.set_xticklabels(memory_metrics)
ax.set_ylabel('Count / KB')
ax.set_title('Memory Metrics Comparison')
ax.legend()
plt.savefig('memory_comparison.png')
plt.close()

print("Saved time_comparison.png and memory_comparison.png")
