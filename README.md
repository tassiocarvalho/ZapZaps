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
No estado atual, o módulo `chat.py` não implementa criptografia nas mensagens trocadas entre os membros do chat. Esta decisão foi influenciada por vários fatores relacionados ao design inicial do algoritmo e à trajetória de desenvolvimento do projeto.

### Fatores que Influenciaram a Ausência de Criptografia

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
Embora a criptografia não esteja presente na versão atual do `chat.py`, ela é reconhecida como uma melhoria importante para a segurança e privacidade dos usuários. Em futuras iterações ou projetos similares, a integração de métodos de criptografia será considerada desde o início do desenvolvimento, garantindo uma comunicação mais segura.

### Realização de teste do sistema:
O sistema foi testado em containers sem o uso de servidor externo, não foi configurada na execução do sistema, não foi implementada no Dockerfile a funcionalidade de rodar o sistema dentro do container e escutar servidores externos.

Para criar um Docker container é usado o seguinte comando
´´´ docker build -t chat . ´´´´
para executar 
´´´ docker run -it chat´´´

