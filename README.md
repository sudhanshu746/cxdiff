# CXDiff: A Document Comparison App

This application is designed to compare documents and highlight differences, supporting both Excel and CSV file formats. It allows users to upload two files of the same format, select unique identifiers for comparison, and then view the differences between them in a highlighted manner.

## Features

- Support for comparing **Excel** and **CSV** files.
- Option to select unique identifier columns to accurately compare records.
- Differences are displayed with red highlights for easy identification.
- Download the comparison result as an Excel file.

## Requirements

Before you can run the app, make sure you have the following packages installed:
Install them using pip:
```
pip install -r requirement.txt
```



## Usage

To start the Streamlit app, navigate to the directory containing the `app.py` script and run the following command:

```
streamlit run app/cxdiff.py
```

### Step-by-Step Guide

1. Start the application.
2. Select the file type (CSV or Excel) that you wish to compare.
3. Upload the first document using the provided file uploader.
4. If you chose Excel, select the desired sheet from the uploaded document.
5. Choose the column(s) that will serve as the unique identifier for comparison.
6. Repeat steps 3 to 5 for the second document.
7. Click the 'Compare Documents' button to initiate the comparison process.
8. The application will display the differences between the two documents. Differences will be highlighted in red.
9. Optionally, download the comparison results by clicking on the 'Download Comparison Excel' button.

## Considerations

- Ensure that the documents to be compared have some common columns that can serve as unique identifiers.
- Column names used as unique identifiers should be present in both documents and contain the same type of values which uniquely identify each record.

## Troubleshooting

If you encounter any issues, double-check the following:
- Both files are uploaded and both sheets are selected for Excel files.
- The list of unique identifiers is correctly provided and matches across both documents.
- Uploaded files are of the correct format and are not corrupted.

In case of errors during the comparison, the app will provide a specific error message to help identify the problem.

## Contribution

Contributions to improve the app are welcome. Please feel free to fork the repository, make changes, and submit a pull request.