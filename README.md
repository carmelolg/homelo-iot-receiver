# homelo-iot-receiver
Microservice that receive and provide informations of the home sensor's data

## What do you need
- An instance of MongoDB
- An instance of your DB with inside the following Collection: **Detection**
- You should define two environment variables
  - **MONGO_URL**
  - **MONGO_DB_NAME**
  
## How to save your sensor's data
From your **Arduino/Raspberry/ESP32/ESP8622** microcontroller just generate an **HTTP-POST** request:
- **URL**:    will be your host address
- **Path**:   /sensor
- **Body**:   { data: "2020-07-03", temperature: 25.6, ... }


