# Nao - Reconhecimento óptico de caracteres avançado para NVDA

* Autores: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Baixar [Versão estável][1]
* Compatível com NVDA: 2019.3 em diante

Nao (reconhecimento óptico de caracteres avançado para NVDA) é um complemento que melhora a funcionalidade padrão de reconhecimento óptico de caracteres oferecida pelo NVDA em versões modernas do Windows.
Enquanto o o comando padrão do NVDA usa os recursos de OCR do Windows para efetuar o reconhecimento da tela, o NAO é capaz de efetuar reconhecimento em arquivos salvos no disco rígido ou em dispositivos USB.
Use tecla NVDA-Shift-R para efetuar reconhecimento em qualquer tipo de imagem ou pdf!
Simplesmente coloque o cursor sobre o arquivo desejado, sem abri-lo, e pressione tecla NVDA-Shift-R.
O arquivo será reconhecido e uma janela simples de texto aparecerá, na qual você poderá ler todo o conteúdo reconhecido, efetuar buscas por texto específico, copiar para a área de transferência e salvá-lo.
O Nao também é capaz de lidar com PDFs contendo múltiplas páginas, então se você tiver um documento inacessível não se preocupe, o OCR do Windows será capaz de fazer o reconhecimento total.

## Requisitos de sistema
Este complemento funciona nos Windows 10 e 11, já que esses sistemas oferecem serviço nativo de reconhecimento ótico de caracteres.
O Nao requer uma versão do NVDA igual ou superior a 2019.3, então não tente utilizá-lo com versões mais antigas do leitor de telas.
Note que o Nao funciona apenas quando usado com o Windows Explorer, na área de trabalho, com o Total Commander ou com o xplorer² filemanager. Não tente utilizá-lo com aplicativos como o 7zip ou Winrar, já que esses programas não são suportados.

## Funcionalidades e comandos
* NVDA + Shift + R: reconhece qualquer tipo de imagem ou pdf a partir do sistema de arquivos;
  * PgUp / PgDown: move o cursor entre páginas reais de um documento de múltiplas páginas.
  * Ctrl + S: Salva o documento no formato nao-document-format.
  * P: Informa o número da página atual relativa ao cursor em um documento de múltiplas páginas.
  * L: informa a linha atual com relação à página corrente.
  * Shift + L: informa a linha atual com relação ao documento inteiro.
  * G: Vai diretamente a uma página.
  * C: copia todo o texto para a área de transferência.
  * S: salva uma cópia do documento no formato texto.
  * F: localiza texto e lê algumas palavras antes e depois do resultado.
* NVDA + Shift + Ctrl + R: realiza a captura completa da tela e reconhece o conteúdo.
  * Note que é possível usar comandos padrão do NVDA para explorar a janela e mover o foco para um elemento. Por exemplo, você pode usar as setas para se mover até um botão e pressionar enter para ativá-lo. Você também pode mover o cursor do mouse até a posição atual com tecla NVDA-barra do teclado numérico e clicar com o botão esquerdo ou direito.

Note que você pode alterar as teclas de atalho do Nao usando o diálogo de definição de comandos do NVDA. Acesse o menu do NVDA, vá até preferências e no sub menu selecione definir comandos. Lembre-se de que essas funcionalidades não são globais, elas só funcionarão em aplicativos de onde é possível realizar OCR. Assim, esses gestos aparecerão apenas se você estiver na área de trabalho, no explorador de arquivos, no Total Commander ou no Xplorer.

Você também pode abortar um processo de OCR apenas pressionando "Cancelar" na janela com a barra de progresso.

Também é possível encontrar um sub menu chamado Nao dentro do menu de ferramentas do NVDA. No momento, ele apenas oferece acesso a um diálogo de onde é possível fazer uma doação, mas nós vamos melhorá-lo com novas funcionalidades!

## Suporte e doações
Nao é totalmente gratuito. Entretanto, lembre-se de que este complemento é feito durante o tempo livre de seus desenvolvedores.
Nós apreciaríamos demais qualquer contribuição que você possa nos dar!
Se você entender que nosso trabalho é bom e melhora sua vida, <a href="https://nvda-nao.org/donate">considere fazer uma doação.</a>

Quer reportar um bug, sugerir novas funcionalidades, traduzir o complemento para o seu idioma? Temos um e-mail para você! Apenas escreva para support@nvda-nao.org e nós estaremos felizes em ajudá-lo.

## Histórico
### 2022.1.2
* Salvar e carregar arquivos no formato de arquivo nao-document file format.
* Um cache de documentos reconhecidos anteriormente torna o processo de reconhecimento mais rápido. Se um arquivo for detectado  no cache, a versão cacheada é usada em vez de um novo reconhecimento ocorrer.
* Armazenar a última posição de leitura nos meta dados do cache.
* Limpeza automática para o cache de documentos.
* Limpeza manual do cache a partir do menu de ferramentas.
* Agora, um arquivo pode ser reconhecido diretamente a partir de uma pasta comprimida no Windows explorer.
* Melhor detecção de arquivos inválidos.
* Melhor compatibilidade com Windows Explorer usando diferentes estratégias de seleção de arquivos: Primeiro, tentar usando Shell.Application no NVDA, depois tentar Shell.Application no PowerShell e, por fim, usar navegação manual.
* Motor de OCR mantém a configuração do idioma atual mesmo se este for mudado durante um processo de reconhecimento de documentos de múltiplas páginas.
* Fila de OCR para reconhecimento a partir de múltiplas origens.
* Comando pg down vai até o fim do documento e anuncia a linha atual quando usado na última página de um documento.
* Diretório temporário do Windows é usado para as ferramentas de conversão de arquivo em vez do diretório do complemento (melhor desempenho no NVDA portável).
* Tradução para Romeno e atualização da tradução para Chinês simplificado.
### 2022.1.1
* Suporte para o formato de arquivo DjVu.
* Suporte para arquivos tiff de múltiplas páginas.
* Correção de bugs de codificação de PDFs em sistemas operacionais em chinês simplificado.
* Atualização manual do complemento no menu ferramentas do NVDA.
* Compatibilidade com NVDA a partir da versão 2019.3.
### 2022.1
* Atualizações automáticas do complemento.
* Atualização nas traduções para Francês e Espanhol.
### 2021.2
* OCR de PDFs e imagens é apresentado em uma nova janela de texto, com alguns comandos para operações simples.
* Suporte para o gerenciador de arquivos Xplorer.
* Teclas de comando do Nao podem ser modificadas a partir do diálogo de definir comandos do NVDA.
* Nao funciona apenas em contexto apropriado, então se você estiver em um aplicativo onde seu funcionamento não faz sentido os seus comandos serão ignorados. Isso resolveu um problema sério que impedia que usuários do Word e do Excel pressionassem nvda-Shift-R, uma vez que o complemento estava interceptando esse comando incorretamente.
* Um processo longo de OCR pode ser abortado simplesmente pressionando-se o botão "Cancelar" na janela da barra de progresso.
* Traduções para Turco, Russo, Espanhol, Chinês e Francês adicionadas.
* Usuários podem fazer doações para o projeto.
* Corrigido um bug com alguns caracteres em nomes de arquivos que impediam o processo de OCR de ocorrer corretamente.
### 2021.1
* Primeira versão pública!

[1]: https://nvda-nao.org/download

