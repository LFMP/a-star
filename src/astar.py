import heapq
import copy

final_config = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

##################### Modelagem pra organizar o tabuleiro #####################


class inputAStar:
  def __init__(self, matriz, pai, sucessores, g, h):
    self.matriz = copy.deepcopy(matriz)
    self.g = g
    self.h = h
    self.pai = pai
    self.sucessores = sucessores

  def f(self):
    return self.g + self.h

  def add_sucessor(self, sucessor):
    self.sucessores.append(sucessor)

##################### Geração de sucessores #####################


def geraSucessores(no):
  matriz = copy.deepcopy(no.matriz)
  i = j = 0
  while (True):
    if (j == 4):
      j = 0
      i += 1
    if(matriz[i][j] == 0):
      break
    else:
      j += 1
  if(i > 0):
    up = copy.deepcopy(matriz)
    up[i][j], up[i-1][j] = up[i-1][j], up[i][j]
    no.add_sucessor(inputAStar(up, [], [], no.g + 1, 0))
  if(j > 0):
    left = copy.deepcopy(no.matriz)
    left[i][j], left[i][j-1] = left[i][j-1], left[i][j]
    no.add_sucessor(inputAStar(left, [], [], no.g + 1, 0))
  if(i < 3):
    down = copy.deepcopy(no.matriz)
    down[i][j], down[i+1][j] = down[i+1][j], down[i][j]
    no.add_sucessor(inputAStar(down, [], [], no.g + 1, 0))
  if(j < 3):
    right = copy.deepcopy(no.matriz)
    right[i][j], right[i][j+1] = right[i][j+1], right[i][j]
    no.add_sucessor(inputAStar(right, [], [], no.g + 1, 0))

##################### Trata a entrada e monta o tabuleiro #####################


def montaTabuleiro(entrada):
  lido = input().split(' ')
  lido = [num for num in lido if num]
  k = 0

  for i in range(0, 4):
    for j in range(0, 4):
      entrada[i][j] = int(lido[k])
      k += 1

##################### Heurísticas #####################

posicao_pecas = [
  [3,3], [0,0], [0,1], [0,2],
  [0,3], [1,0], [1,1], [1,2],
  [1,3], [2,0], [2,1], [2,2],
  [2,3], [3,0], [3,1], [3,2]]

def distancia_manhatan(valor,i,j):
  soma = 0
  i_certo = posicao_pecas[valor][0]
  j_certo = posicao_pecas[valor][1]

  soma += int(abs(j - j_certo))
  soma += int(abs(i - i_certo))

  return soma

def h_linha_1(start):
  foraDoLugar = 0
  for (indice, i) in enumerate(start):
    for j in range(len(i)):
      if (i[j] != final_config[indice][j]):
        foraDoLugar += 1
  return foraDoLugar


def h_linha_2(start):
  foraDaOrdem = 0
  temp = []
  for i in range(0, 4):
    for j in range(0, 4):
      temp.append(start[i][j])
  for k in range(len(temp)):
    if(k == 0):
      pass
    else:
      if((temp[k] != (temp[k-1] + 1)) and temp[k-1] != 0):
        foraDaOrdem += 1
  return foraDaOrdem

def h_linha_3(start):
  soma = 0
  for i in range(4):
    for j in range(4):
      if(start[i][j]):
        soma += distancia_manhatan(start[i][j],i,j)

  return soma

def h_linha_4(start):
  soma = 0
  p = [0.4,0.2,0.4]
  return int(p[0]*h_linha_1(start) + p[1]*h_linha_2(start) + p[2]*h_linha_3(start))

def h_linha_5(start):
  return max(h_linha_1(start),h_linha_2(start),h_linha_3(start))

##################### Principal #####################


def astar(start,selected):
  h_linha = [h_linha_1,h_linha_2,h_linha_3,h_linha_4,h_linha_5]
  T = str(final_config)
  A = F = {}
  h = []
  A[str(start)] = inputAStar(start, [], [], 0, h_linha[selected](start))
  heapq.heappush(h, (A[str(start)].f(), str(start)))
  v = A[str(start)]
  while A and (str(v.matriz) != T):
    while True:
      posicao = heapq.heappop(h)
      if (posicao[1] in A):
        break
    v = A.get(posicao[1])
    A.pop(str(v.matriz))
    F[str(v.matriz)] = v
    if not v.sucessores:
      geraSucessores(v)
    m = v.sucessores
    for i in range(0, len(v.sucessores)):
      m_linha = str(m[i].matriz)
      if(m_linha in A and m[i].g < A[m_linha].g):
        A.pop(m_linha)
      if(m_linha not in A and m_linha not in F):
        A[str(m[i].matriz)] = m[i]
        A[str(m[i].matriz)].pai = v
        A[str(m[i].matriz)].h = h_linha[selected](m[i].matriz)
        heapq.heappush(h, (A[str(m[i].matriz)].f(), str(m[i].matriz)))
  return v.g


def main():
  entrada = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
  montaTabuleiro(entrada)
  print(astar(entrada,4))


if __name__ == '__main__':
  main()
