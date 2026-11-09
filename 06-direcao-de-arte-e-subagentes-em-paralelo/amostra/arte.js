// Frente Arte: a loja do Centro vista de cima, com as cores de DIRECAO-DE-ARTE.md.
window.PALETA = {
  creme: '#f3ead7', verde: '#3f7d4e', verdeEscuro: '#2a5a37', madeira: '#a8743f',
  terracota: '#c8613a', rua: '#8a8f94', vidro: '#8fc1d4', carvao: '#2b2a2e',
  tecido: '#fbf8f1', mostarda: '#d9a441', jeans: '#3d5a80', vinho: '#8c3b4a', sombra: '#4f6f6a'
};

function caixa(ctx, cor, x, y, w, h) {
  ctx.fillStyle = cor;
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = PALETA.carvao;
  ctx.lineWidth = 2;
  ctx.strokeRect(x, y, w, h);
}

// Foto 2: salão comprido; Foto 3: balcão no canto do fundo à direita; Foto 1: toldo, vitrine e porta.
window.desenharLoja = function (ctx) {
  caixa(ctx, PALETA.creme, 200, 40, 240, 230);            // salão
  caixa(ctx, PALETA.madeira, 250, 120, 50, 70);           // mesa baixa 1
  caixa(ctx, PALETA.madeira, 340, 120, 50, 70);           // mesa baixa 2
  caixa(ctx, PALETA.tecido, 258, 130, 34, 50);            // jogos de cama
  caixa(ctx, PALETA.tecido, 348, 130, 34, 50);
  caixa(ctx, PALETA.madeira, 360, 50, 70, 26);            // balcão (Foto 3)
  caixa(ctx, PALETA.verdeEscuro, 410, 80, 20, 30);        // porta Somente funcionários
  caixa(ctx, PALETA.vidro, 210, 262, 80, 8);              // vitrine (Foto 1)
  caixa(ctx, PALETA.vidro, 330, 262, 50, 8);              // porta de vidro (Foto 1)
  caixa(ctx, PALETA.verde, 200, 270, 240, 14);            // toldo verde (Foto 1)
};
