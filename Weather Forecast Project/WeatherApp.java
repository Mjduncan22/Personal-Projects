import java.util.Scanner;

public class WeatherApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        WeatherAPI service = new WeatherAPI();

        System.out.print("Enter a city: ");
        String city = scanner.nextLine();

        scanner.close();

        ForecastDetail forecast = service.getWeather(city);
        if (forecast != null) {
            clearConsole();
            System.out.println("\nCurrent weather for " + city + ":");
            forecast.display();
        } else {
            System.out.println("Could not retrieve weather data.");
        }
    }
    public static void clearConsole() {
        try {
            new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
        } catch (Exception e) {
            System.out.println("Could not clear console.");
        }
    }
}
