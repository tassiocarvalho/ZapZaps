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
