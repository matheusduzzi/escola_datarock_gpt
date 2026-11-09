// Vida: gente e bichos na calçada. No máximo 4 figuras, e no máximo 1 delas é bicho.
(function () {
  var P = window.PALETA;
  var CALCADA = { y0: 292, y1: 318, x0: 10, x1: 630 };
  var parado = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var figuras = [
    { tipo: 'pessoa', nome: 'dona Cida', x: 60, y: 300, v: 30, roupa: P.mostarda },
    { tipo: 'carteiro', x: 420, y: 310, v: -36, roupa: P.jeans },   // US-02: no lugar de um pedestre
    { tipo: 'ciclista', x: 250, y: 296, v: 62, roupa: P.vinho },
    { tipo: 'bicho', x: 540, y: 314, v: -24, roupa: P.madeira }
  ];

  function andar(f, dt) {
    var x = f.x + f.v * dt;
    if (x < CALCADA.x0 || x > CALCADA.x1) { f.v = -f.v; return; }
    f.x = x;
  }

  window.vida = {
    CALCADA: CALCADA,
    figuras: figuras,
    atualizar: function (dt) {
      if (parado || window.conversaAberta) return;
      figuras.forEach(function (f) { andar(f, dt); });
    },
    desenhar: function (ctx) {
      figuras.forEach(function (f) {
        var a = f.tipo === 'bicho' ? 6 : 14;
        ctx.fillStyle = P.sombra;
        ctx.fillRect(f.x - 5, f.y + 2, 10, 3);
        ctx.fillStyle = f.roupa;
        ctx.fillRect(f.x - 4, f.y - a, 8, a);
        ctx.strokeStyle = P.carvao;
        ctx.lineWidth = 1;
        ctx.strokeRect(f.x - 4, f.y - a, 8, a);
        if (f.nome) { ctx.fillStyle = P.carvao; ctx.fillText(f.nome, f.x - 20, f.y - a - 4); }
      });
    }
  };
})();
