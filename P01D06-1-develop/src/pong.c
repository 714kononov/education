#include <stdio.h>

void createtable(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
                 int upper_rocket_l, int ball_x, int ball_y);

int next_movement_x(int ball_x, int ball_y, int dx, int width, int upper_rocket_r, int upper_rocket_l);
int next_movement_y(int ball_y, int dy, int length);

void startgame(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
               int upper_rocket_l, int ball_x, int ball_y, int racket_length, int dx, int dy);

int main() {
    int width = 80;
    int length = 25;
    int countPlayer1 = 0;
    int countPlayer2 = 0;

    int upper_rocket_r = (length - 2) / 2;
    int upper_rocket_l = (length - 2) / 2;

    int ball_x = width / 2;
    int ball_y = length / 2;

    int dx = 1;
    int dy = 1;

    int racket_length = 3;

    startgame(width, length, countPlayer1, countPlayer2, upper_rocket_r, upper_rocket_l, ball_x, ball_y,
              racket_length, dx, dy);
    return 0;
}

void createtable(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
                 int upper_rocket_l, int ball_x, int ball_y) {
    for (int x = 0; x < width; x++) {
        printf("-");
    }
    printf("\n");
    printf("Player 1");
    for (int x = 9; x < width - 9; x++) {
        if (x == width / 2 - 3) {
            printf("%2d", countPlayer1);
        }

        else if (x == width / 2) {
            printf("%d", countPlayer2);
        } else if (x == width / 2 - 1) {
            printf("|");
        } else if (x == width / 2 - 2) {
            printf("|");
        } else
            printf(" ");
    }
    printf("Player 2\n");

    for (int y = 2; y < length; y++) {
        for (int x = 0; x < width; x++) {
            if (y == 2)
                printf("-");
            else if (y == length - 1)
                printf("-");
            else if (x == width - 1 && y >= upper_rocket_r && y <= upper_rocket_r + 2)
                printf("|");
            else if (x == 0 && y >= upper_rocket_l && y <= upper_rocket_l + 2)
                printf("|");
            else if (x == ball_x && y == ball_y)
                printf("@");
            else if (x == width / 2 - 1)
                printf("|");
            else if (x == width / 2 - 2)
                printf("|");
            else
                printf(" ");
        }
        printf("\n");
    }

    printf("\n");
}

int next_movement_x(int ball_x, int ball_y, int dx, int width, int upper_rocket_r, int upper_rocket_l) {
    if (ball_x == width - 2 && ball_y >= upper_rocket_r && ball_y <= upper_rocket_r + 2)
        dx = -1;
    else if (ball_x == 1 && ball_y >= upper_rocket_l && ball_y <= upper_rocket_l + 2)
        dx = 1;

    return dx;
}
int next_movement_y(int ball_y, int dy, int length) {
    if (ball_y == 3)
        dy = 1;
    else if (ball_y == length - 2)
        dy = -1;
    return dy;
}

void startgame(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
               int upper_rocket_l, int ball_x, int ball_y, int racket_length, int dx, int dy) {
    char key = '1';

    while (countPlayer1 < 21 && countPlayer2 < 21 && key != 'q') {
        createtable(width, length, countPlayer1, countPlayer2, upper_rocket_r, upper_rocket_l, ball_x,
                    ball_y);

        dx = next_movement_x(ball_x, ball_y, dx, width, upper_rocket_r, upper_rocket_l);
        dy = next_movement_y(ball_y, dy, length);

        if (ball_x == 0) {
            ball_x = width / 2;
            ball_y = length / 2;
            countPlayer2++;
        }
        if (ball_x == width - 1) {
            ball_x = width / 2;
            ball_y = length / 2;
            countPlayer1++;
        }

        scanf("%c", &key);

        if ((key == 'A' || key == 'a') && upper_rocket_l > 3) {
            upper_rocket_l--;
            ball_y = ball_y + dy;
            ball_x = ball_x + dx;
        } else if ((key == 'Z' || key == 'z') && upper_rocket_l < length - racket_length - 1) {
            ball_y = ball_y + dy;
            ball_x = ball_x + dx;
            upper_rocket_l++;
        }

        else if ((key == 'K' || key == 'k') && upper_rocket_r > 3) {
            ball_y = ball_y + dy;
            ball_x = ball_x + dx;
            upper_rocket_r--;
        }

        else if ((key == 'M' || key == 'm') && upper_rocket_r < length - racket_length - 1) {
            ball_y = ball_y + dy;
            ball_x = ball_x + dx;
            upper_rocket_r++;
        } else if (key == ' ') {
            ball_y = ball_y + dy;
            ball_x = ball_x + dx;
        }

        printf("\033c");
    }

    if (countPlayer1 == 21)
        printf("\nПобеда 1");
    else
        printf("\nПобеда 2");
}
