The application has two endpoints:

1) Ingest Contributors Endpoint:
   
      Accepts a POST request with a JSON body containing a GitHub public repository owner and repo name.

      Fetches all contributors of the specified repository from GitHub's API.

      Inserts contributors' data into a MongoDB collection.
   
      Returns a success message along with the total number of contributors ingested.


2) Get Contributor Info Endpoint:

      Accepts a POST request with parameters: owner, repo, username, and type (e.g., "User" or "Bot").
  
      Retrieves contributor information from the MongoDB collection based on the provided parameters.
  
      Returns the username, avatar URL, whether the contributor is a site admin, and the number of contributions.
  
      Add input validation and error handling as necessary
