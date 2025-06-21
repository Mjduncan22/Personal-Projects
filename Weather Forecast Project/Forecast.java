public class Forecast {
    private final String city;
    private final double temperature;
    private final String description;

    public Forecast(String city, double temperature, String description) {
        this.city = city;
        this.temperature = temperature;
        this.description = description;
    }

    public void display() {
        System.out.println("Weather in " + city);
        System.out.println("Temperature: " + temperature + "°C");
        System.out.println("Description: " + description);
    }
}
