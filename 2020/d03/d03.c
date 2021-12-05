#include "../aoc.h"

#ifndef DAY
#define DAY(num) \
    int day = num;\
    int solution(char *inp, void *p1, void *p2, char *fmt)
#endif

int offset(int x, int y, int width) {
    return (width + 1) * y + (x % width);
}

int num_hit(char *grid, int width, int height, int dx, int dy) {
    int acc = 0;
    int x = 0, y = 0;

    while (y <= height) {
        if (grid[offset(x, y, width)] == '#') {
            acc++;
        }
        y += dy;
        x += dx;
    }
    return acc;
}

DAY(3) {
    int line_len = 0;
    int num_lines = 0;

    char *trav = inp;
    while (*trav++ >= 0x20) {
        line_len++;
    }
    while (*trav > 0) {
        if (*trav++ == '\n') {
            num_lines++;
        }
    }
    printf("line_len = %i; num_lines = %i\n", line_len, num_lines);

    *(int *)p1 = num_hit(inp, line_len, num_lines, 3, 1);
    *(int *)p2 = *(int *)p1 * num_hit(inp, line_len, num_lines, 1, 1);
    *(int *)p2 *= num_hit(inp, line_len, num_lines, 5, 1);
    *(int *)p2 *= num_hit(inp, line_len, num_lines, 7, 1);
    *(int *)p2 *= num_hit(inp, line_len, num_lines, 1, 2);
    sprintf(fmt, "p1 = %%i\np2 = %%i\n");
    return 0;
}
