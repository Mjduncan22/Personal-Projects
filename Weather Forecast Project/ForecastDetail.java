public class ForecastDetail extends Forecast {
    private final int humidity;
    private final double windSpeed;
    private final double feelsLike;

    public ForecastDetail(String city, double temperature, String description,
                            int humidity, double windSpeed, double feelsLike) {
        super(city, temperature, description);
        this.humidity = humidity;
        this.windSpeed = windSpeed;
        this.feelsLike = feelsLike;
    }

    @Override
    public void display() {
        super.display();
        System.out.println("Feels Like: " + feelsLike + "°C");
        System.out.println("Humidity: " + humidity + "%");
        System.out.println("Wind Speed: " + windSpeed + " m/s");
    }
}
