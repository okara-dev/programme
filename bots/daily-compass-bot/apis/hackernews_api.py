"""
Hacker News API – Tech-News von Y Combinator
Kein Key nötig, kein Rate-Limit [citation:2][citation:7]
"""

import requests

class HackerNewsAPI:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
    
    def get_top_stories(self, limit=5):
        """Holt die Top-Stories von Hacker News"""
        try:
            # Top-Story-IDs holen
            response = requests.get(
                f"{self.base_url}/topstories.json",
                timeout=10
            )
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            stories = []
            for story_id in story_ids:
                story_response = requests.get(
                    f"{self.base_url}/item/{story_id}.json",
                    timeout=5
                )
                story = story_response.json()
                if story and story.get("title"):
                    stories.append({
                        "title": story.get("title"),
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "score": story.get("score", 0)
                    })
            
            return stories
            
        except Exception as e:
            print(f"⚠️ Hacker News Fehler: {e}")
            return []
    
    def format(self, stories):
        if not stories:
            return "🟠 Keine Hacker News verfügbar."
        
        lines = ["🟠 **HACKER NEWS**", "=" * 35]
        for i, story in enumerate(stories, 1):
            title = story.get("title", "Kein Titel")
            url = story.get("url", "#")
            score = story.get("score", 0)
            
            lines.append(f"{i}. **{title}**")
            lines.append(f"   👍 {score} Points | [Link]({url})")
            lines.append("")
        
        return "\n".join(lines)