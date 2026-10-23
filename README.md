# Instagram Ban Generator (Forensic Simulator)

A Python utility that simulates Instagram's internal enforcement logic. It analyzes account metadata, content strategy, and engagement patterns against Meta's known spam and inauthentic behavior heuristics to generate a forensic "Ban Report."

## Features
- **Risk Scoring:** Calculates a 0-100 risk score based on account health.
- **Severity Levels:** Predicts if the account will be Shadowbanned, Temporarily Restricted, or Permanently Banned.
- **Internal Log Simulation:** Generates a mock internal system log showing exactly which filters (NLP, Velocity, Ratio) triggered the ban.
- **Heuristic Rules:** Includes a database of known "spam" keywords, hashtags, and engagement baiting patterns.

## Installation
```bash
git clone https://github.com/your-username/ig-ban-generator
cd ig-ban-generator
pip install -r requirements.txt
