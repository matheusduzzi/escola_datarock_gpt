// O quadro da cena. A página e o teste rodam esse mesmo código.
(function () {
  window.conversaAberta = false;
  window.cena = {
    alternarConversa: function () { window.conversaAberta = !window.conversaAberta; },
    quadro: function (ctx, dt) {
      desenharRua(ctx);
      desenharLoja(ctx);
      vida.atualizar(dt);
      vida.desenhar(ctx);
      if (window.conversaAberta) {
        ctx.fillStyle = PALETA.tecido;
        ctx.fillRect(140, 20, 360, 40);
        ctx.fillStyle = PALETA.carvao;
        ctx.fillText('Seu Dito: Veio ver cortina ou toalha?', 156, 44);
      }
    }
  };
})();
