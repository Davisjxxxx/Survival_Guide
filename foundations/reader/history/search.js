const query = document.querySelector('#lookup');
const status = document.querySelector('#matches');
function filterPages() {
  const terms = query.value.trim().toLowerCase().split(/\s+/);
  let count = 0;
  for (const section of document.querySelectorAll('.catalog section')) {
    let visible = 0;
    for (const item of section.querySelectorAll('li')) {
      item.hidden = !terms.every(term => item.dataset.index.includes(term));
      if (!item.hidden) visible++;
    }
    section.hidden = visible === 0;
    count += visible;
  }
  status.textContent = count ? count + (count === 1 ? ' page' : ' pages') : 'No matching pages. Try another word.';
}
query.addEventListener('input', filterPages);
window.addEventListener('pageshow', filterPages);
