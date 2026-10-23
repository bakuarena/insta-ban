# main.py

import json
import sys
from ban_engine import BanAnalyzer

def print_report(report):
    """Pretty prints the BanReport to the terminal."""
    print("\n" + "="*50)
    print(f"🚨 INSTAGRAM ENFORCEMENT REPORT: @{report.handle}")
    print("="*50)
    print(f"SEVERITY:      {report.severity}")
    print(f"RISK SCORE:    {report.risk_score:.1f}/100")
    print(f"PRIMARY REASON:{report.primary_reason}")
    
    if report.secondary_reasons:
        print("\nSECONDARY FACTORS:")
        for reason in report.secondary_reasons:
            print(f"  - {reason}")
            
    if report.shadowbanned_tags:
        print("\nSHADOWBANNED TAGS:")
        print(f"  {', '.join(report.shadowbanned_tags)}")
        
    print("\nINTERNAL SYSTEM LOG:")
    print("-" * 30)
    for log_line in report.internal_log:
        print(log_line)
    print("="*50 + "\n")

def load_account_from_json(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Demo data for a "Spammy" account
        demo_account = {
            "handle": "crypto_signals_bot",
            "bio": "DM for signals! +100% ROI. Follow back!",
            "recent_captions": ["Like this post and I'll like you back! Follow for more!"],
            "recent_hashtags": ["#crypto", "#nft", "#follow4follow", "#like4like", "#bitcoin"],
            "followers": 500,
            "following": 3000,
            "posts_per_hour": 12,
            "follows_per_hour": 45
        }
    elif len(sys.argv) > 1:
        demo_account = load_account_from_json(sys.argv[1])
    else:
        print("Usage: python main.py <path/to/account.json> or python main.py --demo")
        return

    analyzer = BanAnalyzer()
    report = analyzer.analyze(demo_account)
    print_report(report)

if __name__ == "__main__":
    main()