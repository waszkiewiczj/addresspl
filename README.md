# AddressPL 
## Polish address parser web service

This is a tool for parsing polish addresses based on TERYT database.

For single address it returns list of top 3 best matched addresses with their score.

For instance, given `ul. Kościuszku 12 Słubice` it returns:
```json
[
  {
    "postal_code": "",
    "street": " Kościuszki",
    "building_number": "12",
    "city": {
      "name": "Słubice",
      "score": 1
    },
    "errors": ["Postal code not found"],
    "is_postal_code_matching": false

  },

  {
    "postal_code": "",
    "street": "Mieszka I",
    "building_number": "12",
    "city": {
      "name": "Słubice",
      "score": 1
    },
    "errors": ["Postal code not found"],
    "is_postal_code_matching": false
  },

  {
    "postal_code": "",
    "street": " Konstytucji 3 Maja",
    "building_number": "12",
    "city": {
      "name": "Słubice",
      "score": 1
    },
    "errors": ["Postal code not found"],
    "is_postal_code_matching": false
  }
]
``` 

### Docker container

Application is available as web service in docker container with 80 port exposed.

see: https://hub.docker.com/repository/docker/waszkiewiczj/addressp
