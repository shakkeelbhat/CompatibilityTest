# CompatibilityTest

Automate.py takes QUERY and FILENAME as command-line arguments 

extract(filename) uses GoogleDrive api to read the filename from google-drive and returns the contents of the txt file.

query_content(content) takes the content returned from extract(filename) and utilizes openai langchain to make the QUERY to the content. 

It utilizes OPENAI_API and Google search api  SERPAPI_API to make the query.

