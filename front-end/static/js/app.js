document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search');
  const playersSelect = document.getElementById('filter-players');
  const grid = document.getElementById('games-grid');
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.card'));

  function normalize(s){
    return (s||'').toString().trim().toLowerCase();
  }

  function matchesPlayers(cardPlayers, filterValue){
    if (!filterValue) return true;
    const p = normalize(cardPlayers);
    if (filterValue === '4+') return p.includes('4') || p.includes('+') || parseInt(p) >= 4;
    if (filterValue === '1-2') return p.includes('1') || p.includes('2') || /1|2/.test(p);
    if (filterValue === '2-4') return /2|3|4/.test(p);
    return true;
  }

  function applyFilters(){
    const q = normalize(searchInput?.value);
    const f = playersSelect?.value;
    let visible = 0;
    cards.forEach(c=>{
      const title = c.dataset.title || '';
      const players = c.dataset.players || '';
      const okText = !q || title.includes(q);
      const okPlayers = matchesPlayers(players, f);
      if (okText && okPlayers){
        c.style.display = '';
        visible++;
      } else {
        c.style.display = 'none';
      }
    });
    let no = document.getElementById('no-results');
    if (visible === 0){
      if (!no){
        no = document.createElement('p');
        no.id = 'no-results';
        no.textContent = 'Brak wyników.';
        grid.parentNode.appendChild(no);
      }
    } else if (no){
      no.remove();
    }
  }

  searchInput?.addEventListener('input', applyFilters);
  playersSelect?.addEventListener('change', applyFilters);
});