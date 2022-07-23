# What to do
A friend of mine told me that he needs to save some .eml files (emails) in a folder and extract specific information from them.

We need to extract from "Resum hores:" to "Salut!" which is like the summary section of the entire email report. He told me it would be nice to pass the information to a csv file.

So I did it :) 

The program is "smart enough" to avoid duplicating output information if it has been already processed and just process the new info. To check that, you can execute the program once, remove a few lines from output files and execute the program multiple times to see that no line is duplicated and new results are added.

# How to execute the program (Linux/Mac)
- In the root directory of the project, execute
```bash
python3 python/main.py
```

# How to execute the tests (Optional)
### First, install project dependencies
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r python/requirements.txt
```

### And run pytest
```bash
pytest
```

# Execute the program using Docker (working with Mac, Linux, Windows, etc.)
### Install and configure Docker
https://www.docker.com/

### Build the image
```bash
docker build -t stores_summary  .
```

### Run the container
```bash
docker run --rm -it -v ${PWD}/results:/app/results stores_summary 
```

# Execute the unit tests using Docker (optional)
### Build the image
```bash
docker build -t stores_summary  .
```

### Run the tests
```bash
docker run --rm -it stores_summary  pytest
```
As you can see we have provided the "pytest" command as an entry point for the container, overriding the one specified in the Dockerfile.

# csv files format
## departments.csv
date, department, hours

## summary.csv
date, effective_hours, total_hours, percentage_effective_hours_to_total

### Notes
When reading input files (the email's content) with any text editor, you will see the string 

\> Gr=C3=A0cies! 

but when you print the content of the input files using the python parsing library, you will se 

\> Gràcies!

In order to explore the contents of the eml files (and choose a sentinel to extract the text block you are interested in), always use the Pyton parser and output it to the console, otherwise you will be using a sentinel you will not find in the text parsed (because reading the file with a text reader is different than doing it with the python parser).

The original emails that my friend gave me are not included here. Instead, I have created and send some sample emails to myself and I have saved them in the input_files forder in order to not include any personal information from anyone. The format of the emails is the same ensuring it works both with this example emails and the ones from my friend.

Happy coding!

### Useful links
https://docs.python.org/3.7/library/email.parser.html

https://enjoylifescience.com/2020/11/05/analyzing-emails-in-python/

https://realpython.com/python-csv/

https://docs.docker.com/storage/bind-mounts/
