

# YouTube Recommendation Network Analysis

This project explores YouTube's recommendation network by scraping video data and analyzing the relationships between videos. It includes scripts for data collection, network construction, and analysis.

## Project Structure

```
.
├── code/
│   ├── scrape_youtube.py        # Script for scraping YouTube data
│   ├── youtube_network_1.ipynb  # Notebook for constructing the recommendation network and overview network analysis 
│   ├── youtube_network_2.ipynb  # Notebook for constructing the recommendation network and network analysis of channel feature
├── data/
│   ├── youtube_recommendation_network.csv  # Scraped data in CSV format
```
---

## Installation and Setup

### Prerequisites
- Python 3.x
- Colab Notebook
- Required Python libraries:
  - `networkx`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `selenium` (for web scraping)

### Installation
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-folder]
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Step 1: Scrape YouTube Data
Run the `scrape_youtube.py` script to collect recommendation data:
```bash
python code/scrape_youtube.py
```

### Step 2: Construct the Network and Network analysis
- Open `youtube_network_1.ipynb` and `youtube_network_2.ipynb` in colab and follow the steps to build the recommendation network graph and analyze the network using metrics like centrality, shortest paths, and more
---

## Dataset Structure

The scraped dataset includes the following columns:

| Column Name             | Description                                           |
|-------------------------|-------------------------------------------------------|
| Source Video ID         | Unique identifier of the source video                |
| Source Title            | Title of the source video                            |
| Source Channel Name     | Name of the source channel                           |
| Source Views            | View count of the source video                       |
| Source Publish Time     | Publish date and time of the source video            |
| Target Video ID         | Unique identifier of the recommended video           |
| Target Title            | Title of the recommended video                       |
| Target Channel Name     | Name of the recommended video's channel              |
| Target Views            | View count of the recommended video                  |
| Target Publish Time     | Publish date and time of the recommended video       |
| Depth                  | Depth in the recommendation network                  |

---

## Network Analysis

Key metrics analyzed in the project include:
- **In-Degree and Out-Degree Centrality**: Identify influential videos.
- **Betweenness Centrality**: Measure the importance of videos in connecting different parts of the network.
- **Closeness Centrality**: Assess how easily a video can reach others.
- **Network Diameter and Path Length**: Evaluate the overall structure of the recommendation network.

---

## Results

The analysis provides insights into:
- Network structural properties
- Echo chambers in recommendation algorithm
---

## Contributors

- **Xueying Cheng**
- **Jingyi Chen**
- **Jinglei Huang**
- **Zhiyu Wei**

---

