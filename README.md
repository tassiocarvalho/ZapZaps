# Introdução

## Descrição do Sistema `chat.py`

O `chat.py` é um sistema de chat em tempo real que opera em um modelo peer-to-peer (P2P), utilizando sockets UDP para comunicação direta entre os usuários. Este módulo foi desenvolvido com o foco em simplicidade e eficiência, permitindo a criação de grupos de chat dinâmicos onde os membros podem trocar mensagens de forma rápida e sincronizada. O sistema também implementa um mecanismo de relógio vetorial (VetorClock) para manter a consistência e a ordem causal das mensagens no ambiente distribuído.

## Metodologia de Desenvolvimento

### Tecnologias Utilizadas
O desenvolvimento do `chat.py` se baseou em várias tecnologias e abordagens chave:

1. **Sockets UDP:** Para a comunicação de rede, o sistema utiliza sockets UDP, que oferecem uma forma eficiente e de baixa latência para troca de mensagens em uma rede P2P.
2. **Python 3.x:** O sistema é implementado em Python 3, aproveitando suas bibliotecas robustas para redes e concorrência.
3. **Threads:** Utilizamos múltiplas threads para permitir a escuta simultânea de mensagens entrantes e a interação do usuário com a interface do chat.
4. **Relógio Vetorial:** O algoritmo VetorClock é usado para manter a ordem das mensagens, garantindo que o histórico de chat seja consistente entre todos os membros do grupo.

![image](https://github.com/tassiocarvalho/ZapZaps/assets/90158519/e59672ee-7f80-4509-8036-9cab7f1a8bbf)


### Principais Características
- **Comunicação P2P UDP:** Proporciona uma comunicação direta e eficiente entre os membros do chat.
- **Gerenciamento Dinâmico de Membros:** Permite a adição e remoção de membros em tempo real sem interromper o fluxo de comunicação.
- **Sincronização de Mensagens:** Assegura que todos os membros do chat tenham um histórico de mensagens atualizado e ordenado corretamente.
- **Relógio Vetorial:** Implementa uma lógica de ordenação baseada em relógio vetorial para manter a consistência das mensagens em um ambiente distribuído.

### Processo de Desenvolvimento
O desenvolvimento seguiu uma abordagem iterativa:

1. **Prototipagem e Design Inicial:** Iniciamos com uma versão básica para estabelecer a comunicação P2P e a interface do usuário.
2. **Testes e Refinamento:** Após a implementação inicial, realizamos testes extensivos para identificar e corrigir falhas, além de aprimorar a performance e a usabilidade.
3. **Integração de Funcionalidades:** Gradualmente, integramos funcionalidades adicionais, como o relógio vetorial e o gerenciamento dinâmico de membros.
4. **Documentação e Preparação para Lançamento:** Completamos o projeto com uma documentação detalhada, preparando o sistema para uso e distribuição.


## Descrição
O módulo `chat.py` é uma aplicação de chat P2P (peer-to-peer) que utiliza sockets UDP para a comunicação entre os usuários. O sistema permite adicionar novos membros ao grupo de chat e mantém um histórico de mensagens sincronizado entre todos os participantes.

## Funcionalidades
- **Comunicação P2P UDP:** Utiliza o protocolo UDP para troca de mensagens em um ambiente peer-to-peer.
- **Adicionar Novos Membros:** Possibilidade de adicionar novos membros ao chat em tempo real.
- **Sincronização de Mensagens:** Mantém um histórico de mensagens sincronizado entre todos os membros do chat.
- **Relógio Vetorial (VetorClock):** Implementa um relógio vetorial para manter a ordem causal das mensagens.

## Como Funciona
1. **Inicialização do Socket:** Cria um socket UDP e se vincula a um endereço IP local e porta.
2. **Recebimento de Mensagens:** Uma thread é iniciada para escutar mensagens recebidas de outros membros do chat.
3. **Tratamento de Mensagens:**
   - **Atualização de Membros:** Atualiza a lista local de membros quando uma nova lista é recebida.
   - **Histórico de Chat:** Sincroniza o histórico de mensagens com novos membros.
   - **Mensagens Regulares:** Processa e exibe mensagens de chat.
4. **Envio de Mensagens:** Permite ao usuário enviar mensagens que são transmitidas para todos os membros do chat.
5. **Adição de Novos Membros:** Novos membros podem ser adicionados ao chat através de um comando específico.

## Instruções de Uso
1. **Execução do Script:**
   - Execute o script `chat.py`.
   - Forneça a porta desejada para a comunicação.
2. **Adicionar um Novo Membro:**
   - Para adicionar um novo membro, digite: `/add_membro <IP> <PORTA>`.
   - O novo membro receberá o histórico de mensagens existente.
3. **Envio de Mensagens:**
   - Digite sua mensagem e pressione Enter para enviar.

## Dependências
- Python 3.x
- Módulo `socket`
- Módulo `threading`
- Módulo `json`
- Módulo `vetorclock` (deve estar disponível no mesmo diretório)

# Seção de Criptografia

## Criptografia no `chat.py`

### Contexto Atual
No estado atual, o módulo `chat.py` não implementa criptografia ideal nas mensagens trocadas entre os membros do chat. Esta decisão foi influenciada por vários fatores relacionados ao design inicial do algoritmo e à trajetória de desenvolvimento do projeto, foi implemetado uma criptografia usando Cifra de César

### Fatores que Influenciaram a Ausência de Criptografia ideal

1. **Estrutura do Algoritmo:**
   - O design inicial do `chat.py` foi focado em estabelecer uma comunicação básica P2P usando sockets UDP. A estrutura do algoritmo foi moldada para priorizar a funcionalidade principal de enviar e receber mensagens em um ambiente de rede simples.
   - A integração da criptografia exigiria uma camada adicional de complexidade que não estava alinhada com os objetivos iniciais do projeto.

2. **Foco nas Versões Anteriores:**
   - Antes de desenvolver a versão P2P do `chat.py`, foram criadas outras versões que não eram baseadas em P2P. O tempo e esforço dedicados a essas versões anteriores consumiram uma parte significativa dos recursos disponíveis para o projeto.
   - Isso resultou em menos tempo e oportunidade para explorar e implementar recursos de segurança avançados, como a criptografia, na versão P2P.

3. **Limitações de Tempo:**
   - O desenvolvimento de qualquer funcionalidade adicional, incluindo a criptografia, é limitado pelo tempo disponível. No caso deste projeto, a priorização de outras funcionalidades e versões do chat consumiu grande parte do tempo de desenvolvimento.
   - Consequentemente, a implementação de um sistema de criptografia robusto não foi viável dentro do prazo estabelecido para este projeto.

### Considerações Futuras
Embora a criptografia não esteja presente na versão atual do `chat.py`, porém foi implementada a Cifra de César que não é o aconselhavel, a criptografia assimetrica ou simetrica é reconhecida como uma melhoria importante para a segurança e privacidade dos usuários. Em futuras iterações ou projetos similares, a integração de métodos de criptografia será considerada desde o início do desenvolvimento, garantindo uma comunicação mais segura.

---

### Realização de Testes do Sistema

#### Contexto
O sistema foi desenvolvido para operar em containers, priorizando a independência de servidores externos. Esta abordagem assegura uma maior flexibilidade e portabilidade do sistema. No entanto, até o momento atual, a configuração para conexão com servidores externos não foi implementada, e o `Dockerfile` não está configurado para suportar a execução do sistema em modo de escuta de servidores externos.

#### Criação e Execução de Containers Docker

Para facilitar o teste e a implantação, o sistema pode ser encapsulado dentro de um container Docker. Seguem os passos para criar e executar o container:

1. **Criação do Container:**  
   Utilize o seguinte comando para construir a imagem Docker do sistema, substituindo `chat` pelo nome que deseja atribuir à sua imagem:

   ```bash
   docker build -t chat .
   ```

   Este comando lê o `Dockerfile` presente no diretório atual e constrói uma imagem Docker denominada `chat`.

2. **Execução do Container:**  
   Após a criação da imagem, você pode iniciar um container a partir desta imagem utilizando:

   ```bash
   docker run -it chat
   ```

   Este comando inicia um container baseado na imagem `chat`, e o parâmetro `-it` permite a interação com o container através do terminal.

#### TESTE 
![image](https://github.com/tassiocarvalho/ZapZaps/assets/90158519/d6a3421a-6ba2-45dd-988e-4ddfe8d7bfb1)
imagem acima mostra 4 usuários se comunicando no grupo do chat

#### Observações Importantes

- A configuração atual não permite que o sistema operando dentro do container se conecte a servidores externos. Futuras atualizações podem incluir essa funcionalidade.
- Recomenda-se verificar e ajustar as configurações de rede do Docker conforme necessário para atender às necessidades específicas do seu ambiente de teste.

