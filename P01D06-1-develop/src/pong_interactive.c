
#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void createtable(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
                 int upper_rocket_l, int ball_x, int ball_y);

void table(int countPlayer1, int countPlayer2);

int next_movement_x(int ball_x, int ball_y, int upper_rocket_r, int upper_rocket_l, int dx, int width);
int next_movement_y(int ball_y, int dy, int length);

void startgame(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
               int upper_rocket_l, int ball_x, int ball_y, int racket_length, int dx, int dy);

int main() {
    initscr();
    cbreak();
    noecho();
    nodelay(stdscr, TRUE);

    int width = 80;
    int length = 25;
    int countPlayer1 = 0;
    int countPlayer2 = 0;

    int upper_rocket_r = (length - 2) / 2;
    int upper_rocket_l = (length - 2) / 2;

    int ball_x = width / 2;
    int ball_y = length / 2;

    srand(time(NULL));
    int dx = (rand() % 2) * 2 - 1;
    int dy = (rand() % 2) * 2 - 1;

    int racket_length = 3;

    startgame(width, length, countPlayer1, countPlayer2, upper_rocket_r, upper_rocket_l, ball_x, ball_y,
              racket_length, dx, dy);
}

void createtable(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
                 int upper_rocket_l, int ball_x, int ball_y) {
    clear();

    table(countPlayer1, countPlayer2);

    for (int y = 0; y < length; y++) {
        for (int x = 0; x < width; x++) {
            if ((y == upper_rocket_l || y == upper_rocket_l + 1 || y == upper_rocket_l + 2) && x == 0)
                mvprintw(y, x, "|");
            else if ((y == upper_rocket_r || y == upper_rocket_r + 1 || y == upper_rocket_r + 2) &&
                     x == width - 1)
                mvprintw(y, x, "|");
            else if (x == ball_x && y == ball_y)
                mvprintw(y, x, "@");
            else if (y == 0)
                mvprintw(y, x, "-");
            else if (y == length - 1)
                mvprintw(y, x, "-");
            else if (x == width / 2)
                mvprintw(y, x, ":");
            else if (x == width / 2 + 1)
                mvprintw(y, x, ":");
        }
    }
}

void table(int countPlayer1, int countPlayer2) {
    int countPlayer;
    int x;

    for (int i = 0; i <= 4; i++) {
        if (i == 0) {
            countPlayer = countPlayer1 / 10;
            x = 10;
        }
        if (i == 1) {
            countPlayer = countPlayer1 % 10;
            x = 20;
        }
        if (i == 3) {
            countPlayer = countPlayer2 / 10;
            x = 50;
        }
        if (i == 4) {
            countPlayer = countPlayer2 % 10;
            x = 60;
        }
        switch (countPlayer) {
            case 0:
                mvprintw(1, x, "   #####  ");
                mvprintw(2, x, "  ##   ## ");
                mvprintw(3, x, " ##     ##");
                mvprintw(4, x, " ##     ##");
                mvprintw(5, x, " ##     ##");
                mvprintw(6, x, "  ##   ## ");
                mvprintw(7, x, "   #####  ");
                break;
            case 1:
                mvprintw(1, x, "   ##  ");
                mvprintw(2, x, " ####  ");
                mvprintw(3, x, "   ##  ");
                mvprintw(4, x, "   ##  ");
                mvprintw(5, x, "   ##  ");
                mvprintw(6, x, "   ##  ");
                mvprintw(7, x, " ######");
                break;
            case 2:
                mvprintw(1, x, "  ####### ");
                mvprintw(2, x, " ##     ##");
                mvprintw(3, x, "        ##");
                mvprintw(4, x, "  ####### ");
                mvprintw(5, x, " ##       ");
                mvprintw(6, x, " ##       ");
                mvprintw(7, x, " #########");
                break;
            case 3:
                mvprintw(1, x, "  ####### ");
                mvprintw(2, x, " ##     ##");
                mvprintw(3, x, "        ##");
                mvprintw(4, x, "  ####### ");
                mvprintw(5, x, "        ##");
                mvprintw(6, x, " ##     ##");
                mvprintw(7, x, "  ####### ");
                break;
            case 4:
                mvprintw(1, x, " ##       ");
                mvprintw(2, x, " ##    ## ");
                mvprintw(3, x, " ##    ## ");
                mvprintw(4, x, " ##    ## ");
                mvprintw(5, x, " #########");
                mvprintw(6, x, "       ## ");
                mvprintw(7, x, "       ## ");
                break;
            case 5:
                mvprintw(1, x, " ########");
                mvprintw(2, x, " ##      ");
                mvprintw(3, x, " ##      ");
                mvprintw(4, x, " ####### ");
                mvprintw(5, x, "       ##");
                mvprintw(6, x, " ##    ##");
                mvprintw(7, x, "  ###### ");
                break;
            case 6:
                mvprintw(1, x, "  ####### ");
                mvprintw(2, x, " ##     ##");
                mvprintw(3, x, " ##       ");
                mvprintw(4, x, " ######## ");
                mvprintw(5, x, " ##     ##");
                mvprintw(6, x, " ##     ##");
                mvprintw(7, x, "  ####### ");
                break;
            case 7:
                mvprintw(1, x, " ########");
                mvprintw(2, x, " ##    ##");
                mvprintw(3, x, "     ##  ");
                mvprintw(4, x, "    ##   ");
                mvprintw(5, x, "   ##    ");
                mvprintw(6, x, "   ##    ");
                mvprintw(7, x, "   ##    ");
                break;
            case 8:
                mvprintw(1, x, "  ####### ");
                mvprintw(2, x, " ##     ##");
                mvprintw(3, x, " ##     ##");
                mvprintw(4, x, "  ####### ");
                mvprintw(5, x, " ##     ##");
                mvprintw(6, x, " ##     ##");
                mvprintw(7, x, "  ####### ");
                break;
            case 9:
                mvprintw(1, x, "  ####### ");
                mvprintw(2, x, " ##     ##");
                mvprintw(3, x, " ##     ##");
                mvprintw(4, x, "  ########");
                mvprintw(5, x, "        ##");
                mvprintw(6, x, " ##     ##");
                mvprintw(7, x, "  ####### ");

                break;

            default:
                break;
        }
    }
}

int next_movement_x(int ball_x, int ball_y, int upper_rocket_r, int upper_rocket_l, int dx, int width) {
    if ((ball_x == 1 && ball_y >= upper_rocket_l && ball_y <= upper_rocket_l + 2) ||
        (ball_x == width - 2 && ball_y >= upper_rocket_r && ball_y <= upper_rocket_r + 2)) {
        dx *= -1;
    }
    return dx;
}
int next_movement_y(int ball_y, int dy, int length) {
    if (ball_y == 1 || ball_y == length - 2) {
        dy *= -1;
    }
    return dy;
}

void startgame(int width, int length, int countPlayer1, int countPlayer2, int upper_rocket_r,
               int upper_rocket_l, int ball_x, int ball_y, int racket_length, int dx, int dy) {
    char key = getch();

    while (countPlayer1 < 21 && countPlayer2 < 21 && key != 'q') {
        timeout(150);
        createtable(width, length, countPlayer1, countPlayer2, upper_rocket_r, upper_rocket_l, ball_x,
                    ball_y);

        dx = next_movement_x(ball_x, ball_y, upper_rocket_r, upper_rocket_l, dx, width);
        dy = next_movement_y(ball_y, dy, length);

        if (ball_x == 0) {
            ball_x = width / 2;
            ball_y = length / 2;
            countPlayer2++;
            dx = (rand() % 2) * 2 - 1;
            dy = (rand() % 2) * 2 - 1;

        } else if (ball_x == width) {
            ball_x = width / 2;
            ball_y = length / 2;
            countPlayer1++;
            dx = (rand() % 2) * 2 - 1;
            dy = (rand() % 2) * 2 - 1;
        }

        ball_y = ball_y + dy;
        ball_x = ball_x + dx;

        key = getch();

        if ((key == 'A' || key == 'a') && upper_rocket_l > 1) {
            upper_rocket_l--;

        } else if ((key == 'Z' || key == 'z') && upper_rocket_l < length - 1 - racket_length) {
            upper_rocket_l++;

        } else if ((key == 'K' || key == 'k') && upper_rocket_r > 1) {
            upper_rocket_r--;

        } else if ((key == 'M' || key == 'm') && upper_rocket_r < length - 1 - racket_length) {
            upper_rocket_r++;
        }
    }

    endwin();

    if (countPlayer1 == 21)
        printf("\nПобедил игрок 1");
    else
        printf("\nПобедил игрок 2");
}
