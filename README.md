# AddressPL 
## Polish address parser web service

This is a tool for parsing polish addresses based on TERYT database.

For single address it returns list of top 3 best matched addresses with their score.

For instance, given `ul. Kościuszku 12 Słubice` it returns:
```json
[
  {
    "postal_code": "",
    "street": {"name": "Kościuszki", "score": 0.69},
    "building_number": "12",
    "city": {"name": "Słubice", "score": 1},
    "score": 0.7985,
    "is_postal_code_matching": false
  },

  {
    "postal_code": "",
    "street": {"name": "Mieszka I", "score": 0.4},
    "building_number": "12",
    "city": {"name": "Słubice", "score": 1},
    "score": 0.6269,
    "is_postal_code_matching": false
  },

  {
    "postal_code": "",
    "street": {"name": "Konstytucji 3 Maja", "score": 0.35},
    "building_number": "12",
    "city": {"name": "Słubice", "score": 1},
    "score": 0.6,
    "is_postal_code_matching": false
  }
]
``` 

### Docker container

Application is available as web service in docker container with 80 port exposed.

see: https://hub.docker.com/repository/docker/waszkiewiczj/addresspl
