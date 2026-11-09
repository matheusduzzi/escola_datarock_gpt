## Exercício: publique o seu protótipo, três versões e a lista de direitos

Agora é o seu protótipo, o que você construiu no módulo. A gerente pediu o link para ver no celular e quer pôr o passeio no perfil da loja. Você publica privado, faz três versões e só abre depois da lista de direitos.

Copie para a pasta do seu protótipo o `publicar.py` e os modelos em branco `DIREITOS.md` e `VERSOES.md` do kit. Os comandos rodam na pasta que tem os dois modelos. Se o seu protótipo estiver em outra pasta, use `--prototipo` com o caminho dele.

1. **A pasta que vai para o ar.** Preencha a tabela de arquivos do `DIREITOS.md`, uma linha por arquivo ou padrão. Rode `python3 publicar.py montar` e veja se só foi para a `dist` o que deve ir para a web.
2. **A primeira versão privada.** Rode o teste do portão. Com ele passando, peça ao ChatGPT para publicar só a `dist`, com acesso só para você. Anote o endereço no `DIREITOS.md`.
3. **Três versões.** Faça pelo menos três versões no mesmo endereço, cada uma com uma mudança só. Uma delas resolve algo que você viu no celular. Outra refina um componente, como os móveis, as figuras da calçada ou a página de créditos. Rode o teste antes de cada uma.
4. **O registro.** Para cada versão, uma linha no `VERSOES.md`: quando, o commit, o que mudou, onde testou e o endereço. O que não testou, escreva que não testou.
5. **A lista de direitos.** Preencha as três tabelas do `DIREITOS.md`. Na de arquivos, os dados de mapa com o crédito na tela e no README, e cada foto com a origem e a licença. Na de pessoas, cada figura com nome ou cara, inventada ou não. Na de marcas e referência visual, o nome da loja, o estilo e qualquer mascote ou logo. Três regras valem aqui: foto de terceiro sem licença livre fica fora, nenhuma pessoa real vira personagem sem autorização por escrito e nada imita uma marca.
6. **O portão do público.** Rode `python3 publicar.py montar` e depois `python3 publicar.py conferir` até sair com 0.
7. **O acesso.** Só depois do `conferir` com 0, mude o acesso para a opção mais estreita que serve ao pedido da gerente. Anote qual opção você escolheu e a data.
8. **O que o programa não vê.** Escreva de duas a quatro frases sobre o que você olhou com os seus olhos: gente reconhecível nas imagens, personagem que lembra alguém, mascote ou estilo que imita uma marca, crédito legível no celular.

**Entregue:**
- o endereço publicado e a opção de acesso que ficou, com a data;
- o `VERSOES.md`, com pelo menos três versões;
- o `DIREITOS.md` preenchido;
- a saída do último `conferir`;
- as frases do passo 8.

Se a sua conta não tiver o Sites, use um serviço de hospedagem em que você escolhe quem abre, e diga qual foi.

<details><summary>Dica 1</summary>

Comece pela tabela de arquivos, com padrões: `*.html`, `*.js`, `sprites/*.png`. Depois escreva as linhas que fogem do padrão, como o arquivo de dados do mapa e cada foto. A linha exata vale mais que o padrão. Rode o `montar` e leia a lista "vai" e "fica fora" antes de publicar.

</details>

<details><summary>Dica 2</summary>

Se o `conferir` diz que a página não mostra o crédito, procure onde ele está. Comentário no HTML não aparece na tela. Para as versões, escreva o pedido ao ChatGPT com uma mudança só e com o que deve ficar como está. Peça o commit no fim da resposta e copie para o `VERSOES.md`.

</details>
