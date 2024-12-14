from tablero import Tablero, Pieza, Color  

class MinMax:
    def __init__(self, color, profundidad=3):
        self.color = color  # Color que juega la IA
        self.profundidad = profundidad
        
    def evaluar_tablero(self, tablero):
        """
        Función heurística para evaluar el estado del tablero
        Retorna un valor positivo si es favorable para la IA, negativo si es favorable para el oponente
        """
        valor = 0
        valores_piezas = {
            Pieza.PEON: 100,
            Pieza.CABALLO: 320,
            Pieza.ALFIL: 330,
            Pieza.TORRE: 500,
            Pieza.DAMA: 900,
            Pieza.REY: 20000
        }
        
        # Evaluar material en ambos tableros
        for tablero_num in [1, 2]:
            for fila in range(8):
                for columna in range(8):
                    pieza = tablero.obtener_pieza(tablero_num, fila, columna)
                    if pieza:
                        valor_base = valores_piezas[pieza[0]]
                        # Sumar para piezas de la IA, restar para piezas del oponente
                        multiplicador = 1 if pieza[1] == self.color else -1
                        valor += valor_base * multiplicador
                        
                        # Bonificaciones posicionales
                        if pieza[0] == Pieza.PEON:
                            # Peones más avanzados son mejores
                            avance = 7 - fila if self.color == Color.BLANCO else fila
                            valor += avance * 10 * multiplicador
                        elif pieza[0] in [Pieza.CABALLO, Pieza.ALFIL]:
                            # Piezas menores en el centro son mejores
                            centro_fila = 3.5 - abs(3.5 - fila)
                            centro_col = 3.5 - abs(3.5 - columna)
                            valor += (centro_fila + centro_col) * 10 * multiplicador
        
        return valor

    def minimax(self, tablero, profundidad, alfa, beta, es_maximizador):
        """
        Implementación del algoritmo Minimax con poda alfa-beta
        """
        if profundidad == 0:
            return self.evaluar_tablero(tablero)
            
        if es_maximizador:
            mejor_valor = float('-inf')
            for movimiento in self.obtener_todos_movimientos(tablero, self.color):
                tablero_temp = tablero.copiar_tablero()
                tablero_temp.realizar_movimiento(movimiento)
                valor = self.minimax(tablero_temp, profundidad - 1, alfa, beta, False)
                mejor_valor = max(mejor_valor, valor)
                alfa = max(alfa, mejor_valor)
                if beta <= alfa:
                    break
            return mejor_valor
        else:
            mejor_valor = float('inf')
            color_oponente = Color.NEGRO if self.color == Color.BLANCO else Color.BLANCO
            for movimiento in self.obtener_todos_movimientos(tablero, color_oponente):
                tablero_temp = tablero.copiar_tablero()
                tablero_temp.realizar_movimiento(movimiento)
                valor = self.minimax(tablero_temp, profundidad - 1, alfa, beta, True)
                mejor_valor = min(mejor_valor, valor)
                beta = min(beta, mejor_valor)
                if beta <= alfa:
                    break
            return mejor_valor

    def obtener_mejor_movimiento(self, tablero):
        """
        Encuentra el mejor movimiento usando Minimax con poda alfa-beta
        """
        mejor_movimiento = None
        mejor_valor = float('-inf')
        alfa = float('-inf')
        beta = float('inf')
        
        for movimiento in self.obtener_todos_movimientos(tablero, self.color):
            tablero_temp = tablero.copiar_tablero()
            tablero_temp.realizar_movimiento(movimiento)
            valor = self.minimax(tablero_temp, self.profundidad - 1, alfa, beta, False)
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
                
        return mejor_movimiento

    def obtener_todos_movimientos(self, tablero, color):
        """
        Obtiene todos los movimientos posibles para un color dado
        """
        movimientos = []
        for tablero_num in [1, 2]:
            for fila in range(8):
                for columna in range(8):
                    pieza = tablero.obtener_pieza(tablero_num, fila, columna)
                    if pieza and pieza[1] == color:
                        movs = tablero.movimientos_pieza(pieza[0], (fila, columna), tablero_num)
                        for mov in movs:
                            movimientos.append((tablero_num, (fila, columna), mov))
        return movimientos

