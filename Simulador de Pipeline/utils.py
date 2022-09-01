import instTranslator
import G_MEM, G_UTL

def readFile(filename):
    content = []
    with open(filename, 'r', encoding='UTF-8') as f:
        for l in f:
            s = l.strip()
            if s:
                content.append(s)

    return content

#Tentei criar uma "Interface" para minha saída

def printInstMem():
    print('╔═════╦═════════════════════════════[PROGRAM]═══════════╦════════════════════════╗')

    for i in range(len(G_MEM.INST)):
        print('║ {:>3} ║ 0x{:08X} = 0b{:032b} ║ {:<22} ║'.format(i*4, G_MEM.INST[i], G_MEM.INST[i], instTranslator.decode(G_MEM.INST[i])))

    print('╚═════╩═════════════════════════════════════════════════╩════════════════════════╝')



def printHistory(clkHistory):
    
    history = [[' ' for i in range(len(clkHistory))] for i in range(len(G_MEM.INST))]
    for i in range(len(clkHistory)):
        for exe in clkHistory[i]:
            if exe[2]: 
                history[exe[1][0]][i] = ' '
                
            else:
                history[exe[1][0]][i] = exe[0]

    # Quantidades de clocks utilizados

    print('╔═════╦════════════════════════╦' + '═'*(6*len(clkHistory)) + '╗')
    print('║ Mem ║ ' + 'Clock #'.center(22) + ' ║', end='')
    for i in range(len(clkHistory)):
        print(str(i).center(5), end=' ')
    print('║')
    print('╠═════╬════════════════════════╬' + '═'*(6*len(clkHistory)) + '╣')

    
    for i in range(len(history)):
        print('║ {:>3} ║ {:>22} ║'.format(i*4, instTranslator.decode(G_MEM.INST[i])), end='')
        for j in range(len(history[0])):
            print(history[i][j].center(5), end=' ')
        print('║')
    print('╚═════╩════════════════════════╩' + '═'*(6*len(clkHistory)) + '╝')