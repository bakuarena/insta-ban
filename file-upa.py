# ban_engine/analyzer.py

import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, field

from .rules import (
    BANNED_HASHTAGS, 
    SPAM_BIO_KEYWORDS, 
    ENGAGEMENT_BAIT_PATTERNS, 
    AUTOMATION_THRESHOLDS
)

@dataclass
class BanReport:
    handle: str
    severity: str
    primary_reason: str
    secondary_reasons: List[str] = field(default_factory=list)
    shadowbanned_tags: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    internal_log: List[str] = field(default_factory=list)

class BanAnalyzer:
    def __init__(self):
        self.log_buffer = []

    def _log(self, message: str):
        timestamp = datetime.now().strftime("[%H:%M:%S.%f]")
        self.log_buffer.append(f"{timestamp} {message}")

    def analyze(self, account: Dict[str, Any]) -> BanReport:
        """
        Analyzes account data and generates a BanReport.
        """
        self.log_buffer = []
        self._log(f"INITIATING AUDIT for @{account['handle']}")
        
        risk_score = 0.0
        secondary_reasons = []
        shadowbanned_tags = []

        # 1. Inauthentic Behavior / Ratio Analysis
        followers = account.get("followers", 0)
        following = account.get("following", 0)
        ratio = following / followers if followers > 0 else following
        
        if ratio > AUTOMATION_THRESHOLDS["max_ratio"]:
            risk_score += 30
            secondary_reasons.append(f"Abnormal Follow Ratio ({ratio:.1f}:1)")
            self._log(f"Anomaly detected: Following/Followers ratio {ratio:.1f} exceeds threshold.")

        # 2. Automation / Velocity Check
        pph = account.get("posts_per_hour", 0)
        fph = account.get("follows_per_hour", 0)
        
        if pph > AUTOMATION_THRESHOLDS["max_posts_per_hour"]:
            risk_score += 25
            secondary_reasons.append("Excessive Posting Velocity")
            self._log(f"Velocity flag: {pph} posts/hr detected. Likely automated.")
            
        if fph > AUTOMATION_THRESHOLDS["max_follows_per_hour"]:
            risk_score += 20
            secondary_reasons.append("Aggressive Follow/Unfollow Activity")

        # 3. Hashtag Spam & Shadowban Triggers
        hashtags = [h.lower() for h in account.get("recent_hashtags", [])]
        for tag in hashtags:
            if tag in BANNED_HASHTAGS:
                shadowbanned_tags.append(tag)
                risk_score += 15
                self._log(f"Hashtag filter hit: {tag} is on the 'Engagement Bait' blocklist.")
            if hashtags.count(tag) > 3:
                risk_score += 5
                self._log(f"Repetitive hashtag usage detected: {tag}")

        # 4. Bio & Content Keyword Analysis
        bio = account.get("bio", "").lower()
        captions = [c.lower() for c in account.get("recent_captions", [])]
        
        for kw in SPAM_BIO_KEYWORDS:
            if kw in bio:
                risk_score += 10
                secondary_reasons.append(f"Promotional Bio Keyword: '{kw}'")
                self._log(f"Bio classifier flagged promotional keyword: {kw}")

        for pattern in ENGAGEMENT_BAIT_PATTERNS:
            if any(re.search(pattern, c) for c in captions):
                risk_score += 15
                secondary_reasons.append("Engagement Baiting in Captions")
                self._log("NLP classifier detected 'engagement baiting' syntax in captions.")
                break

        # 5. Determine Severity & Primary Reason
        primary_reason = "No Enforcement Action"
        if risk_score >= 80:
            severity = "PERMANENT BAN"
            primary_reason = "Inauthentic Behavior & Spam Ecosystem"
            self._log("CRITICAL: Account classified as part of a spam ring. Initiating permanent termination.")
        elif risk_score >= 50:
            severity = "TEMPORARY RESTRICTION (24-72h)"
            primary_reason = "Excessive Automation"
            self._log("Warning: Rate limits exceeded. Applying temporary action block.")
        elif risk_score >= 25:
            severity = "SHADOWBAN (Reach Throttled)"
            primary_reason = "Content Quality & Relevance"
            self._log("Action: Reducing account reach in Explore and Suggested. No user notification.")
        elif risk_score > 0:
            severity = "WATCHLIST"
            primary_reason = "Minor Policy Deviations"
            self._log("Account added to 'Watchlist' for continued monitoring.")
        else:
            severity = "CLEAN"
            self._log("Audit complete. No significant violations detected.")

        return BanReport(
            handle=account['handle'],
            severity=severity,
            primary_reason=primary_reason,
            secondary_reasons=secondary_reasons,
            shadowbanned_tags=shadowbanned_tags,
            risk_score=risk_score,
            internal_log=self.log_buffer
        )