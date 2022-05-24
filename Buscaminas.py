import random
class Game:
    def __init__(self):
        self.tablero=[]
        self.crear_tablero()
        self.gameplay()

    def limpiar_pantalla(self):
        """IMPRIME 50 SALTOS DE LINEA """
        print("\n" * 50)
    def crear_bombas(self):
        """AGREGA EN LA MATRIZ 9 BOMBAS SIN REVELAR"""
        for elem in range(0,9):
            bombAdded=False
            while not bombAdded:
                x=random.randint(0,7)
                y=random.randint(0,7)
                if self.tablero[y][x]=="E":
                    self.tablero[y][x] ="M"
                    bombAdded=True
        self.imprimir_tablero()



    def crear_tablero(self):
        """DEVUELVE UNA LISTA DE 8 LISTAS DE 8 EMPTY SQUARES [ [E, E, E, E,...,E] , [E, E, E, E,...,E]]"""
        matriz = [["E"] * 8 for i in range(8)]
        self.tablero= matriz
        self.crear_bombas()

    def imprimir_tablero(self):
        #M : Mina sin revelar
        #E : Cuadrado sin revelar
        #B: Cuadrado revelado sin minas adyacentes
        #X: Mina revelada
        #1,8: cantidad de minas adyacentes del cuadrado revelado

        filas=len(self.tablero)
        columnas=len(self.tablero[0])
        abc=["A","B","C","D","E","F","G","H"]
        print(" ",end=" ") #Identar el tablero
        for elem in abc:
            print("%2s" % elem, end="  ")
        print("")

        for f in range(filas):
            print(f+1,end="")
            for c in range (columnas):
                if self.tablero[f][c]=="M" or self.tablero[f][c]=="E":
                    print( "%3s" % "?", end=" ", sep="")
                elif self.tablero[f][c]=="B":
                    print("%3s" % " ", end=" ", sep="")
                elif self.tablero[f][c]=="X":
                    print("\033[91m","%3s" % "#","\033[0m", end=" ", sep="")
                else:
                    print("\033[94m","%3s" % self.tablero[f][c],"\033[0m", end=" ", sep="")


            print() #Salto de linea

    def que_hay_en_xy(self,x,y):
        """DADO UN X, Y y un Valor: Retorna el valor de la matriz en esa posicion"""
        return(self.tablero[y][x])

    def modificar_xy(self,x,y,valor):
        """DADO UN X, Y y un Valor: Coloca el valor en esa posicion"""
        self.tablero[y][x]=valor

    def leer_coordenada(self,coordenada):
        coordenada=coordenada.upper()
        if coordenada=="Z":
            return 9,9
        else:
            abc = ["A", "B", "C", "D", "E", "F", "G", "H"]
            numbers=[1,2,3,4,5,6,7,8]
            if coordenada[0].upper() in abc and int(coordenada[1]) in numbers:
                numX = abc.index(coordenada[0])
                return numX,int(coordenada[1])-1
            else:
                return -1,-1
    def calcular_mina_en_xy(self,x,y):
        """DADO UN X, Y. VERIFICA SI EXISTE ESA POSICION EN EL TABLERO, Y LUEGO VERIFICA SI HAY UNA MINA AHI. SI HAY UNA MINA RETORNA 1 SI NO 0"""
        if ((x>=0 and x<=7) and (y>=0 and y<=7)):
            if self.que_hay_en_xy(x,y)=="M":
                return 1
            else:
                return 0
        else:
            return 0


    def calcular_minas_cercanas(self,x,y):
        contador=0
        contador+=self.calcular_mina_en_xy(x+1,y)
        contador += self.calcular_mina_en_xy(x - 1, y)
        contador += self.calcular_mina_en_xy(x, y+1)
        contador += self.calcular_mina_en_xy(x, y-1)
        contador += self.calcular_mina_en_xy(x+1, y - 1)
        contador += self.calcular_mina_en_xy(x+1, y + 1)
        contador += self.calcular_mina_en_xy(x - 1, y - 1)
        contador += self.calcular_mina_en_xy(x - 1, y + 1)
        return contador

    def revelar_cuadrado_vacio(self,x,y):
        if ((x >= 0 and x <= 7) and (y >= 0 and y <= 7)):
            if self.que_hay_en_xy(x, y) == "E":
                if self.calcular_minas_cercanas(x,y)==0:
                    self.modificar_xy(x, y, "B")
                    self.revelar_cuadrado_vacio(x+1,y)
                    self.revelar_cuadrado_vacio( x - 1, y)
                    self.revelar_cuadrado_vacio(x, y+1)
                    self.revelar_cuadrado_vacio(x, y-1)
                    self.revelar_cuadrado_vacio(x+1, y - 1)
                    self.revelar_cuadrado_vacio( x+1, y + 1)
                    self.revelar_cuadrado_vacio(x - 1, y - 1)
                    self.revelar_cuadrado_vacio(x - 1, y + 1)
                else:
                    self.modificar_xy(x, y, self.calcular_minas_cercanas(x,y))





    def gameplay(self):
        x,y=self.leer_coordenada(input("Ingrese una coordenada con formato A1, Para salir del juego ingrese Z: "))
        while x!=9: #9: finalizar juego
            if x!=-1:
                if self.que_hay_en_xy(x,y)=="M":  #M : Mina sin revelar
                    self.modificar_xy(x, y, "X")
                    self.limpiar_pantalla()
                    self.imprimir_tablero()
                    print("Game Over")
                    x=9
                elif self.que_hay_en_xy(x,y)=="E": #E : Cuadrado sin revelar
                    minasCercanas=self.calcular_minas_cercanas(x,y)
                    #if minasCercanas==0:
                    self.revelar_cuadrado_vacio(x, y)
                        #self.modificar_xy(x,y,"B")
                    #else:
                       # self.modificar_xy(x,y,minasCercanas)
                elif self.que_hay_en_xy(x,y)=="B" or (self.que_hay_en_xy(x,y)>=1 and self.que_hay_en_xy(x,y)<=8): #B: Cuadrado revelado sin minas adyacentes
                    print("La celda ya se encontraba reveleada")
                else:
                    print("Error")

                if x!=9:

                    self.limpiar_pantalla()
                    self.imprimir_tablero()
                    x, y = self.leer_coordenada(
                        input("Ingrese una coordenada con formato A1, Para salir del juego ingrese Z: "))
            else:
                print("Error: Coordenada no existente")
                x, y = self.leer_coordenada(
                    input("Ingrese una coordenada con formato A1, Para salir del juego ingrese Z: "))

        print("Juego finalizado")










game=Game()



