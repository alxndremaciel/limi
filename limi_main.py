class Line:
    __init__(self, program_name, line_number, line):
        self.program_name = program_name 
        self.line_number = line_number 
        self.line = line 

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

def run_debug_mode(registers, commands, CP):
    print(f'Depurando::: Registradores: {registers} --- Comando: {commands[CP]}')

def error_msg(metadata, messages):
    line = metadata['line']
    line_number = metadata['line_number']
    program_name = metadata['program_name']
    loc = f'{program_name}: {line_number}'
    print(50*'-')
    print(f'<<< ERRO - {loc} >>> {line}')
    for message in messages:
        print(f'<<< ERRO - {loc} >>> {message}')
    print(50*'-')
    raise SystemExit(0)

def generate_program(program_name):
    program = []
    program = load_program(program_name, program)
    return program

def load_program(program_name, program):
    with open(program_name, 'r') as program_content:
        for ln, line in enumerate(program_content.readlines()):
            cleaned_line = line.strip().strip('\n')
            if cleaned_line:
                program.append(Line(program_name, ln + 1, cleaned_line))

    return program

def program_scanning(program):
    """Analisar o conteúdo de program e criar registers e commands"""
    registers = [0, ]
    commands  = []

    for item in program:
        line = item.line
        tokens = line.split(' ')
        if tokens[0] == 'R':
            registers.append(register_value(item, registers))

        if len(tokens[0]) == 1 and tokens[0] in '+-PCEF':
            cmd = None
            if len(tokens) == 1:
                messages = [
                        'Erro na definição de comandos.',
                        'Número incorreto de tokes. Tem menos de 2 tokens.']
                error_msg(item, messages)
            elif len(tokens) == 2:
                cmd = {'ope': tokens[0], 'arg': tokens[1], 'lab': None}
            elif len(tokens) == 3:
                cmd = {'ope': tokens[0], 'arg': tokens[1], 'lab': tokens[2]}
            else:
                messages = [
                        'Erro na definição de comandos.',
                        'Número incorreto de tokes. Tem mais de 3 tokens.']
                error_msg(item, messages)

            if cmd is not None:
                commands.append(cmd)

    return registers, commands

def run_program(registers, commands):
    CP = 0
    while True:
        if debugging_mode:
            run_debug_mode(registers, commands, CP)

        command = commands[CP]
        ope = command['ope']
        arg = command['arg']
        lab = command['lab']
        if ope == 'F':
            break
        elif ope =='+':
            registers[int(arg)] += 1
            CP += 1
        elif ope =='-':
            registers[int(arg)] -= 1
            CP += 1
        elif ope =='P':
            for line, cmd in enumerate(commands):
                if cmd['lab'] == arg:
                    CP = line
                    break
        elif ope == 'C':
            if registers[int(arg)] > 0:
                CP += 1
            else:
                CP += 2
        elif ope == 'E':
            print(f'Registrador {arg}: {registers[int(arg)]}')
            CP += 1

    return registers

debugging_mode = False
program_name = 'examples/somar.lmp'
program = generate_program(program_name)
registers, commands = program_scanning(program)
registers = run_program(registers, commands)