import os
import pandas as pd
import matplotlib.pyplot as plt
import ast

# Ensure overall dataset analysis folder exists
os.makedirs('overall_dataset_analysis', exist_ok=True)

# Combine data from all repositories
repos = ['autogen', 'gpt-pilot', 'letta']
# Combine data from all repositories
dfs = []
for repo in repos:
    repo_path = os.path.join('individual_repository_analysis', f'{repo}_bandit_summary.csv')
    df = pd.read_csv(repo_path)
    # Convert unique_cwes from string to list
    df['unique_cwes'] = df['unique_cwes'].apply(ast.literal_eval)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv('overall_dataset_analysis/combined_bandit_summary.csv', index=False)

# RQ2: Different severity patterns (repo-wise)
for repo in repos:
    plt.figure(figsize=(12, 6))
    repo_df = combined_df[combined_df['repo'] == repo].copy()
    repo_df['short_commit'] = repo_df['commit'].str[:5]  # Shorten commit to 5 characters
    for severity in ['high_sev', 'med_sev', 'low_sev']:
        plt.plot(repo_df['short_commit'], repo_df[severity], marker='o', linestyle='-', label=severity)
    plt.xlabel('Commit')
    plt.ylabel('Severity Count')
    plt.title(f'Severity Patterns Over Time ({repo})')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'overall_dataset_analysis/RQ2_severity_patterns_{repo}.png')
    plt.close()


# RQ3: CWE coverage analysis
cwe_counts = combined_df['unique_cwes'].explode().value_counts()
plt.figure(figsize=(12, 6))
cwe_counts.plot(kind='bar')
plt.xlabel('CWE ID')
plt.ylabel('Frequency')
plt.title('CWE Coverage Across Repositories')
plt.xticks(rotation=45, ha='right')  # Rotate and align right to avoid cutoff
plt.tight_layout()
plt.savefig('overall_dataset_analysis/RQ3_cwe_coverage.png')
plt.close()

print("Overall dataset analysis complete. Results saved in 'overall_dataset_analysis' folder.")

