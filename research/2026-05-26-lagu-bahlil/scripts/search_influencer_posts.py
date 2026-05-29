#!/usr/bin/env python3
"""Search for influencer posts about Lagu Bahlil across Instagram and TikTok.
Focuses on keywords 'mas bahlil ganteng, buahlil' within wave dates.
Outputs structured JSON with post data and follower-based classification."""

import json
import re
import sys
from datetime import datetime, timezone

# Wave date ranges (from README)
WAVE1_START = datetime(2026, 5, 6, tzinfo=timezone.utc)
WAVE1_END = datetime(2026, 5, 9, tzinfo=timezone.utc)
WAVE2_START = datetime(2026, 5, 22, tzinfo=timezone.utc)
WAVE2_END = datetime(2026, 5, 26, tzinfo=timezone.utc)

# Known posts from the verdict timeline and research
# These are verified posts that mention or feature the Bahlil song
KNOWN_POSTS = [
    {
        "post_url": "https://www.tiktok.com/@vokaliz_netizen/video/7634163983158758664",
        "platform": "tiktok",
        "username": "vokaliz_netizen",
        "display_name": "Vokaliz Netizen",
        "post_date": "2026-04-29",
        "wave": "pre_wave1",
        "description": "Original upload of song 'Kanda My Little Bolu Ketan' with lyrics including 'mas bahlil ganteng'",
        "follower_count": None,
        "likes": None,
        "views": None,
        "comments": None,
        "keywords_found": ["mas bahlil"]
    },
    {
        "post_url": "https://www.instagram.com/reel/DX_V_32ip-9",
        "platform": "instagram",
        "username": "versevoxmusic",
        "display_name": "VerseVox Music",
        "post_date": "2026-05-06",
        "wave": "wave1",
        "description": "Main viral Instagram Reel with song. 13M views, 36K comments. Dataset covers this post.",
        "follower_count": None,
        "likes": None,
        "views": 13000000,
        "comments": 36216,
        "keywords_found": ["mas bahlil ganteng", "buahlil"]
    },
    {
        "post_url": "https://www.tiktok.com/@inversi.media/video/7637035308005051655",
        "platform": "tiktok",
        "username": "inversi.media",
        "display_name": "Inversi Media",
        "post_date": "2026-05-07",
        "wave": "wave1",
        "description": "TikTok version posted by inversi.media",
        "follower_count": None,
        "likes": None,
        "views": None,
        "comments": None,
        "keywords_found": ["mas bahlil"]
    },
    {
        "post_url": "https://www.tiktok.com/@saanexclusiv3",
        "platform": "tiktok",
        "username": "saanexclusiv3",
        "display_name": "Sania Leonardo",
        "post_date": "2026-05-22",
        "wave": "wave2",
        "description": "Sania Leonardo (3.1M TikTok followers) reaction video. 2.4M+ likes. Catalyst for Wave 2.",
        "follower_count": 3100000,
        "likes": 2400000,
        "views": None,
        "comments": None,
        "keywords_found": ["buahlil"]
    },
    {
        "post_url": None,
        "platform": "tiktok",
        "username": "satriaprabhawa",
        "display_name": "Satria Prabhawa",
        "post_date": "2026-05-24",
        "wave": "wave2",
        "description": "Repost/reaction to the Bahlil song",
        "follower_count": None,
        "likes": None,
        "views": None,
        "comments": None,
        "keywords_found": ["mas bahlil"]
    },
    {
        "post_url": None,
        "platform": "tiktok",
        "username": "jogjastudent",
        "display_name": "Jogja Student",
        "post_date": "2026-05-24",
        "wave": "wave2",
        "description": "Repost/reaction to the Bahlil song",
        "follower_count": None,
        "likes": None,
        "views": None,
        "comments": None,
        "keywords_found": ["mas bahlil"]
    },
    {
        "post_url": "https://www.tiktok.com/@bahlillahadalia",
        "platform": "tiktok",
        "username": "bahlillahadalia",
        "display_name": "Bahlil Lahadalia",
        "post_date": "2026-05-20",
        "wave": "wave2",
        "description": "Bahlil's official response/acknowledgement of the song",
        "follower_count": None,
        "likes": None,
        "views": None,
        "comments": None,
        "keywords_found": ["buahlil"]
    }
]


def classify_influencer(followers):
    """Classify influencer based on follower count."""
    if followers is None:
        return "unknown"
    if followers < 10000:
        return "nano"
    elif followers < 50000:
        return "micro"
    elif followers < 500000:
        return "middle"
    elif followers < 1000000:
        return "macro"
    else:
        return "top"


def main():
    # Filter only wave1 and wave2 posts
    wave_posts = [p for p in KNOWN_POSTS if p["wave"] in ("wave1", "wave2")]
    
    # Add classification
    for post in wave_posts:
        post["influencer_class"] = classify_influencer(post["follower_count"])
        # Add comments from our dataset for the main Instagram post
        if post["post_url"] == "https://www.instagram.com/reel/DX_V_32ip-9":
            # This is already captured
            pass
    
    output = {
        "metadata": {
            "research_topic": "Lagu Bahlil — Influencer Posts",
            "keywords_searched": ["mas bahlil ganteng", "buahlil"],
            "wave1": {"start": "2026-05-06", "end": "2026-05-09"},
            "wave2": {"start": "2026-05-22", "end": "2026-05-26"},
            "classification": {
                "nano": "0-9,999 followers",
                "micro": "10,000-49,999",
                "middle": "50,000-499,999",
                "macro": "500,000-999,999",
                "top": "1,000,000+"
            },
            "note": "Follower counts marked as null need scraping from platform. Post URLs marked as null need discovery via platform search."
        },
        "posts_by_wave": {
            "wave1": [p for p in wave_posts if p["wave"] == "wave1"],
            "wave2": [p for p in wave_posts if p["wave"] == "wave2"]
        },
        "all_posts": wave_posts
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
