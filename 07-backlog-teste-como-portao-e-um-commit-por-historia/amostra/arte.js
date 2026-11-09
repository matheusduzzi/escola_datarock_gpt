// Arte: a loja do Centro vista de cima, com a paleta da direção de arte.
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

// O mesmo número sai sempre para o mesmo x e y: a rua fica igual em toda visita.
function sorteio(n) {
  var x = Math.imul(n ^ 0x9e3779b9, 0x85ebca6b);
  x ^= x >>> 13;
  return (x >>> 0) / 4294967296;
}

// Fundo, calçada de ladrilhos e asfalto com grão, desenhados a cada quadro.
window.desenharRua = function (ctx) {
  var x, y;
  ctx.fillStyle = PALETA.creme;
  ctx.fillRect(0, 0, 640, 284);
  for (y = 284; y < 330; y += 4) {
    for (x = 0; x < 640; x += 4) {
      ctx.fillStyle = ((x + y) / 4) % 2 ? PALETA.terracota : PALETA.madeira;
      ctx.fillRect(x, y, 4, 4);
    }
  }
  for (y = 330; y < 400; y += 4) {
    for (x = 0; x < 640; x += 4) {
      ctx.fillStyle = sorteio(x * 131 + y) < 0.8 ? PALETA.rua : PALETA.sombra;
      ctx.fillRect(x, y, 4, 4);
    }
  }
};

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
