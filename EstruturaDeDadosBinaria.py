from datetime import datetime
from typing import Optional, List, Tuple

class NoReserva:
    def __init__(self, data: str, numero_quarto: int):
        self.data = datetime.strptime(data, "%d-%m-%Y").date()
        self.numero_quarto = numero_quarto
        self.esquerda = None
        self.direita = None

    def __repr__(self):
        data_formatada = self.data.strftime("%d-%m-%Y")
        return f"Reserva quarto {self.numero_quarto}, data {data_formatada}"


class SistemaReservas:
    def __init__(self):
        self.raiz = None

    def inserir(self, data: str, numero_quarto: int) -> bool:
        if self.raiz is None:
            self.raiz = NoReserva(data, numero_quarto)
            return True
        else:
            return self._inserir(self.raiz, data, numero_quarto)

    def _inserir(self, no_atual: NoReserva, data: str, numero_quarto: int) -> bool:
        novo_no = NoReserva(data, numero_quarto)
        if no_atual.data == novo_no.data and no_atual.numero_quarto == novo_no.numero_quarto:
            return False  
        elif (novo_no.data, novo_no.numero_quarto) < (no_atual.data, no_atual.numero_quarto):
            if no_atual.esquerda is None:
                no_atual.esquerda = novo_no
                return True
            else:
                return self._inserir(no_atual.esquerda, data, numero_quarto)
        else:
            if no_atual.direita is None:
                no_atual.direita = novo_no
                return True
            else:
                return self._inserir(no_atual.direita, data, numero_quarto)

    def verificar_disponibilidade(self, data: str, numero_quarto: int) -> bool:
        data_para_verificar = datetime.strptime(data, "%d-%m-%Y").date()
        return self._verificar_disponibilidade(self.raiz, data_para_verificar, numero_quarto)

    def _verificar_disponibilidade(self, no_atual: Optional[NoReserva], data: datetime, numero_quarto: int) -> bool:
        if no_atual is None:
            return True
        if no_atual.data == data and no_atual.numero_quarto == numero_quarto:
            return False
        elif (data, numero_quarto) < (no_atual.data, no_atual.numero_quarto):
            return self._verificar_disponibilidade(no_atual.esquerda, data, numero_quarto)
        else:
            return self._verificar_disponibilidade(no_atual.direita, data, numero_quarto)

    def cancelar_reserva(self, data: str, numero_quarto: int) -> bool:
        self.raiz, deletado = self._cancelar_reserva(self.raiz, datetime.strptime(data, "%d-%m-%Y").date(), numero_quarto)
        return deletado

    def _cancelar_reserva(self, no_atual: Optional[NoReserva], data: datetime, numero_quarto: int) -> Tuple[Optional[NoReserva], bool]:
        if no_atual is None:
            return None, False
        if no_atual.data == data and no_atual.numero_quarto == numero_quarto:
            if no_atual.esquerda is None:
                return no_atual.direita, True
            if no_atual.direita is None:
                return no_atual.esquerda, True
            no_menor_maior = self._encontrar_minimo(no_atual.direita)
            no_atual.data, no_atual.numero_quarto = no_menor_maior.data, no_menor_maior.numero_quarto
            no_atual.direita, _ = self._cancelar_reserva(no_atual.direita, no_menor_maior.data, no_menor_maior.numero_quarto)
            return no_atual, True
        elif (data, numero_quarto) < (no_atual.data, no_atual.numero_quarto):
            no_atual.esquerda, deletado = self._cancelar_reserva(no_atual.esquerda, data, numero_quarto)
            return no_atual, deletado
        else: 
            no_atual.direita, deletado = self._cancelar_reserva(no_atual.direita, data, numero_quarto)
            return no_atual, deletado

    def _encontrar_minimo(self, no_atual: NoReserva) -> NoReserva:
        while no_atual.esquerda is not None:
            no_atual = no_atual.esquerda
        return no_atual

    def listar_reservas(self, numero_quarto: int) -> List[NoReserva]:
        reservas = []
        self._listar_reservas(self.raiz, numero_quarto, reservas)
        return reservas

    def _listar_reservas(self, no_atual: Optional[NoReserva], numero_quarto: int, reservas: List[NoReserva]):
        if no_atual is not None:
            if no_atual.numero_quarto == numero_quarto:
                reservas.append(no_atual)
            self._listar_reservas(no_atual.esquerda, numero_quarto, reservas)
            self._listar_reservas(no_atual.direita, numero_quarto, reservas)
            reservas.sort(key=lambda x: x.data)


# Demonstração de uso
sistema_reservas = SistemaReservas()

# inserindo algumas reservas
sistema_reservas.inserir("20-12-2023", 101)
sistema_reservas.inserir("23-12-2023", 301)
sistema_reservas.inserir("30-12-2023", 102)

# Verificando disponibilidade
print(sistema_reservas.verificar_disponibilidade("20-12-2023", 101))  # retorna False já que a reserva existe
print(sistema_reservas.verificar_disponibilidade("11-11-2023", 103))  # retorna True, pois não há reserva para esta data

# cancela uma reserva
sistema_reservas.cancelar_reserva("23-12-2023", 301)

# lista todas as reservas de um quarto específico 
print(sistema_reservas.listar_reservas(101))
