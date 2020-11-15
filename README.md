# Finding performance outliers with DeepWalk

# lc-scrape

The scripts used to obtain the ~2,000 samples we analyze in this project from leetcode. The leetcode platform is a place to practice classic algorithms challenges such as "subset sum" and "find median" (typically used to prepare for SE interviews). Once an accepted solution is produced, the user has the ability to view a distribution of other accepted submissions organized by run-time, as well as the corresponding code. 

To access this code, the user must be logged in and have already submitted an accepted solution. We had access to an account with 33 completed array challenges, and I used the cookies from this account in the html scraper to avoid automating the whole sign-in. These cookies last 14 days, and can be replaced for a new account by signing in and copy/pasting the request headers.

## leet.py 

creates an HTML parser with the correct response headers that returns an array of tuples of the form (runtime,percentile) for a given problem that the user has completed. The number of samples provided by leetcode for each problem differs. The cookie field within the "headers" dictionary should be replaced for this method to work with a different account.  

## scrape\_array.py

uses the HTMLParser object defined in leet.py to make an authenticated request to the leetcode API for the code at each accepted submission. The form of the GET request is "/submissions/api/detail/\<prob\_number\>/python3/\<runtime\>". Stores the code, along with its problem number, run-time, and percentile, in a mySQL table called "samples" 
   
# convert-code

Scripts used to create embedding (from Python3 code to DeepWalk vectors), described in the order theywere called.

## to2.py

Queries Python3 samples, converts them to Python2, adds the Python2 code to that sample's entry in the leetcode.samples table.

## toAST.py

Queries Python2 samples, converts them to serialized ASTs using the parse\_python.py script (source: https://eth-sri.github.io/py150), adds the ASTs to that sample's entry in the leetcode.samples table.

## toDD.py

Queries ASTs, converts them to data-dependency graphs by adding an edge between a declared variables and their uses throughout the tree. This turns the tree into a graph structure. The graph structure is then represented as an adjacency list of integers. Adds the adj lists to that sample's entry in the leetcode.samples table.      

# deepwalk

A clone of the DeepWalk project, cloned here so that it can be called to created the embeddings in convert-code/toDW.py. Original source is hosted at https://github.com/phanein/deepwalk.  

# data-analysis

## percentiles.py

Determines which samples are "high performing" and which are "low performing" by sorting the percentile ranges stored in the DB, and marking the top 50th percentile as high and the bottom 50th as low (within each problem).

## visualize.py 

DeepWalk encodes every node, each of which correspond to a statement in the AST, as a high-dimensional vector. visualize.py takes these high dimensional vectors and uses TSNE dimensionality reduction to represent each node in 2D Euclidean space. It then calculates outliers in the x and y direction using interquartile ranges for each leetcode problem. Then, it plots all of the statements in all of the samples for each problem, checking if each statement is an outlier, and if each sample is high or low performing. Statements from high performing samples are then plotted in green, and statements from low performing samples are plotted in red. Outliers are plotted with an 'x' and non-outliers are plotted with an 'o'. The sample problem number and sample ID of each outlier statement is printed to the file "outlier\_stats.txt" for further analysis.  



