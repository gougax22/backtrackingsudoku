import numpy as np   #importa a biblioteca para manipular matrizes atraves da abreviacao np
import random       #usado para aleatoriedade dos numeros

def gerar_numeros_unicos():  #funcao para criar pares unicos x,y entre 1 a 9 porem nao iguais que serao usados para preencher as diagoinais dos subquadrantes
    numeros = [(x, y) for x in range(1, 10) for y in range(1, 10) if x != y] #faz x e y percorrerem valores de 1 a 9 onde antes de adicionar o par x,y na lista ,o programa verefica se sao diferentes e se nao forem n serao incluidos na lista
    random.shuffle(numeros)    #embaralha os pares na lista, garantindo que sua ordem seja aleatória.
    return numeros



def criar_diagonais(tabuleiro, pares):#funcao para preenche as diagonais principais de cada subquadrante 3x3 com palíndromos formados pelos pares x,y
    usados = set()   #armazena elementos unicos sem repeticao
    for bloco_i in range(3):
        for bloco_j in range(3):  #percorrer o subquadrante
            for par in pares:   #para cada par em pares passado como parametro
                if par not in usados:  # verifica se o par nao nao esta em usados
                    i, j = bloco_i * 3, bloco_j * 3  # calcula os índices iniciais do bloco no tabuleiro.
                    tabuleiro[i][j], tabuleiro[i + 1][j + 1], tabuleiro[i + 2][j + 2] = par[0], par[1], par[0]  #preenche a diagonal com x,y,x
                    usados.add(par)   #Marca o par como usado.
                    break    #sai do loop pro proximo bloco
            else:  # se nenhuma par adequado foi encontrado 
                return False   # retorna false indicando falha ao preencher as diagonais
    return True   # se todas as diagonais foram preenchidas sem falhas retorna true




def preencher_bloco(tabuleiro, bloco_i, bloco_j):  #função para preencher o restante de um bloco 3x3.
    numeros = list(range(1, 10))  # cria uma lista com numeros de 1 a 9
    random.shuffle(numeros)  #embaralha os numeros para preenchimento aleatorio a cada execucao 
    inicio_linha, inicio_coluna = bloco_i * 3, bloco_j * 3 #calcula os índices iniciais do bloco 3x3 no tabuleiro.
    bloco = tabuleiro[inicio_linha:inicio_linha + 3, inicio_coluna:inicio_coluna + 3] #extrai o subquadrante específico do tabuleiro, com 3 linhas e 3 colunas, para trabalhar com ele,ex=para 0 em ambas[0 a 3,0 a 3] sem contar o 3
    
    for linha in range(3):
        for coluna in range(3):    #percorre todas as celulas do subquadrante
            if bloco[linha, coluna] == 0:  #verifica se a celula atual esta vazia
                for numero in numeros:   #tenta preencher a celula vazia com a lista de numeros embaralhados
                    if numero not in bloco.flatten(): # verifica se o numero ja existe no subquadrante,a funcao flatten'planifica' o subquadrante 3x3 para simplificar a verificação
                        bloco[linha, coluna] = numero  #insere o numero na celula atual
                        if preencher_bloco(tabuleiro, bloco_i, bloco_j):  #recursivamente chama a função para preencher o restante do subquadrante
                            return True
                        bloco[linha, coluna] = 0  #  se o numero atual nao leva a nenhuma solucao ,ela  desfaz a escolha deixando a celula vazia novamente 
                return False  #se nenhum número da lista pode ser colocado na célula atual sem violar as restrições, retorna false
    return True  #se todas as células do subquadrante foram preenchidas corretamente, retorna true



def preencher_restantes(tabuleiro): # preenche o tabuleiro atraves dos blocos 3x3
    for bloco_i in range(3):
        for bloco_j in range(3):  #percorre todos os blocos do tabuleiros
            if not preencher_bloco(tabuleiro, bloco_i, bloco_j):  #verifica se o metodo obteve sucesso,se nao obteve retorna false(falha)
                return False
    return True #caso n tenha dado false,Se todos os blocos foram preenchidos com sucesso retorna true(tabuleiro preenchido com sucesso)



def gerar_sudoku(): #cria um tabuleiro completo de Sudoku, seguindo todas as regras de preenchimento
    tabuleiro = np.zeros((9, 9), dtype=int)  # cria o tabuleiro preenchido com zeros
    pares = gerar_numeros_unicos()  #atribui os valores dos pares desse metodos a variavel apres
    if criar_diagonais(tabuleiro, pares) and preencher_restantes(tabuleiro): #preenche as diagonais e os restantante do tabuleiro
        return tabuleiro  #se der certo,retorna ao  tabuleiro sudoku preenchido
    return None #caso contrario,o tabuleiro n pode ser gerado



def exibir_tabuleiro(tabuleiro):        #imprimi o tabuleiro do Sudoku no terminal 
    if tabuleiro is None:  #se o tabuleiro for none n pode ser gerado
        print("Falha ao gerar o tabuleiro.")
        return
    
    for i in range(9):  # percorrendo os indices da linha(i)
        if i % 3 == 0 and i != 0:  # adiciona uma linha divisoria entre os subquaadrantes 3x3
            print("--" * 12)  # Linha divisória horizontal
        linha = ""  # string vazia q ira ser preenchida com linhas do tabuleiro
        for j in range(9):  # percorre indices da coluna(j)
            if j % 3 == 0 and j != 0: # adiciona divisoria vertical entre os subquadrantes 3x3
                linha += " | "  # Linha divisória vertical
            valor = tabuleiro[i][j]  #obtem o valor da celula na posição (i, j) do tabuleiro  
            if valor == 0:      # verifica se o valor eh zero (célula vazia)
                simbolo = '.'  # Substitui por ponto
            else:
                simbolo = valor  # Mantém o número original
            linha += f"{simbolo} " # Adiciona o símbolo (ou valor) à linha formatada com um espaço
        print(linha)



def gerar_varios_tabuleiros(quantidade):   # cria varios tabuleiros do sudoku que segrem as regras estabelecidas 
    tabuleiros = [] #Inicializa uma lista para guardar os tabuleiros gerados 
    for _ in range(quantidade):  #um loop percorre ate gerar a quantidade especificada de tabuleiros.
        novo_tabuleiro = None  #armazena o resultado de cada tentativa de gerar um tabuleiro
        tentativas = 0   #contador para evitar loops infinitos caso nao seja possivel  gerar tabuleiros validos
        while novo_tabuleiro is None and tentativas < 500: # ate que um tabuleiro nao seja gerado ou tentativas cheguem a 500,evita loop infinito
            novo_tabuleiro = gerar_sudoku()  # criar tabuleiro
            if novo_tabuleiro is not None and any(np.array_equal(novo_tabuleiro, t) for t in tabuleiros): # Se novo_tabuleiro nao for None e ja existir um tabuleiro igual a novo_tabuleiro dentro de tabuleiros, então
                novo_tabuleiro = None # se esse novo tabuleiro for none ou ja existir ele vai acabar sendo none
            tentativas += 1  # incrmenta numero de tentativas
        if novo_tabuleiro is not None:      # se novo tabuleiro nao for none
            tabuleiros.append(novo_tabuleiro)  # novo tabuleiro sera adicionado em tabuleiros 
    return tabuleiros  # retorna tabuleiros

print("Gerando tabuleiros de Sudoku com palíndromos...\n")
tabuleiros = gerar_varios_tabuleiros(2)  # gerar 2 tabuleiros 
for i, tabuleiro in enumerate(tabuleiros, 1):  #i representa o numero de tabuleiros comecando de 1,enumerate retorna o valor e indice do elemento 
    print(f"\nTabuleiro {i}:") # exibe o tabuleiro q esta sendo mostrado 
    exibir_tabuleiro(tabuleiro)  # imprime o tabuleiro formatado

