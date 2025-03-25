import os
import json
import pandas as pd

# Define paths
repos = ['autogen', 'gpt-pilot', 'letta']
output_folder = 'individual_repository_analysis'
os.makedirs(output_folder, exist_ok=True)

# Data collection
def parse_bandit_reports(repo):
    reports_path = os.path.join(repo, 'bandit_reports')
    data = []

    for report_file in os.listdir(reports_path):
        with open(os.path.join(reports_path, report_file), 'r') as f:
            report = json.load(f)

        commit = report_file.replace('.json', '')
        high_conf, med_conf, low_conf = 0, 0, 0
        high_sev, med_sev, low_sev = 0, 0, 0
        unique_cwes = set()

        for result in report.get('results', []):
            # Confidence
            if result['issue_confidence'] == 'HIGH':
                high_conf += 1
            elif result['issue_confidence'] == 'MEDIUM':
                med_conf += 1
            elif result['issue_confidence'] == 'LOW':
                low_conf += 1

            # Severity
            if result['issue_severity'] == 'HIGH':
                high_sev += 1
            elif result['issue_severity'] == 'MEDIUM':
                med_sev += 1
            elif result['issue_severity'] == 'LOW':
                low_sev += 1

            # CWE Extraction
            cwe_id = result.get('issue_cwe', {}).get('id')
            if cwe_id:
                unique_cwes.add(cwe_id)

        data.append({
            'repo': repo,
            'commit': commit,
            'high_conf': high_conf,
            'med_conf': med_conf,
            'low_conf': low_conf,
            'high_sev': high_sev,
            'med_sev': med_sev,
            'low_sev': low_sev,
            'unique_cwes': list(unique_cwes),  # Store as list for CSV
            'total_no_unique_cwes': len(unique_cwes)
        })
    
    return pd.DataFrame(data)

# Analysis
def analyze_repo(repo):
    print(f"Analyzing {repo}...")
    df = parse_bandit_reports(repo)
    df = df.sort_values('commit')
    output_path = os.path.join(output_folder, f'{repo}_bandit_summary.csv')
    df.to_csv(output_path, index=False)
    print(f"{repo} analysis complete. Summary saved to {output_path}")

# Run analysis for each repo
for repo in repos:
    analyze_repo(repo)

print("Analysis complete. CSV summaries saved in individual_repository_analysis folder.")

