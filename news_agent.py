#!/usr/bin/env python3
"""
AI and GitHub Competitor News Agent

This agent fetches and formats weekly news updates about AI developments
and GitHub competitors. It aggregates news from various sources and
presents them in a structured format.
"""

import json
import datetime
import feedparser
import requests
from typing import List, Dict, Any
import re
from dataclasses import dataclass
import argparse
import sys

@dataclass
class NewsItem:
    title: str
    url: str
    summary: str
    source: str
    published_date: str
    category: str

class NewsAgent:
    def __init__(self, config_file: str = "news_config.json"):
        """Initialize the news agent with configuration."""
        self.config = self.load_config(config_file)
        self.news_items: List[NewsItem] = []
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration if file doesn't exist
            return {
                "sources": {
                    "ai_news": [
                        {
                            "name": "AI News",
                            "url": "https://feeds.feedburner.com/oreilly/radar/ai",
                            "type": "rss"
                        },
                        {
                            "name": "VentureBeat AI",
                            "url": "https://venturebeat.com/ai/feed/",
                            "type": "rss"
                        },
                        {
                            "name": "The AI Blog",
                            "url": "https://ai.googleblog.com/feeds/posts/default",
                            "type": "rss"
                        }
                    ],
                    "github_competitors": [
                        {
                            "name": "GitLab Blog",
                            "url": "https://about.gitlab.com/blog/all.xml",
                            "type": "rss"
                        },
                        {
                            "name": "Bitbucket Blog",
                            "url": "https://bitbucket.org/blog/rss.xml",
                            "type": "rss"
                        },
                        {
                            "name": "Azure DevOps Blog",
                            "url": "https://devblogs.microsoft.com/devops/feed/",
                            "type": "rss"
                        }
                    ]
                },
                "days_back": 7,
                "max_items_per_source": 5
            }

    def fetch_rss_news(self, source: Dict[str, str], category: str) -> List[NewsItem]:
        """Fetch news from RSS feed."""
        news_items = []
        try:
            print(f"Fetching from {source['name']}...")
            feed = feedparser.parse(source["url"])
            
            if not feed.entries:
                print(f"No entries found for {source['name']}")
                return news_items
            
            print(f"Found {len(feed.entries)} entries from {source['name']}")
            
            # Calculate cutoff date
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.config["days_back"])
            
            count = 0
            for entry in feed.entries:
                if count >= self.config["max_items_per_source"]:
                    break
                    
                # Parse published date - more flexible approach
                published_date = "Unknown"
                entry_date = None
                
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        entry_date = datetime.datetime(*entry.published_parsed[:6])
                        published_date = entry_date.strftime("%Y-%m-%d")
                    except (TypeError, ValueError):
                        pass
                
                if published_date == "Unknown" and hasattr(entry, 'published'):
                    published_date = entry.published[:10] if len(entry.published) >= 10 else entry.published
                
                # More lenient date filtering - if we can't parse the date, include the item
                if entry_date and entry_date < cutoff_date:
                    continue
                
                # Extract summary
                summary = ""
                if hasattr(entry, 'summary'):
                    # Clean HTML tags from summary
                    summary = re.sub('<[^<]+?>', '', entry.summary)
                    summary = re.sub(r'\s+', ' ', summary).strip()  # Clean extra whitespace
                    summary = summary[:200] + "..." if len(summary) > 200 else summary
                elif hasattr(entry, 'description'):
                    # Try description as fallback
                    summary = re.sub('<[^<]+?>', '', entry.description)
                    summary = re.sub(r'\s+', ' ', summary).strip()
                    summary = summary[:200] + "..." if len(summary) > 200 else summary
                
                news_item = NewsItem(
                    title=entry.title if hasattr(entry, 'title') else "No Title",
                    url=entry.link if hasattr(entry, 'link') else "",
                    summary=summary,
                    source=source["name"],
                    published_date=published_date,
                    category=category
                )
                news_items.append(news_item)
                count += 1
                print(f"  Added: {news_item.title[:50]}...")
                
        except Exception as e:
            print(f"Error fetching from {source['name']}: {str(e)}")
        
        return news_items

    def create_sample_data(self) -> None:
        """Create sample news data for testing purposes."""
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        two_days_ago = today - datetime.timedelta(days=2)
        
        sample_ai_news = [
            NewsItem(
                title="OpenAI Announces GPT-5 with Enhanced Reasoning Capabilities",
                url="https://openai.com/blog/gpt-5-announcement",
                summary="OpenAI has unveiled GPT-5, featuring significant improvements in logical reasoning, mathematical problem-solving, and code generation. The model shows 40% better performance on standardized benchmarks compared to GPT-4.",
                source="OpenAI Blog",
                published_date=today.strftime("%Y-%m-%d"),
                category="AI News"
            ),
            NewsItem(
                title="Google's Gemini Pro Now Available in 100+ Countries",
                url="https://blog.google/technology/ai/gemini-pro-global-rollout",
                summary="Google expands Gemini Pro availability globally, bringing advanced AI capabilities to developers and enterprises worldwide. The rollout includes new API endpoints and improved multilingual support.",
                source="Google AI Blog",
                published_date=yesterday.strftime("%Y-%m-%d"),
                category="AI News"
            ),
            NewsItem(
                title="Microsoft and Meta Partner on Open Source AI Framework",
                url="https://blogs.microsoft.com/ai/meta-partnership-announcement",
                summary="Microsoft and Meta announce a strategic partnership to develop an open-source AI framework aimed at democratizing access to advanced machine learning tools for researchers and developers.",
                source="Microsoft AI Blog",
                published_date=two_days_ago.strftime("%Y-%m-%d"),
                category="AI News"
            )
        ]
        
        sample_github_competitor_news = [
            NewsItem(
                title="GitLab 16.8 Released with Advanced Security Scanning",
                url="https://about.gitlab.com/releases/2024/01/18/gitlab-16-8-released/",
                summary="GitLab's latest release introduces enhanced security scanning capabilities, improved CI/CD performance, and new collaboration features. The update includes better integration with cloud providers and advanced vulnerability detection.",
                source="GitLab Blog",
                published_date=today.strftime("%Y-%m-%d"),
                category="GitHub Competitors"
            ),
            NewsItem(
                title="JetBrains Introduces AI-Powered Code Completion in IntelliJ IDEA",
                url="https://blog.jetbrains.com/idea/2024/01/ai-code-completion/",
                summary="JetBrains rolls out AI-powered code completion features across its IDE suite, promising 60% faster code writing with context-aware suggestions and intelligent refactoring recommendations.",
                source="JetBrains Blog",
                published_date=yesterday.strftime("%Y-%m-%d"),
                category="GitHub Competitors"
            ),
            NewsItem(
                title="Atlassian Acquires AI Startup for Developer Productivity",
                url="https://www.atlassian.com/blog/announcements/ai-acquisition",
                summary="Atlassian announces the acquisition of DevAI, a startup focused on AI-powered development tools. The acquisition aims to enhance Jira and Confluence with intelligent automation and predictive analytics.",
                source="Atlassian Blog",
                published_date=two_days_ago.strftime("%Y-%m-%d"),
                category="GitHub Competitors"
            )
        ]
        
        self.news_items = sample_ai_news + sample_github_competitor_news
        print(f"Created {len(self.news_items)} sample news items for testing")

    def fetch_all_news(self) -> None:
        """Fetch news from all configured sources."""
        self.news_items = []
        
        # Fetch AI news
        for source in self.config["sources"]["ai_news"]:
            items = self.fetch_rss_news(source, "AI News")
            self.news_items.extend(items)
        
        # Fetch GitHub competitor news
        for source in self.config["sources"]["github_competitors"]:
            items = self.fetch_rss_news(source, "GitHub Competitors")
            self.news_items.extend(items)

    def generate_report(self) -> str:
        """Generate a formatted news report."""
        if not self.news_items:
            return "No news items found for this week."
        
        # Group by category
        ai_news = [item for item in self.news_items if item.category == "AI News"]
        github_news = [item for item in self.news_items if item.category == "GitHub Competitors"]
        
        report = f"# Weekly Tech News Update - {datetime.datetime.now().strftime('%B %d, %Y')}\n\n"
        
        if ai_news:
            report += "## 🤖 AI News\n\n"
            for item in ai_news:
                report += f"### [{item.title}]({item.url})\n"
                report += f"**Source:** {item.source} | **Date:** {item.published_date}\n\n"
                if item.summary:
                    report += f"{item.summary}\n\n"
                report += "---\n\n"
        
        if github_news:
            report += "## 🚀 GitHub Competitors & DevOps\n\n"
            for item in github_news:
                report += f"### [{item.title}]({item.url})\n"
                report += f"**Source:** {item.source} | **Date:** {item.published_date}\n\n"
                if item.summary:
                    report += f"{item.summary}\n\n"
                report += "---\n\n"
        
        report += f"\n*Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        report += f"*Total items: {len(self.news_items)}*\n"
        
        return report

    def save_report(self, filename: str = None) -> str:
        """Save the report to a file."""
        if filename is None:
            filename = f"weekly_news_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filename

def main():
    """Main entry point for the news agent."""
    parser = argparse.ArgumentParser(description='AI and GitHub Competitor News Agent')
    parser.add_argument('--config', default='news_config.json',
                        help='Configuration file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--print', action='store_true',
                        help='Print report to console')
    parser.add_argument('--test', action='store_true',
                        help='Run with sample data for testing')
    
    args = parser.parse_args()
    
    try:
        agent = NewsAgent(args.config)
        
        if args.test:
            print("Running in test mode with sample data...")
            agent.create_sample_data()
        else:
            print("Fetching news...")
            agent.fetch_all_news()
        
        if args.print:
            print("\n" + "="*60)
            print(agent.generate_report())
        
        if args.output or not args.print:
            filename = agent.save_report(args.output)
            print(f"Report saved to: {filename}")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()