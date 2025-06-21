import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.json.JSONObject;

public class WeatherAPI {
    private static final String API_KEY = "7f062e57cc83fabb8b61098c40ca3471";
    private final HttpClient client = HttpClient.newHttpClient();

    public ForecastDetail getWeather(String city) {
        try {
            var encodedCity = URLEncoder.encode(city, StandardCharsets.UTF_8);
            var urlStr = "http://api.openweathermap.org/data/2.5/weather?q=" + encodedCity +
                         "&appid=" + API_KEY + "&units=metric";

            var request = HttpRequest.newBuilder()
                .uri(URI.create(urlStr))
                .GET()
                .build();

            var response = client.send(request, HttpResponse.BodyHandlers.ofString());

            var obj = new JSONObject(response.body());
            var main = obj.getJSONObject("main");
            var weather = obj.getJSONArray("weather").getJSONObject(0);
            var wind = obj.getJSONObject("wind");

            double temp = main.getDouble("temp");
            double feelsLike = main.getDouble("feels_like");
            int humidity = main.getInt("humidity");
            double windSpeed = wind.getDouble("speed");
            String description = weather.getString("description");

            return new ForecastDetail(city, temp, description, humidity, windSpeed, feelsLike);

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            return null;
        }
    }
}
