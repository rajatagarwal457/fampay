# Steps to run

- Setup the API keys in Dockerfile. The field is `YOUTUBE_API_KEYS` You can give multiple keys separted by a comma in a single string  

- docker build -t fampay .

- docker run -p 5000:5000 fampay:latest

  

# Testing Via Postman

  

1)  Set the search term

		URL: http://localhost:5000/api/update-term

		Body: 
		{
			"term": "msfs"
		}

		Method: POST

		Content-Type: Application/json (use raw and json on postman)

  

- query the db with whatever term

		URL: http://localhost:5000/api/search

		Body:{
		"query": "a320",
		"page": 1,
		"per_page": 10
		}

		Method: POST

		Content-Type: Application/json (use raw and json on postman)