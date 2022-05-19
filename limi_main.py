import os

class Line:
    '''
    Classe Line usada para criar objetos que representam uma linha de
    programa com o contéudo da linha e a identificação de arquivo e
    número de linha para posterior referência.
    '''
    def __init__(self, program_name, line_number, line):
        self.program_name = program_name
        self.line_number = line_number
        self.line = line

    def __str__(self):
        return f'{self.program_name}: {self.line_number} --> {self.line}'

class Command:
    '''
    A classe Command é usada para criar objetos que representam comandos
    válidos.
    '''
    def __init__(self, item):
        # Tokens são criados separando uma linha de comando em tokens
        line = item.line
        tokens = line.split(' ')
        
        # Todo comando deve ter 2 ou 3 tokens.
        if len(tokens) == 1:
            messages = [
                    'Erro na definição de comandos.',
                    'Número incorreto de tokes. Tem menos de 2 tokens.']
            error_msg(item, messages)
        elif len(tokens) > 3:
            messages = [
                    'Erro na definição de comandos.',
                    'Número incorreto de tokes. Tem mais de 3 tokens.']
            error_msg(item, messages)
        
        # O primeiro token é sempre uma operação
        self.operation = tokens[0]

        '''
        Se o token de operação for '+', '-', 'C' ou 'E', seu argumento
        deve ser inteiro.
        Caso contrário o argumento será string.
        '''
        if self.operation in '+-CE':
            try:
                self.argument = int(tokens[1])
            except ValueError:
                messages = [
                    'Erro na definição de comandos.',
                    f'Argumento da operação \'{self.operation}\' deve ser inteiro.']
                error_msg(item, messages)
        else:
            self.argument = tokens[1]

        '''
        Para comandos com 3 tokens o ultimo token é um rótulo.
        Para comandso com 2 tokens usamos None para o rótulo.
        '''
        if len(tokens) == 3:
            self.label = tokens[2]
        else:
            self.label = None

        '''
        item é adicionado como trace para uso na visualização de erros
        e traceback
        '''
        self.trace = item

    def __str__(self):
        '''
        Overloading da representação em string de um objeto tipo Command.
        '''
        if self.label is None:
            return f'{self.operation} {self.argument}'
        else:
            return f'{self.operation} {self.argument} {self.label}'

def register_value(item, registers):
    '''
    Função para verificar se uma definição de registro foi feita de
    forma correta.
    Retorna o valor a ser inicializado no registrador
    durante a análise.
    '''

    # Tokens são criados separando uma linha de comando em tokens.
    line = item.line
    tokens = line.split(' ')

    '''
    Uma definição de registradores devem ter exatamente 3 tokens.
    O formato deve ser R X V onde R é para indicar que a linha de
    comando é uma definição de registrador, X é o identificador de
    registro e V é o valor a ser inicializado.
    '''
    if len(tokens) != 3:
        messages = [
                'Erro na definição de registradores.',
                'Número incorreto de tokes. Deveriam ser 3 tokens.']
        error_msg(item, messages)

    # Um identificador de registrador deve ser um inteiro
    try:
        reg_id= int(tokens[1])
    except ValueError:
        messages = [
            'Erro na definição de registradores.',
            'Identificação de um registrador deve ser inteiro.']
        error_msg(item, messages)

    # Um valor de inicialização de registrador deve ser inteiro
    try:
        reg_val = int(tokens[2])
    except ValueError:
        messages = [
            'Erro na definição de registradores.',
            'Valor inicializado em um registrador deve ser inteiro.']
        error_msg(item, messages)

    '''
    Os registradores devem ser definidos em ordem crescente e sequencial
    iniciando em 1. Dessa forma, considerando que a lista de registradores
    começa como [0,] temos que a identificação de um novo registro é
    precisamente o tamanho da lista antes de sua inclusão.
    '''
    if reg_id!= len(registers):
        messages = [
            'Erro na definição de registradores.',
            'Ordem incorreta dos identificadores.']
        error_msg(item, messages)

    # Se nenhum problema for encontrado o valor de inicialização é retornado.
    return reg_val

def analyse_module_calling(item, registers):
    '''
    Função para analisar um comando de chamada de módulo.
    
    '''
    line = item.line
    arguments = line.split('(')[1].split(')')[0]
    if not arguments:
        messages = [
            'Erro na chamada de módulo.',
            f'É precisso passar argumentos ao chamar um módulo']
        error_msg(item, messages)
    else:
        for arg in arguments.split(','):
            try:
                X = int(arg)
            except ValueError:
                messages = [
                    'Erro na chamada de módulo.',
                    f'Argumentos do módulo devem ser inteiros separados por vírgula']
                error_msg(item, messages)  
            if X >= len(registers):
                messages = [
                    'Erro na chamada de módulo.',
                    f'O argumento {X} não é um registrador válido.']
                error_msg(item, messages) 

    module_name = line.split(' ')[1].split('(')[0]
    module_path_name = f'lib/{module_name}.lmm'
    if not os.path.isfile(module_path_name):
        messages = [
            'Erro na chamada de módulo.',
            f'Módulo \'{module_name}\' não encontrado em \'lib\'']
        error_msg(item, messages)

def run_debug_mode(registers, commands, CP):
    print(f'Depurando::: Registradores: {registers} --- Comando: {commands[CP]}')

def verify_program_integrity(commands, registers, item):
    if len(registers) == 1:
        messages = [
            'Erro de integridade do programa.',
            f'Não foram definidos registradores']
        error_msg(item, messages)        
    if commands[-1].operation != 'F':
        messages = [
            'Erro de integridade do programa.',
            f'O programa não termina com operação F.']
        error_msg(item, messages)   


def error_msg(item, messages):
    line = item.line
    line_number = item.line_number
    program_name = item.program_name
    loc = f'{program_name}: {line_number}'
    print(50*'-')
    for traceback in traceback_list:
        tb_line = traceback.line
        tb_line_number = traceback.line_number
        tb_program_name = traceback.program_name
        tb_loc = f'{tb_program_name}: {tb_line_number}'
        print(f'<<< ERRO - [Traceback] - {tb_loc} >>> {tb_line}')
    print(f'<<< ERRO - {loc} >>> {line}')
    for message in messages:
        print(f'<<< ERRO - {loc} >>> {message}')
    print(50*'-')
    raise SystemExit(0)

def execute(program_name, args_val = []):
    args_len = len(args_val)
    program = generate_program(program_name)
    registers, commands = program_scanning(program, args_val)
    registers = run_program(registers, commands)
    if args_len:
        return registers[1:args_len+1] # Offset de 1 para deixar o elemento 0 intacto
    else:
        return None

def generate_program(program_name):
    program = []
    with open(program_name, 'r') as program_content:
        for ln, line in enumerate(program_content.readlines()):
            cleaned_line = line.strip().strip('\n')
            item = Line(program_name, ln + 1, cleaned_line)
            if cleaned_line:
                program.append(item)
    return program

def program_scanning(program, args_val):
    """Analisar o conteúdo de program e criar registers e commands"""
    registers = [0, ]
    commands  = []

    for item in program:
        line = item.line
        tokens = line.split(' ')

        if tokens[0] == 'R':
            if args_val:
                val = args_val.pop(0)
            else:
                val = register_value(item, registers)
            registers.append(val)

        if tokens[0] == '.':
            analyse_module_calling(item, registers)
            commands.append(Command(item))

        if len(tokens[0]) == 1 and tokens[0] in '+-PCEF':
            commands.append(Command(item))

    verify_program_integrity(commands, registers, item)

    return registers, commands

def run_module(module, registers):
    args = module.split('(')[1].split(')')[0].split(',')
    args_val = [registers[int(arg)] for arg in args]

    module_name = module.split('(')[0]
    module_path_name = f'lib/{module_name}.lmm'

    new_reg = execute(module_path_name, args_val)
    for arg, reg in zip(args, new_reg):
        registers[int(arg)] = reg

    return registers

def run_program(registers, commands):
    CP = 0
    while True:
        if debugging_mode:
            run_debug_mode(registers, commands, CP)

        command = commands[CP]
        ope = command.operation
        arg = command.argument
        lab = command.label

        if ope == 'F':
            break
        elif ope =='+':
            registers[arg] += 1
            CP += 1
        elif ope =='-':
            registers[arg] -= 1
            CP += 1
        elif ope =='P':
            for line, cmd in enumerate(commands):
                if cmd.label == arg:
                    CP = line
                    break
        elif ope == 'C':
            if registers[arg] > 0:
                CP += 1
            else:
                CP += 2
        elif ope == 'E':
            print(f'Registrador {arg}: {registers[arg]}')
            CP += 1
        elif ope == '.':
            traceback_list.append(command.trace)
            registers = run_module(arg, registers)
            traceback_list.pop()
            CP += 1

    return registers

debugging_mode = False
traceback_list = []
program_name = 'examples/somar.lmp'
execute(program_name)