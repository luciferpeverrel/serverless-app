const axios = require('axios');

const getWeather = async (city) => {
    const apiKey = process.env.WEATHER_API_KEY;
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    
    try {
        const response = await axios.get(url);
        return {
            city: city,
            temperature: response.data.main.temp,
            weather: response.data.weather[0].description 
        };
    } catch (error) {
        return { city: city, error: "Failed to fetch weather data" };
    }
};

exports.handler = async (event) => {
    const bengaluruWeather = await getWeather("Bengaluru");
    const newYorkWeather = await getWeather("New York");
    
    return {
        statusCode: 200,
        body: JSON.stringify({
            Bengaluru: bengaluruWeather,
            NewYork: newYorkWeather
        })
    };
};