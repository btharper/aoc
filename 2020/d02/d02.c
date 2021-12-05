#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

char* get_input() {
    int size;
    int read;
    FILE *fp;
    char *ret;
    char *pos;

    struct stat statbuf;
    read = stat("../inputs/d02.txt", &statbuf);
    if (read != 0) {
        printf("stat failed: %i\n", read);
        exit(1);
    }
    size = statbuf.st_size + 1;
    pos = (char *)calloc(size, 1);
    ret = pos;

    fp = fopen("../inputs/d02.txt", "r");
    while (read < size - 1) {
        read += fread(pos + read, 1, size - 1, fp);
    }
    fclose(fp);
    return ret;
}

int get_int(char **s) {
    int ret = 0;
    while (0x30 <= **s && **s <= 0x40) {
        ret = ret * 10 + *(*s)++ - 0x30;
    }
    return ret;
}

int d02(char *inp, int *p1, int *p2) {
    int n1, n2;
    char c;
    char *s;
    int count;
    int len;

    do {
        n1 = get_int(&inp);
        inp++; /* dash */
        n2 = get_int(&inp);
        inp++; /* space */
        c = *inp++;
        inp++; /* colon */
        /* space, don't skip */

        len = 0;
        count = 0;
        s = inp;
        while (*inp >= 0x20) {
            if (*inp++ == c) {
                count++;
            }
            len++;
        }
        if (n1 <= count && count <= n2) {
            (*p1)++;
        }
        if (n2 < (len - 0) && ((s[n1] == c) != (s[n2] == c))) {
            (*p2)++;
        }
    } while(*inp++ != 0 && *inp != 0);

    return 0;
}

int main() {
    char *inp = get_input();
    int p1 = 0, p2 = 0;
    int ret = d02(inp, &p1, &p2);
    free(inp);
    printf("p1 = %i\np2 = %i\n", p1, p2);
    return ret;
}
