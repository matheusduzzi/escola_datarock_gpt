// Teste da Loja Aurora: roda arte.js, vida.js e cena.js no Node, sem navegador.
// O npm test roda esse arquivo, e o gancho de pre-commit roda o npm test.
// Cada regra vem do critério de uma história do BACKLOG.md ou de uma aula anterior.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const PASTA = __dirname;
const ARQUIVOS = ['arte.js', 'vida.js', 'cena.js'];
const DESENHO = ['fillRect', 'strokeRect', 'clearRect', 'fillText', 'strokeText', 'drawImage', 'fill', 'stroke'];

// Um canvas de mentira: guarda as cores e conta as chamadas que desenham.
function canvasDeTeste() {
  const ctx = { chamadas: 0, textos: [] };
  DESENHO.forEach(function (nome) {
    ctx[nome] = function (a) { ctx.chamadas++; if (nome === 'fillText') ctx.textos.push(a); };
  });
  ['beginPath', 'moveTo', 'lineTo', 'arc', 'rect', 'closePath', 'save', 'restore', 'translate', 'scale', 'setTransform']
    .forEach(function (nome) { ctx[nome] = function () {}; });
  return { width: 640, height: 400, getContext: function () { return ctx; }, ctx: ctx };
}

// Carrega o protótipo do zero, como a página faz.
function carregar() {
  const janela = {
    console: console, Math: Math,
    matchMedia: function () { return { matches: false }; },
    document: {
      createElement: function () { return canvasDeTeste(); },
      getElementById: function () { return null; },
      addEventListener: function () {}
    }
  };
  janela.window = janela;
  vm.createContext(janela);
  ARQUIVOS.forEach(function (nome) {
    vm.runInContext(fs.readFileSync(path.join(PASTA, nome), 'utf8'), janela, { filename: nome });
  });
  return janela;
}

function passos(j, n) {
  const ctx = canvasDeTeste().ctx;
  for (let i = 0; i < n; i++) j.cena.quadro(ctx, 1 / 60);
  return ctx;
}

const regras = [
  function figurasNaCalcada() {
    const f = carregar().vida.figuras;
    const bichos = f.filter(function (x) { return x.tipo === 'bicho'; }).length;
    const ok = f.length <= 4 && bichos <= 1;
    return [ok, f.length + ' figuras na calçada, ' + bichos + ' bicho (limite: 4 figuras, 1 bicho)'];
  },
  function ninguemSaiDaCalcada() {
    const j = carregar();
    const c = j.vida.CALCADA;
    let fora = 0;
    for (let i = 0; i < 2000; i++) {
      j.vida.atualizar(1 / 60);
      j.vida.figuras.forEach(function (f) {
        if (f.x < c.x0 || f.x > c.x1 || f.y < c.y0 || f.y > c.y1) fora++;
      });
    }
    return [fora === 0, fora + ' saídas da calçada em 2000 passos'];
  },
  function conversaParaTodos() {
    const j = carregar();
    const pos = function () { return j.vida.figuras.map(function (f) { return f.x + ',' + f.y; }); };
    passos(j, 10);
    j.cena.alternarConversa();
    let a = pos();
    passos(j, 120);
    const andaram = pos().filter(function (p, i) { return p !== a[i]; }).length;
    j.cena.alternarConversa();
    a = pos();
    passos(j, 60);
    const depois = pos().filter(function (p, i) { return p !== a[i]; }).length;
    const n = j.vida.figuras.length;
    return [andaram === 0 && depois === n,
      'com a conversa aberta, ' + andaram + ' de ' + n + ' andaram; depois de fechar, ' + depois + ' de ' + n];
  },
  // US-02: o carteiro passa na calçada, dentro do limite de figuras.
  function carteiroNaCalcada() {
    const n = carregar().vida.figuras.filter(function (f) { return f.tipo === 'carteiro'; }).length;
    return [n === 1, n + ' carteiro na calçada (pedido: 1)'];
  }
];

let falhas = 0;
regras.forEach(function (regra) {
  let r;
  try { r = regra(); } catch (e) { r = [false, regra.name + ' quebrou: ' + e.message]; }
  if (!r[0]) falhas++;
  console.log((r[0] ? 'ok: ' : 'FALHOU: ') + r[1]);
});
console.log(falhas ? falhas + ' de ' + regras.length + ' regras falharam' : regras.length + ' de ' + regras.length + ' regras ok');
process.exit(falhas ? 1 : 0);
