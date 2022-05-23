# Article-research
My project is devoted to the analysis of scientific articles, more precisely, to the calculation of which types of cells are being researched in the article. 
In this training model, I decided to limit myself to analyzing the main blood cell lines, although ideally I would like to analyze all possible cell types. However, for now, I decided to limit myself to a small model based on the analysis of blood cells.

So the database my analysis is based on is in the file "cell lines.db"
![database.png](https://github.com/AlenaSt97/Article-research/blob/main/database.png?raw=true)

In order to determine the type of cells, I decided to analyze 2 hypotheses: the first hypothesis is based on the mention of cell markers in the article. In fact, this is an attempt to "calculate" a cell line based on the specific proteins that appear in the article. The second hypothesis is an analysis of the specific names of cell types that are mentioned in the article.

This stage is performed by the programs "parsnames.py" and "parsmarkers.py"

Thus, for each article there are 2 stages of data collection: first, the first program looks for cell markers and assigns "points" to one or another cell type. Then the second program awards "points" for mentioning the names of specific cell types in the article.

Further, the third program makes the final calculation, which adds up the data of the first and second hypotheses, and also takes into account the length of the article as a whole, and whether or not the analyzed concepts are mentioned among the keywords of the article, in its title, etc.

This is program "finalcalc.py". She puts all the data in the "markersrating.sqlite" file.
![data.png](https://github.com/AlenaSt97/Article-research/blob/main/data.png?raw=true)

And finally, the last program creates a java script file based on all the collected data in order to further build the final graph. I decided that it would be a bar chart.

This is done by the program "graph.py". You can run the "cellrating.htm" file to see the graph that resulted from the analysis of five random articles on the topic of blood cells that I found on NCBI.
![graph.png](https://github.com/AlenaSt97/Article-research/blob/main/graph.png?raw=true)

The numbers on the Y-axis are just "points" that correlate with the mention of cell markers and cell names in the article. I also added some coefficients there to make the data more representative.

I do not claim the reliability of the data obtained, since I did not look for and use the complex mathematical calculations, which is most likely necessary for the correct processing of such data. Right now it's just a model, and the calculations I'm doing are based on my imagination :)
