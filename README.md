# Mission to Mars

![mission_to_mars](Mission_to_Mars/Images/mission_to_mars.png)

This repository has a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 

* Jupyter Notebook file [`mission_to_mars.ipynb`](Mission_to_Mars/MissionToMars.ipynb) has the scraping script, which has been built using BeautifulSoup, Pandas, and Requests/Splinter
* Python script ['scrape_mars.py'](Mission_to_Mars/scrape_mars.py) also has scraping scripts and retuns a Dictionary of Data to the calling function
* Python script ['app.py'](Mission_to_Mars/app.py) utilizes flask to display the data in html format.

Here are some screenshots from the App.
![final_app_part1.png](Mission_to_Mars/Images/final_app_part1.png)
![final_app_part2.png](Mission_to_Mars/Images/final_app_part2.png)
![final_app_part2.png](Mission_to_Mars/Images/final_app_part3.png)