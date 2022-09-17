# EES Directory Generator

This script generates a parent directory in PDF format. Its input is a CSV file with the following fields:

- Timestamp
- Child's First and Last Name
- Grade Level
- Teacher Name
- Guardian Name
- Guardian E-Mail
- Guardian Phone Number
- Guardian Name
- Guardian E-Mail
- Guardian Phone Number
- AM or PM (for pre-K classes; this column is manually filled out)

This CSV can be exported from the [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1gEXitFLUsJx-6El9Wn-6-6Wc0Cl8CD2auO8cjyv-DQk/edit?resourcekey#gid=514288204) that holds the results of the [Google Form](https://docs.google.com/forms/d/1LEmecyWNYuETYEZksG8-MMkgXA0WLO4vRNQqUdqIv-k/edit) used to collect this information.

## Prerequisites

Install [Poetry](https://python-poetry.org). On macos:
```
    brew install poetry
```
Or, follow [the instructions](https://python-poetry.org/docs/) for your platform and install method of choice.

Then, in this directory:
```
    poetry install
```

## Save input CSV

From Google Sheets, `File->Download->Comma Separated Values (.csv)`. 

## Run

```
    poetry run ./directory.py --infile <path to CSV file> --outfile <desired name of PDF file> 
```
