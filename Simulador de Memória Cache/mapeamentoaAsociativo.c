#include <stdio.h>

int tag[8];
int mru[8] = {7,6,5,4,3,2,1,0};

void mruUpdate(int index)
{
    int i;
    // encontra o índice no mru
    for (i = 0; i < 8; i++)
        if (mru[i] == index)
            break;
    // move os refs anteriores um depois
    while (i > 0) {
        mru[i] = mru[i-1];
        i--;
    }
    mru[0] = index;
}

int main( )
{
    int addr;
    int i;
    int acertos, acessos, perdidos;
    int ciclos;
    FILE *fp;
    
    fp = fopen("teste_2.txt", "r");
    acertos = 0;
    acessos = 0;
    perdidos = 0;
    ciclos = 0;

    while (fscanf(fp, "%x", &addr) > 0) {
/* simula cache totalmente associativo com 8 palavras */

        acessos += 1;
        printf("%3d: 0x%08x ", acessos, addr);
        for (i = 0; i < 8; i++) {
            if (tag[i] == addr) {
                acertos += 1;
                printf("Acerto%d ", i);
                mruUpdate(i);
                break;
            }
        }
        if (i == 8) {
            /* aloca entrada */

            printf("Perdidos ");
            i = mru[7];
            tag[i] = addr;
            ciclos = ciclos + 100;
            perdidos++;
            mruUpdate(i);
        }
        for (i = 0; i < 8; i++)
            printf("0x%08x ", tag[i]);
        for (i = 0; i < 8; i++)
            printf("%d ", mru[i]);
        printf("\n");
    }
    printf("\nAcertos = %d\n  \nAcesso = %d\n \nPerdidos = %d\n \nTaxa de acerto = %f\n", acertos, acessos, perdidos, ((float)acertos)/perdidos);
}