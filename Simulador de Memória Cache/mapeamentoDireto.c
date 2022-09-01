#include <stdio.h>

int tag[8];

int main( )
{
    int addr;
    int i, t;
    int acertos, acessos, perdidos;
    int ciclos;
    FILE *fp;

    fp = fopen("teste_1.txt", "r");
    acertos = 0;
    acessos = 0;
    perdidos = 0;
    ciclos = 0;

    while (fscanf(fp, "%x", &addr) > 0) {
        /* simula um cache de mapeamento direto com 8 palavras */
        acessos += 1;
        printf("%3d: 0x%08x ", acessos, addr);
        i = (addr >> 2) & 7;
        t = addr | 0x1f;
        if (tag[i] == t) {
            acertos += 1;
            printf("Acertos%d ", i);
        } else {
        printf("Perdidos ");
        tag[i] = t;
        ciclos = ciclos + 100;
        perdidos++;
    }
        for (i = 0; i < 8; i++)
            printf("0x%08x ", tag[i]);
        printf("\n");
    }
    printf("\nAcertos = %d\n  \nAcesso = %d\n \nPerdidos = %d\n \nTaxa de acerto = %f\n", acertos, acessos, perdidos, ((float)acertos)/perdidos);
}