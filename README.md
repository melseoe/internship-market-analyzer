# internship-market-analyzer

A Python tool that scrapes and visualizes internship data from Youthall to identify market trends in locations, sectors, and top hiring companies using: [cite: 20, 53]
- Python 
- BeautifulSoup
- Selenium 
- Pandas
- Matplotlib.

### 3 Scraping Stages I Used:

1. **General Data Collection**: Scraping post titles, companies, and URLs.
2. **Deep-Dive Extraction**: Using Selenium to get specific details like department, location, and sector.
3. **Visual Analytics**: Generating insights through bar and pie charts.

**Note**: I checked the robots.txt of Youthall site beforehand and added a crawl_delay while creating this project to learn a concept that is new to me by trying to be a *polite* agent and understand the web ethics.

## How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/melseoe/internship-market-analyzer.git](https://github.com/melseoe/internship-market-analyzer.git)
   
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt

3. **Run the analysis:**
Execute the main script to start the scraping and visualization process:
	```bash
	python Main.py
