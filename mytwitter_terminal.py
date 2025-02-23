from mytwitter_classes import  PessoaFisica, PessoaJuridica, RepositorioUsuarios, MyTwitter

repositorio = RepositorioUsuarios() #construtpr da RepositorioUsuarios
mytt = MyTwitter(repositorio) #construtor da classe Mytwitter

while True:
    formatacao_perfil = lambda usuario: "@" + usuario if not usuario.startswith("@") else usuario #função de formatação de usuário
    print('\n')
    menu = ('Digite "1" para acessar conta\n'
            'Ainda não possui conta? Digite "2" para cadastrar uma conta\n'
            'Digite "3" para sair de Mytwitter\n'
            'Após digitar, clique em "enter": ')
    opcao = input(menu)

    if opcao == "1":
        print('\n')
        usuario_nome = str(input('Digite seu nome de usuário para poder acessar a conta: ').lower())
        perfil_formatado = formatacao_perfil(usuario_nome)
        perfil_usuario = repositorio.buscar(perfil_formatado)

        if perfil_usuario is None:
            print('\n')
            print('Não encontramos seu usuário no nosso sistema. Tente novamente ou cadraste uma conta')
            
        else:
            nome_usuario = perfil_usuario.get_usuario()
            while True:
                print('\n')
                print('O que você deseja fazer hoje?')
                menu2 = (
                    '1 - Tweetar\n'
                    '2 - Ver sua timeline\n'
                    '3 - Ver seus tweets\n'
                    '4 - Seguir usuário\n'
                    '5 - Ver número de seguidores\n'
                    '6 - Ver seus seguidores\n'
                    '7 - Ver seus seguidos\n'
                    '8 - Mudar nome do perfil\n'
                    '9 - Cancelar perfil\n'
                    '10 - Sair do perfil\n'
                    'Digite sua opção: '
                )
                opcao2 = str(input(menu2))

                if opcao2 == "1":
                    '''Tweetar'''
                    print('\n')
                    mensagem = str(input('Digite a mensagem do tweet abaixo:\n'))
                    mytt.tweetar(usuario= nome_usuario, mensagem= mensagem)
                
                elif opcao2 == "2":
                    '''Timeline'''
                    print('\n')
                    timeline = mytt.timeline(usuario= nome_usuario)
                    for tweet in timeline:
                        print(str(tweet))  # Exibe cada tweet corretamente

                elif opcao2 == "3":
                    '''Tweets'''
                    print('\n')
                    tweets = mytt.tweets(usuario= nome_usuario)
                    for tweet in tweets:
                        print(str(tweet))
                
                elif opcao2 == "4":
                    '''Seguir'''
                    print('\n')
                    seguir_usuario = input('Digite o nome do usuário que deseja seguir: ')
                    mytt.seguir(seguidor= nome_usuario, seguido= seguir_usuario)
                
                elif opcao2 == "5":
                    '''Número de seguidores'''
                    print('\n')
                    num_seguidores = mytt.num_seguidores(usuario= nome_usuario)
                    print(int(num_seguidores))

                
                elif opcao2 == "6":
                    '''Seguidores'''
                    print('\n')
                    seguidores = mytt.seguidores(usuario= nome_usuario)
                    for seguidor in seguidores:
                        print(str(seguidor))  # Se a classe do seguidor tem __str__, funciona

                elif opcao2 == "7":
                    '''Seguidos'''
                    print('\n')
                    seguidos = mytt.seguidos(usuario= nome_usuario)
                    for seguido in seguidos:
                        print(str(seguido))  # Se a classe do seguido tem __str__, funciona
                
                elif opcao2 == "8":
                    '''Atualizar perfil'''
                    print('\n')
                    novo_nome = input('Digite o seu novo nome de usuário: ')
                    nome_formatado = formatacao_perfil(novo_nome)
                    perfil_usuario.set_usuario(novo_usuario= nome_formatado)
                    repositorio.atualizar(perfil= perfil_usuario)
                
                elif opcao2 == "9":
                    '''Cancelar perfil'''
                    print('\n')
                    mytt.cancelar_perfil(usuario= nome_usuario)
                
                elif opcao == "10":
                     break
                
                else:
                    print('\n')
                    print('Opção inválida. Tente novamente.')

                
    elif opcao == "2":
        print('\n')
        pessoas = (
            'Se sua conta for pessoal, digite "1"\n'
            'Se sua conta for empresarial, digite "2"\n' 
            'Digite aqui qual será seu tipo de conta: '
        )
        pessoa = input(pessoas)

        if pessoa == "1":
            cadastramento = False 
            while cadastramento != True:
                
                perfil_inicial = str(input('Digite seu nome de usuario: ').lower())
                perfil_formatado = formatacao_perfil(perfil_inicial)

                cpf = input('Digite aqui o seu CPF: ')
                cpf_formatado = ''.join(filter(str.isdigit, cpf))

                if len(cpf_formatado) == 11:
                    perfil_usuario = PessoaFisica(nome_usuario= perfil_formatado, cpf= cpf_formatado) 
                    mytt.criar_perfil(perfil= perfil_usuario)
                    cadastramento = True
                    
                elif len(cpf_formatado) != 11:
                    print('CPF inválido')


        elif pessoa == "2":
            cadastramento = False 
            while cadastramento != True:
                
                perfil_inicial = str(input('Digite seu nome de usuario: ').lower())
                perfil_formatado = formatacao_perfil(perfil_inicial)

                cnpj = input('Digite aqui o seu CNPJ: ')
                cnpj_formatado = ''.join(filter(str.isdigit, cnpj))

                if len(cnpj_formatado) == 14:
                    perfil_usuario = PessoaJuridica(nome_usuario= perfil_formatado, cnpj= cnpj_formatado) 
                    mytt.criar_perfil(perfil= perfil_usuario)
                    cadastramento = True
                    
                elif len(cnpj_formatado) != 14:
                    print('CPF inválido')

        else:
            print('\n')
            print('Opção inválida. Tente novamente.')
    

    elif opcao == "3":
        break

    else:
        print('\n')
        print('Opção inválida. Tente novamente.')