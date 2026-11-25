// Gera produtos.json (lido pelo robô do WhatsApp) a partir de fonte.html. Chamado pelo montar.py.
const fs = require('fs'), path = require('path');
const s = fs.readFileSync(path.join(__dirname, 'fonte.html'), 'utf8');
const bloco = (ini, fim) => { const a = s.indexOf(ini); const b = s.indexOf(fim, a); if (a < 0 || b < 0) throw new Error('bloco ' + ini); return s.slice(a, b + fim.length); };
const lojaIni = s.indexOf('const LOJA = {'), lojaFim = s.indexOf('const MARCAS = [');
const codigo = s.slice(lojaIni, lojaFim) + '\n' + bloco('const PRODUTOS = [', '\n];') + '\n({ LOJA, PRODUTOS })';
const { LOJA, PRODUTOS } = eval(codigo);
const slug = t => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const site = 'https://demen-loja.github.io/';
const out = {
  geradoEm: new Date().toISOString(),
  loja: { nome: 'DE men', site, endereco: LOJA.endereco, horario: LOJA.horario, pagamento: LOJA.pagamento, pagamentos: LOJA.pagamentos,
          envio: LOJA.envio, trocas: LOJA.trocas, fretes: LOJA.fretes, instagram: LOJA.instagram, cupom: LOJA.cupom && LOJA.cupom.ativo ? LOJA.cupom : null },
  produtos: PRODUTOS.filter(p => p.foto).map(p => { const id = slug(p.marca + ' ' + p.nome);
    return { id, nome: p.nome, marca: p.marca, cat: p.cat, sub: p.sub || '', preco: p.preco || '', tam: p.tam || [], selo: p.selo || '', desc: p.desc || '',
             foto: site + p.foto, link: site + '#p/' + id }; })
};
fs.writeFileSync(path.join(__dirname, 'produtos.json'), JSON.stringify(out, null, 1));
console.log('produtos.json ok', out.produtos.length, 'produtos');
