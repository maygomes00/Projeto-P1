###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Johnny Mayron Santana Ferreira
#           Mayara Gomes de Oliveira Pina
#
# Email:    jmsf2@cin.ufpe.br
#           mgop@cin.ufpe.br
#
# Data:     2016-06-19
#
# Descricao:  Este é um modelo de arquivo para ser utilizado para a implementacao
#             do projeto pratico da disciplina de Programacao 1. 
#             A descricao do projeto encontra-se no site da disciplina e trata-se
#             de uma adaptacao do projeto disponivel em 
#             http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#             O objetivo deste projeto é implementar um sistema de analise de
#             sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#          Copyright(c) 2016 Johnny Mayron Santana Ferreira, Mayara Gomes de Oliveira Pina
#
###############################################################################

import sys
import re
sw=open('sw.txt','r')
ler_sw=sw.readlines()
sw.close()
stopwords=[x[:len(x)-1] for x in ler_sw]    

def clean_up(s):    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result

def split_on_separators(original, separators):           
    return list(filter(lambda x: x != '',re.split('[{0}]'.format(separators),original)))
                  
def readTrainingSet(fname):
    words = {}
    ler=open(fname,'r')
    linhas=ler.readlines()
    ler.close()
    listaS=[]
    listaC=[]
    cont=0
    for x in linhas:
        listaS.append(split_on_separators(x,' '))
    for x in listaS:
        listaC.append([])
        for y in x:
            listaC[cont].append(clean_up(y))
            if clean_up(y)=='' or clean_up(y) in stopwords:
                listaC[cont].remove(clean_up(y))
        cont+=1
    for x in listaC:
        for y in x[1:]:
            if y not in words:
                words[y]=[y,len([z for z in x if z==y]),int(x[0])]
            else:
                words[y]=[y,words[y][1]+len([z for z in x if z==y]),(words[y][2]+int(x[0]))/2]
    return words

def readTestSet(fname):
    reviews=[]
    ler=open(fname,'r')
    linhas=ler.readlines()
    ler.close()
    listaS=[]
    listaC=[]
    cont=0	
    for x in linhas:
        listaS.append(split_on_separators(x,' '))
    for x in listaS:
        listaC.append([])
        for y in x:
            listaC[cont].append(clean_up(y))
            if clean_up(y)=='' or clean_up(y) in stopwords:
                listaC[cont].remove(clean_up(y))
        cont+=1
    reviews=[tuple(x) for x in listaC]
    return reviews

def computeSentiment(reviews,words):
    score = 0.0
    count = 0
    for x in reviews:
        if len(reviews)==1:
           
            score+=int(reviews[0])
            count+=1
        else:
            for y in reviews[1:]:
               
                count+=1
                if y in words:
                    score+=words[y][2]
                else:
                    score+=2
    return round(score/count,5)

def computeSumSquaredErrors(reviews,words):
    count = 0
    sse=0
    for x in reviews:
                sse+=(computeSentiment(reviews[count],words)-(int(x[0])))**2
                count+=1
    sse/=count            
    return sse

def main():    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)


    words = readTrainingSet(sys.argv[1])
    
    
    reviews = readTestSet(sys.argv[2])
    
    
    sse = computeSumSquaredErrors(reviews,words)
    
    print ('A soma do quadrado dos erros é: {0}'.format(round(sse,2)))
            

if __name__ == '__main__':
    main()
    
    
    

