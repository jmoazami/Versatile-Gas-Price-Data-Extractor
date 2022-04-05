Versatile Gas Price Data Extractor
by John Shaw Moazami, 
AlphaPoint Challenge


PROBLEM:
Given how exchanges working on the Ethereum blockchain must pay
gas fees everytime a transaction is done on the blockchain,
it is necessary to reduce the costs of these fees to efficently
work on the blockchain and save company funds. To do so, I have 
developed a server written in Python, server.py, that makes use of functions 
written in data.py to ingest free gas price data provided by Etherscan in a mySQL 
data table using my personal API key. I then present this data to the user in a meaningful 
way by giving average gas price over an inputted period of time (with proper error
handling) or providing the most recent gas price in my data.

GETTING STARTED:
To run this project, you must have mySQL downloaded as well as a Python compiler. To start,
Simply run the data.py file for 5-10 minutes to collect data from Etherscan. It is necessary
to first enter your own API key in initialize() along with the name of the database you wish to use
and your MySQL password.To end the data collection process, simply type CTR + C. 

Then, run server.py by typing in the terminal python3 server.py. End the server at any time by typing
CTR + C. Connect with the server with a Firefox browser using the URLS mentioned in the challenge instructions.
Note that the port number to be used is hard-coded as 8880 in the main function of server.py.

SOLUTION/DESIGN:
Etherscan was chosen over EthGasStation because the rate limit of 1 req/5sec was
easily made accessible in the instructions given. I also personally have dealt with
Etherscan more in making my own financial transcations on the Ethereum blochain and 
therefore chose that with which I am more familiar. Additionally, I am personally aware
of a wealth of information on the internet should I come into any issues with Etherscan,
and I knew this may prove a useful resource in the coding process. I am aware that there are trade offs between Etherscan
and EthGasStation, but thought any small differences between the two to be neglible for the purposes of this project.
 I also chose Python because of its incredibly diverse array of packages that would help me in writing my project. 
 I particularly found the json package useful in this project when ingesting data from Etherscan. I am
  aware that other programming languages are encouraged in the completion of this project and am certain that
I would be able to handle such a project in a more preferred language like C#. For timing issues, however,
I chose to use Python, a language that I am more familiar with and experienced in. I also believe that the
Open-source nature of Python along with how dynamic it is made it a clear programming language choice.
I chose to work with mySQL as it is the database management system I am most familiar with. Should this
program be run on anyone's personal device that has mySQL workbench downloaded, all Ethereum gas data will
 be uploaded in a table called gas_data (which includes time, low gas price, fast gas price, average gas price, 
 and last block chain number). Lastly, I chose to write a REST server over a Websocket server because there 
 seemed to be more resources available online to help me develop it. I have limited experience writing either type of server 
 and relied heavily on reading about REST servers. 

 Upon receiving my API key, I designed my program such that data is retrieved every second as to avoid
going over the rate limit and avoid being rejected data upon request. I made sure to present all
gas data in units Gwei, as provided by Etherscan. Additionally, I put all personal user 
information, such as my API key, password for MySQL, and even database name into a config.py file,
which is then included in a .gitignore file. This ensures that, should this code be published on GitHub,
no personal information will be published with it as to maintain the security and privacy of
my users. For the purposes of running the code from the grader's point of view, however,  I have included
my config.py file in this repo so that my API key can be used for testing.

In terms of error handling, I do not handle 404 Not Found errors as I view the messages provided already
as a built-in form of error handling when the user mistypes the proper GET request. If I were to spend more time
on this project, I would research how to handle GET requests that are not the expected ones I handle in my code so as
to present my own message to the user in the event that they mistype the proper URL. I believe I am lacking error handling
for GET /gas, and I believe this addition would allow me to implement error handling in this part of the project and make this
code more production-ready. Additionally, I would add another feature that factors in another valuable piece of data provided 
by Etherscan that is ignored, for the most part, by this challenge--usedGasRatio, which provides insight as to how busy 
the Ethereum blockchain is at a given moment and therefore provides insight on gas fee price. My addition could be as simple as 
presenting usedGasRatio data alongside gas price or even writing code that checks to see if the current usedGasRatio is above
or below a certain benchmark, thereby advising the user to wait or not on making any purchases on the Ethereum blockchain.


In the case of GET /average?fromTime=&toTime=, I make sure to handle if improper fromTime and toTime values already
inputted, such as if the inputted values are not exclusively digits or if toTime > the latest time associated
with data in my mySQL table. 
