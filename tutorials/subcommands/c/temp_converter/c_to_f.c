# include <stdio.h>

int converter()
{
    float celsius, fahrenheit;

    /* Input temp in celsius */
    printf("\nEnter the temperature in Celsius: \n");
    scanf("%f", &celsius);

    /* C to F conversion formula */
    fahrenheit = (celsius * 9 / 5) + 32;

    printf("\n%.2f Celsius = %.2f Fahrenheit\n\n", celsius, fahrenheit);

    return 0;
}
