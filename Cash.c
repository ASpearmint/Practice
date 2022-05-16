#include <stdio.h>
//floating point equality doesnt work dipshit multiply by 100 and use cents

int main(void) {
    double original_number,total1,total2,total3,final_value;
    int quarter,dime,nickel,penny;

    while (1 == 1) {
    
    printf("Please type in a number: ");
    scanf("%lf", &original_number);
    

    if ((original_number <= 0 ) || (original_number > 2000000000)) { 
        printf("Please type in a number between 0 and 2 billion");
        break;

    }
    
    else {
        
        quarter = original_number / .25;
        total1 = original_number - (quarter * .25);
        dime = total1/.10;
        total2 = total1 - (dime * .10);
        nickel = total2/.05;
        total3 = total2 - (nickel * .05);
        penny = total3/.01;
        final_value = total3 - (penny * .01);
        printf("The final value is %lf.", final_value);
        printf("\n");
        printf("Number of quarters: %d", quarter);
        printf("\n");
        printf("Number of dimes: %d", dime);
        printf("\n");
        printf("Number of nickels: %d", nickel);
        printf("\n");
        printf("Number of pennies: %d", penny);
        break;
    }
    }
}


