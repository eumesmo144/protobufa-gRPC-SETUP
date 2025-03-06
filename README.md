

## **Protobuf e gRPC**

---

### **1. Qual problema a tecnologia resolve?**

#### **Contextualização**
- Em sistemas distribuídos e aplicações de microserviços, a comunicação eficiente entre serviços é um desafio crítico.
- Formatos tradicionais como **JSON** e **XML** são verbosos, ocupam mais espaço e são mais lentos para processar.
- A serialização de dados deve ser **rápida, eficiente e padronizada** para evitar problemas de compatibilidade e melhorar a performance.

#### **Problemas resolvidos**
- **Eficiência na serialização de dados:** Protobuf usa um formato binário compacto e eficiente, reduzindo latência e consumo de banda.
- **Interoperabilidade:** Garante que diferentes linguagens e plataformas possam trocar dados sem perda de informação ou necessidade de conversões complicadas.
- **Evolução de APIs sem quebra de compatibilidade:** Protobuf permite adicionar novos campos sem impactar versões antigas de clientes.

---

### **2. Como ela resolve?**

#### **Protocol Buffers (Protobuf)**
- É um **método de serialização de dados** criado pelo Google.
- Usa **arquivos `.proto`** para definir **estruturas de dados**, que são compiladas para gerar código automaticamente para diferentes linguagens.
- Utiliza um **formato binário eficiente**, ao invés de texto como JSON ou XML.

#### **gRPC**
- Um framework de comunicação que usa Protobuf como base.
- Implementa **Remote Procedure Call (RPC)** sobre HTTP/2, permitindo comunicação de alta performance entre serviços.
- Permite **streaming bidirecional** e suporta **autenticação, balanceamento de carga e deadlines**.

#### **Exemplo de um arquivo `.proto`**
```proto
syntax = "proto3";

message User {
  string name = 1;
  int32 age = 2;
}

service UserService {
  rpc GetUserInfo(UserRequest) returns (User);
}
```
Esse arquivo define um serviço que recebe um `UserRequest` e retorna um `User`.

---

### **3. Quais as alternativas e comparações?**

#### **Alternativas**
| Tecnologia  | Formato de Dados | Comunicação | Serialização | Performance |
|------------|----------------|-------------|--------------|------------|
| **Protobuf + gRPC** | Binário | RPC | Sim | **Alta** |
| **JSON + REST** | Texto | HTTP | Não | Média |
| **XML + SOAP** | Texto | HTTP/SOAP | Não | Baixa |
| **Avro** | Binário | Mensagens/Eventos | Sim | Alta |

#### **Por que Protobuf + gRPC?**
- **Mais rápido e eficiente:** Protobuf é binário e compacto, enquanto JSON e XML são verbosos.
- **Esquema estruturado:** Diferente de JSON, Protobuf tem um contrato bem definido (`.proto`).
- **Streaming bidirecional:** Diferente de REST, gRPC permite comunicação **full-duplex**.
- **Evolução segura:** Permite adicionar novos campos sem quebrar clientes existentes, diferentemente de JSON REST APIs.

---

### **4. Demonstração prática**

#### **Passo 1: Instalar dependências**
```bash
# Instalar protoc (Linux/macOS)
sudo apt install protobuf-compiler  # Linux
brew install protobuf  # macOS

# Instalar plugin do gRPC para Python
pip install grpcio grpcio-tools
```

#### **Passo 2: Criar um arquivo `.proto`**
Arquivo: `user.proto`
```proto
syntax = "proto3";

message UserRequest {
  string name = 1;
}

message UserResponse {
  string name = 1;
  int32 age = 2;
}

service UserService {
  rpc GetUserInfo(UserRequest) returns (UserResponse);
}
```

#### **Passo 3: Gerar código a partir do `.proto`**
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
```

#### **Passo 4: Criar o servidor gRPC**
Arquivo: `server.py`
```python
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUserInfo(self, request, context):
        return user_pb2.UserResponse(name=request.name, age=30)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

#### **Passo 5: Criar o cliente gRPC**
Arquivo: `client.py`
```python
import grpc
import user_pb2
import user_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = user_pb2_grpc.UserServiceStub(channel)

request = user_pb2.UserRequest(name="Alice")
response = stub.GetUserInfo(request)

print(f"Nome: {response.name}, Idade: {response.age}")
```

#### **Execução**
Em terminais separados:
```bash
python server.py  # Inicia o servidor gRPC
python client.py  # Faz uma requisição e recebe resposta
```

**Resultado esperado:**
```bash
Nome: Alice, Idade: 30
```

---

### **5. Laboratório para os meus amiguinhos** :nerd_face:

#### **Objetivo**
Criar um serviço gRPC para um sistema de pedidos, onde clientes podem solicitar um produto e obter informações sobre ele.

#### **Passos**
1. Criar um arquivo `order.proto` que define um serviço `OrderService` com:
   - Um método `PlaceOrder` que recebe um `OrderRequest` e retorna um `OrderResponse`.
2. Gerar os arquivos Python usando `protoc`.
3. Implementar um servidor gRPC que processa pedidos e retorna informações como status e ID do pedido.
4. Criar um cliente que faz pedidos e recebe respostas do servidor.

---

### **Conclusão**
- Protobuf e gRPC tornam a comunicação entre serviços mais rápida e eficiente.
- Comparado a REST/JSON, **gRPC é mais performático e suporta streaming**.
- Protobuf garante **estruturação e evolução de dados sem quebra de compatibilidade**.
