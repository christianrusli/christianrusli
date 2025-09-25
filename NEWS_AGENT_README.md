# AI & GitHub Competitor News Agent

An automated news aggregation agent that provides weekly updates on AI developments and GitHub competitors.

## Features

- 🤖 **AI News**: Aggregates latest news from major AI sources including Google AI, OpenAI, VentureBeat AI, and more
- 🚀 **GitHub Competitors**: Tracks updates from GitLab, Bitbucket, Azure DevOps, JetBrains, and Atlassian
- 📅 **Weekly Automation**: Runs automatically every Monday via GitHub Actions
- 📝 **Formatted Reports**: Generates clean, markdown-formatted news reports
- ⚙️ **Configurable**: Easily customizable news sources and filtering options

## Usage

### Manual Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Generate and print news report
python news_agent.py --print

# Generate and save to file
python news_agent.py --output my_news_report.md

# Use custom configuration
python news_agent.py --config my_config.json --print
```

### Automated Execution

The agent runs automatically every Monday at 9:00 AM UTC via GitHub Actions. It will:
1. Fetch the latest news from all configured sources
2. Generate a formatted report
3. Create a pull request with the news update
4. Upload the report as a workflow artifact

You can also trigger it manually:
1. Go to the "Actions" tab in your GitHub repository
2. Select "Weekly AI & GitHub Competitor News"
3. Click "Run workflow"

## Configuration

The `news_config.json` file controls the agent's behavior:

```json
{
  "sources": {
    "ai_news": [...],
    "github_competitors": [...]
  },
  "days_back": 7,
  "max_items_per_source": 5,
  "keywords": {...},
  "filters": {...}
}
```

### Configuration Options

- **sources**: RSS feed URLs for AI and GitHub competitor news
- **days_back**: How many days back to look for news (default: 7)
- **max_items_per_source**: Maximum articles per source (default: 5)
- **keywords**: Relevant keywords for filtering (future feature)
- **filters**: Title filtering options

## News Sources

### AI News Sources
- Google AI Blog
- OpenAI Blog
- VentureBeat AI
- MIT Technology Review
- AI News

### GitHub Competitor Sources
- GitLab Blog
- Bitbucket Blog
- Azure DevOps Blog
- JetBrains Blog
- Atlassian Blog

## Output Format

The generated reports include:
- **Title and URL** for each news item
- **Source and publication date**
- **Summary** (auto-generated from RSS content)
- **Categorization** (AI News vs GitHub Competitors)
- **Metadata** (generation time, item count)

## Requirements

- Python 3.7+
- feedparser
- requests

## Example Output

```markdown
# Weekly Tech News Update - December 25, 2024

## 🤖 AI News

### [New Advances in Large Language Models](https://example.com/article1)
**Source:** OpenAI Blog | **Date:** 2024-12-20

Recent developments in language model architecture show promising results...

---

## 🚀 GitHub Competitors & DevOps

### [GitLab 16.8 Released with Enhanced CI/CD](https://example.com/article2)
**Source:** GitLab Blog | **Date:** 2024-12-18

This release includes improved pipeline performance and new security features...

---

*Report generated on 2024-12-25 09:00:00*
*Total items: 15*
```

## Customization

To add new news sources:
1. Edit `news_config.json`
2. Add RSS feed URLs to the appropriate category
3. Test with `python news_agent.py --print`

To modify the report format:
1. Edit the `generate_report()` method in `news_agent.py`
2. Customize markdown formatting and structure

## Troubleshooting

- **No news items found**: Check if RSS feeds are accessible and contain recent content
- **SSL/Connection errors**: Some feeds may require different request headers or user agents
- **Empty summaries**: RSS feeds may not include summary content; titles and links will still be captured

## Contributing

Feel free to:
- Add new news sources
- Improve filtering and categorization
- Enhance the report format
- Add new features like email notifications or Slack integration

---

*Part of the christianrusli automation suite*