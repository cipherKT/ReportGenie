# ReportGenie

**ReportGenie** is an automated reporting tool designed to generate daily summaries of ongoing conflicts, with a specific focus on the Russia-Ukraine conflict. By scraping the latest articles from various reputable sources such as BBC, Al Jazeera, The Guardian, and Ukrinform, this tool compiles a comprehensive report in a standardized format. It also includes relevant images and properly formatted citations.

## Features

- **Automated Web Scraping**: Fetches the latest articles from selected news sources.
- **Time-Based Filtering**: Ensures that only the most recent articles are included in each report.
- **Content Summarization**: Uses advanced language models to generate concise summaries of lengthy articles.
- **Image Integration**: Incorporates relevant images into the report for enhanced context.
- **Citation Management**: Automatically generates properly formatted citations for all referenced articles.
- **On-Demand & Scheduled Reports**: Generate reports manually or schedule daily automated report generation.

## Project Structure

```
ReportGenie/
├── data/               # Stores scraped articles and images
├── notebooks/          # Jupyter notebooks for prototyping and testing
├── reports/            # Final generated reports
├── src/                # Source code for scraping, summarization, and report generation
├── tests/              # Unit tests and testing scripts
├── venv/               # Virtual environment for project dependencies
└── README.md           # Project overview and documentation
```

## Getting Started

### Prerequisites

- **Python 3.8+** is required to run this project.
- **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ReportGenie.git
   cd ReportGenie
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
