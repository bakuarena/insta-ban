# ban_engine/rules.py

BANNED_HASHTAGS = [
    "#follow4follow", "#l4l", "#like4like", "#f4f", "#followme", 
    "#spambot", "#bot", "#marketing", "#promotion", "#crypto", 
    "#nft", "#bitcoin", "#trading", "#signals"
]

SPAM_BIO_KEYWORDS = [
    "dm me", "dm for", "whatsapp", "telegram", "signals", "roi", 
    "onlyfans", "link in bio", "click here", "promo", "giveaway",
    "crypto", "nft", "trading", "investment"
]

ENGAGEMENT_BAIT_PATTERNS = [
    r"like (this|the|my) post",
    r"follow (me|us|back|for)",
    r"comment.*below.*to (receive|get|win)",
    r"share (this|it)",
    r"tag (your|a) (friend|friend)",
    r"dm (for|to) (me|us)"
]

AUTOMATION_THRESHOLDS = {
    "max_follows_per_hour": 10,
    "max_posts_per_hour": 5,
    "max_ratio": 2.5,
    "max_hashtags_per_post": 10
}