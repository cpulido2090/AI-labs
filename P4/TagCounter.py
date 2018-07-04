import random
class TagCounter():

    def readFile(diccionario , file_read):

        #Abrimos el fichero y lo leemos
    	fr=open(file_read,'r')

    	for line in fr:
            #Definimos un diccionario donde guardaremos el word,tag y num. de ocurrencias
            appearences=dict()
            #Para cada linia que leemos decodificamos la linia
            line = line.decode('latin_1').encode('utf-8').lower().split()

            #Si la palabra aun no se encuentra en el diccionario, la anadimos
            if not diccionario.has_key(line[0]):
                appearences[line[1]]= 1
                diccionario[line[0]]=appearences

            else:
                #Si la palabra ya se encuentra en el diccionario
                appearences = diccionario.get(line[0])

                #Si dicha palabra, ya se encuentra en el diccionario con el mismo tag, incrementamos en 1 el numero de ocurrencias
                if appearences.has_key(line[1]):
                    appearences[line[1]]=appearences.get(line[1])+1
                    diccionario[line[0]]=appearences

                #Si la palabra con el tag actual no aparece en el dccionario la anadimos
                else:
                    appearences[line[1]]=1
                    diccionario[line[0]]=appearences

        #Finalmente, cerramos el fichero y devolvemos el diccionario
        fr.close()
        return diccionario

    def writeFile(diccionario, file_write):
        #Abrimos el fichero a escribir
    	fw= open(file_write,'w')

        #Recorremos el diccionario y el diccionario que contiene el diccionario
        #y escribimos palabra, tag y numero de occurrencias. Finalmente, cerramos el fichero.
    	for word,appearences in diccionario.iteritems():
            for tag, value in appearences.iteritems():
                fw.write(word + '\t' + tag + '\t' + str(value) + '\n')
        fw.close()
    
    def TagPriority(diccionario):
        #Creamos un diccionario donde guardaremos la palabra y el tag con mayor ocurrencia
        tagDic = dict()

        #Recorremos el diccionario y para cada palabra anadimos a valor el tag con mayor ocurrencia
        for word, appearences in diccionario.iteritems():
            valor = None
            maxValue=None

            for tag,tagApp in appearences.iteritems():
                if maxValue < tagApp or maxValue is None:
                    valor = tag
                    maxValue = tagApp

            tagDic[word]= valor

        return tagDic

    def taggingModel(diccionario, test, numTest):

        #Abrimos el fichero de test para leerlo y el fichero result_X, donde X es el numero de test
        fr = open(test,'r')
        fw = open('result_'+str(numTest)+'.txt','w')     

        #Recorremos el fichero de test y lo decodificamos
        for line in fr:
            line = line.decode('latin_1').encode('utf-8').lower().split()
            
            #Recorremos las palabras, si la plabra no tiene tag asignado, le asignamos el tag con mayor ocurrencia.
            #Sino, si la palabra tiene un tag asignado, escribmos la palabra y el tag.
            for word in line:
                if not diccionario.has_key(word):
                    fw.write(word.strip() + '\t' + max(diccionario)[1] + '\n')
                else:
                    fw.write(word.strip() + '\t' + diccionario[word] + '\n')

        #Finalmente, cerramos ambos ficheros
        fr.close()
        fw.close()

    def resultEvaluation(file_result,gold_file):
        #Abrimos los ficheros result y gold y los leemos y decodificamos unicamente el gold, ya que el result lo hemos generado anteriormente 
        fr_result = open(file_result,'r')
        fr_gold = open(gold_file, 'r')

        appearences = 0.0
        checks =0.0

        result = fr_result.readline()
        gold = fr_gold.readline()

        while not gold is '' and not result is '':

            gold = gold.decode('latin_1').encode('utf-8').lower().split()
            result= result.split()

            #Si la palabra y tag de result es igual a la de gold,  sumamos uno a checks
            if result == gold:
                checks+=1.0


            appearences+=1.0

            result = fr_result.readline()
            gold = fr_gold.readline()

        return (checks/appearences)*100

    #Apartado 1
    diccionario = dict()
    diccionario = readFile(diccionario, 'corpus.txt')
    writeFile(diccionario,'lexic.txt')

    #Apartado 2
    diccionarioTag = TagPriority(diccionario)
    
    taggingModel(diccionarioTag,'test_1.txt',1)
    taggingModel(diccionarioTag,'test_2.txt',2)

    #Apartado 3
    accuracy1 = resultEvaluation('result_1.txt', 'gold_standard_1.txt')
    accuracy2 = resultEvaluation('result_2.txt', 'gold_standard_2.txt')

    print 'Accuracy 1: ' + str(accuracy1)[0:5] + '%' + '\nAccuracy 2: '+ str(accuracy2)[0:5] + '%'