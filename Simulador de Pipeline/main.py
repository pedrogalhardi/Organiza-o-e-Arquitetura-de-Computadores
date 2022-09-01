import sys
import instTranslator
import stages
import utils

import G_MEM, G_UTL

def main():
    try:
        filename = next(arg for arg in sys.argv[1:] if not arg.startswith('-'))
    except StopIteration:
        filename = 'program.asm'

    # Ler a entrada.asm
    program = utils.readFile(filename)
    programLength = len(program)

    
    # Codifica e carrega .asm na memória
    for i in range(programLength):

        # Remove os comentarios
        if not program[i] or program[i][0] == '#': continue
        encoded = instTranslator.encode(program[i].split('#')[0])

        # Detecta erros, se nenhum, continue carregando
        if encoded not in G_UTL.ERROR:
            G_MEM.INST.append(encoded)
        else:
            print(f'ERROR @ \'{filename}\':')
            print(f'\tLine {i+1}: \'{program[i]}\'')
            if encoded == G_UTL.EINST:
                print('\t\tCouldn\'t parse the instruction')
            elif encoded == G_UTL.EARG:
                print('\t\tCouldn\'t parse one or more arguments')
            elif encoded == G_UTL.EFLOW:
                print('\t\tOne or more arguments are under/overflowing')
            return

    # Imprime o programa como carregado
    utils.printInstMem()
    print()

    
    # Não imprime memória após cada clock
    silent = ('-s' in sys.argv)

    # Pula o passo do relógio
    skipSteps = silent

    # Executar simulação, será executado até que todos os estágios do pipeline estejam vazios
    clkHistory = []
    clk = 0
    while clk == 0 or (G_UTL.ran['IF'][1] != 0 or G_UTL.ran['ID'][1] != 0 or G_UTL.ran['EX'][1] != 0 or G_UTL.ran['MEM'][1] != 0):
        if silent:
            print(' '.join(['─'*20, f'CLK #{clk}', '─'*20]))
        else:
            print(' '.join(['─'*38, f'CLK #{clk}', '─'*38]))

        clkHistory.append([])
        
        stages.EX_fwd()
        stages.WB()
        stages.MEM()
        stages.EX()
        stages.ID()
        stages.IF()
        stages.ID_hzd()


        for i in range(len(G_MEM.REGS)):
            G_MEM.REGS[i] &= 0xFFFFFFFF
        for i in range(len(G_MEM.DATA)):
            G_MEM.DATA[i] &= 0xFFFFFFFF

        
        for stage in ['IF', 'ID', 'EX', 'MEM', 'WB']:
            if G_UTL.ran[stage][1] != 0:
                idle = ' (idle)' if G_UTL.wasIdle[stage] else ''
                clkHistory[clk].append((stage, G_UTL.ran[stage], G_UTL.wasIdle[stage]))
                print(f'> Stage {stage}: #{G_UTL.ran[stage][0]*4} = [{instTranslator.decode(G_UTL.ran[stage][1])}]{idle}.')

        
        if not silent:
            print('─'*(83+len(str(clk))))
           
            print('─'*(83+len(str(clk))))
        clk += 1

        
        if not skipSteps:
            try:
                opt = input('| step: [ENTER] | end: [E|Q] | ').lower()
                skipSteps = (opt == 'e' or opt == 'q')
            except KeyboardInterrupt:
                print('\nExecution aborted')
                exit()

    if silent:
        print()
        utils.printPipelineRegs()
        utils.printRegMem()
        utils.printDataMem()
    else:
        print('Pipeline vazio, finalizando a execução')

    print()
    print(f'Programa foi executado em {clk} clocks')
    print()

    utils.printHistory(clkHistory)

    return

if __name__ == '__main__':
    
    if sys.platform == 'win32': 
        sys.stdout.reconfigure(encoding='UTF-8')

    main()