import os

class Line:
    def __init__(self, program_name, line_number, line):
        self.program_name = program_name
        self.line_number = line_number
        self.line = line

    def __str__(self):
        return f'{self.program_name}: {self.line_number} --> {self.line}'

class Command:
    def __init__(self, item):
        line = item.line
        tokens = line.split(' ')
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
        
        self.operation = tokens[0]
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

        if len(tokens) == 3:
            self.label = tokens[2]
        else:
            self.label = None

    def __str__(self):
        if self.label is None:
            return f'{self.operation} {self.argument}'
        else:
            return f'{self.operation} {self.argument} {self.label}'

def register_value(item, registers):
    line = item.line
    tokens = line.split(' ')
    if len(tokens) != 3:
        messages = [
                'Erro na definição de registradores.',
                'Número incorreto de tokes. Deveriam ser 3 tokens.']
        error_msg(item, messages)

    try:
        reg_id= int(tokens[1])
    except ValueError:
        messages = [
            'Erro na definição de registradores.',
            'Identificação de um registrador deve ser inteiro.']
        error_msg(item, messages)

    try:
        reg_val = int(tokens[2])
    except ValueError:
        messages = [
            'Erro na definição de registradores.',
            'Valor inicializado em um registrador deve ser inteiro.']
        error_msg(item, messages)

    if reg_id!= len(registers):
        messages = [
            'Erro na definição de registradores.',
            'Ordem incorreta dos identificadores.']
        error_msg(item, messages)

    return reg_val

def analise_module_calling(item, registers):
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

def error_msg(item, messages):
    line = item.line
    line_number = item.line_number
    program_name = item.program_name
    loc = f'{program_name}: {line_number}'
    print(50*'-')
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
            analise_module_calling(item, registers)
            commands.append(Command(item))

        if len(tokens[0]) == 1 and tokens[0] in '+-PCEF':
            commands.append(Command(item))

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
            registers = run_module(arg, registers)
            CP += 1

    return registers

debugging_mode = False
program_name = 'examples/importando_modulo.lmp'
execute(program_name)