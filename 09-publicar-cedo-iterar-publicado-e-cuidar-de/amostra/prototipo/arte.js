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

// Fundo, calçada de ladrilhos e asfalto com grão. Nada disso muda de um quadro para outro.
function pintarFundo(ctx) {
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
}

// US-01: pinto o fundo uma vez numa tela fora da página e copio essa tela a cada quadro.
var fundo = null;
window.desenharRua = function (ctx) {
  if (!fundo) {
    fundo = document.createElement('canvas');
    fundo.width = 640;
    fundo.height = 400;
    pintarFundo(fundo.getContext('2d'));
  }
  ctx.drawImage(fundo, 0, 0);
};

// US-04: as três peças da semana na vitrine. Troque aqui toda semana.
window.VITRINE = [
  { nome: 'jogo de cama de casal', cor: PALETA.mostarda },
  { nome: 'jogo de cama de solteiro', cor: PALETA.jeans },
  { nome: 'jogo de cama infantil', cor: PALETA.vinho }
];

// Sprites aprovados. O atlas.js é escrito por sprites.py integrar; com ele vazio, tudo sai desenhado por código.
var IMAGENS = {};
Object.keys(window.ATLAS || {}).forEach(function (nome) {
  if (typeof Image === 'undefined') return;
  var img = new Image();
  img.src = window.ATLAS[nome].arquivo;
  IMAGENS[nome] = img;
});

// Desenha o sprite com o meio da base em (x, y). Se ele não estiver no jogo, desenha a reserva de antes.
function peca(ctx, nome, x, y, reserva) {
  var a = (window.ATLAS || {})[nome], img = IMAGENS[nome];
  if (!a || !img || !img.complete || !img.naturalWidth) { reserva(); return; }
  ctx.fillStyle = PALETA.sombra;                            // a sombra de contato fica com o código
  ctx.fillRect(Math.round(x - a.w / 2) + 2, y - 2, a.w - 4, 3);
  ctx.drawImage(img, Math.round(x - a.w / 2), y - a.h);
}

// Foto 2: salão comprido; Foto 3: balcão com o caixa e o banco alto; Foto 1: toldo, vitrine, porta e floreira.
window.desenharLoja = function (ctx) {
  caixa(ctx, PALETA.creme, 200, 40, 240, 230);            // salão
  peca(ctx, 'mesa-cama', 275, 190, function () {          // mesa baixa 1
    caixa(ctx, PALETA.madeira, 250, 120, 50, 70);
    caixa(ctx, PALETA.tecido, 258, 130, 34, 50);          // jogos de cama
  });
  peca(ctx, 'mesa-cama', 365, 190, function () {          // mesa baixa 2
    caixa(ctx, PALETA.madeira, 340, 120, 50, 70);
    caixa(ctx, PALETA.tecido, 348, 130, 34, 50);
  });
  peca(ctx, 'balcao', 395, 76, function () {              // balcão (Foto 3)
    caixa(ctx, PALETA.madeira, 360, 50, 70, 26);
  });
  peca(ctx, 'banco-alto', 372, 100, function () {         // banco alto (Foto 3)
    caixa(ctx, PALETA.madeira, 366, 84, 12, 14);
  });
  caixa(ctx, PALETA.verdeEscuro, 410, 80, 20, 30);        // porta Somente funcionários
  caixa(ctx, PALETA.vidro, 210, 262, 80, 8);              // vitrine (Foto 1)
  VITRINE.forEach(function (p, i) { caixa(ctx, p.cor, 216 + i * 24, 263, 18, 6); });
  caixa(ctx, PALETA.vidro, 330, 262, 50, 8);              // porta de vidro (Foto 1)
  caixa(ctx, PALETA.verde, 200, 270, 240, 14);            // toldo verde (Foto 1)
  peca(ctx, 'floreira', 392, 302, function () {           // floreira na calçada (Foto 1)
    caixa(ctx, PALETA.terracota, 384, 290, 16, 12);
  });
};
