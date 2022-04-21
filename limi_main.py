def generate_program(program_name):
    program = []
    program = load_program(program_name, program)
    return program

def load_program(program_name, program):
    with open(program_name, 'r') as program_content:
        for line in program_content.readlines():
            cleaned_line = line.strip().strip('\n')
            if cleaned_line:
                program.append(cleaned_line)

    return program

def program_scanning(program):
    """Analisar o conteúdo de program e criar registers e commands"""
    registers = [0, ]
    commands  = []

    for line in program:
        tokens = line.split(' ')
        if tokens[0] == 'R':
            if len(tokens) == 3:
                try:
                    X = int(tokens[1])
                    V = int(tokens[2])
                    if X == len(registers):
                        registers.append(V)
                    else:
                        print('Erro: Ordem incorreta da definição dos registradores.')

                except ValueError:
                    print('Erro: Impossível converter str em int.')
            else:
                print('Erro: Problema na definição de registradores.')

    return registers, commands

def run_program(registers, commands):

    return registers

program_name = 'examples/somar.lmp'
program = generate_program(program_name)
registers, commands = program_scanning(program)
registers = run_program(registers, commands)
print(registers)
