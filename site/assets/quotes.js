/* Created by: Claude | Date: 2026-11-03 | Purpose: rotate the Growth thinking quote band | Owner: Syed Hadi */
(function () {
  var Q = [["There is only one valid definition of business purpose: to create a customer.", "Peter Drucker", "The Practice of Management, 1954", "Every GTM plan starts with who buys first and why, before any channel."], ["The essence of strategy is choosing what not to do.", "Michael Porter", "What Is Strategy?, Harvard Business Review, 1996", "Drop the segment you serve worst before you add a new one."], ["Price is what you pay. Value is what you get.", "Warren Buffett", "Berkshire Hathaway shareholder letter, 2008", "Sell the outcome in the buyer's own numbers, then show the price."], ["Show me the incentive and I will show you the outcome.", "Charlie Munger", "Berkshire Hathaway vice chairman", "Partner programs grow when the margin lands with the person who sells."], ["We are stubborn on vision. We are flexible on details.", "Jeff Bezos", "Amazon founder", "Hold the ICP and the promise steady. Test the message every week."], ["The aim of marketing is to make selling superfluous.", "Peter Drucker", "Management: Tasks, Responsibilities, Practices, 1973", "Content should answer the objection before the sales call has to."], ["Supreme excellence consists in breaking the enemy's resistance without fighting.", "Sun Tzu", "The Art of War, Giles translation, 1910", "Own the category so buyers never ask for a bake off."], ["The division of labour is limited by the extent of the market.", "Adam Smith", "The Wealth of Nations, 1776", "Specialise the team only once the market is big enough to feed each role."], ["If you are not embarrassed by the first version of your product, you've launched too late.", "Reid Hoffman", "LinkedIn cofounder", "Launch the pilot offer this month and refine it with real deals."], ["Real artists ship.", "Steve Jobs", "To the Macintosh team, 1983", "A shipped campaign teaches more than a perfect plan in a doc."], ["Only the paranoid survive.", "Andy Grove", "Intel, book of the same name, 1996", "Watch the competitor that is cheaper and good enough, not the loudest one."], ["Chance favors only the prepared mind.", "Louis Pasteur", "Lecture at the University of Lille, 1854", "Research the account before the trigger event, so you are first when it lands."], ["Your most unhappy customers are your greatest source of learning.", "Bill Gates", "Business @ the Speed of Thought, 1999", "Read every lost deal note before you write the next battlecard."], ["A journey of a thousand miles begins with a single step.", "Lao Tzu", "Tao Te Ching, chapter 64", "Book one partner meeting today. Pipeline compounds from there."]], T = 6, MS = 8000;
  function ini(n) { var p = n.split(/\s+/).filter(function (w) { return /^[A-Za-z]/.test(w); }); return ((p[0] || ' ')[0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase(); }
  function init(card) {
    var i = +card.getAttribute('data-i') || 0, timer = null, paused = false, $ = function (s) { return card.querySelector(s); };
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function set(n) {
      i = (n + Q.length) % Q.length; var q = Q[i];
      card.classList.add('qb-out');
      setTimeout(function () {
        $('.qb-q').textContent = '\u201C' + q[0] + '\u201D'; $('.qb-av').textContent = ini(q[1]); $('.qb-who').textContent = q[1]; $('.qb-src').textContent = q[2]; $('.qb-tip').textContent = q[3];
        $('.qb-n').textContent = ('0' + (i + 1)).slice(-2) + '/' + ('0' + Q.length).slice(-2);
        card.className = card.className.replace(/\bqt\d\b/, 'qt' + (i % T + 1));
        card.classList.remove('qb-out'); restartBar();
      }, reduce ? 0 : 260);
    }
    function restartBar() { var b = $('.qb-bar i'); if (!b) return; b.style.animation = 'none'; void b.offsetWidth; b.style.animation = ''; b.style.animationDuration = MS + 'ms'; b.style.animationPlayState = paused ? 'paused' : 'running'; }
    function tick() { clearInterval(timer); timer = setInterval(function () { if (!paused && !document.hidden) set(i + 1); }, MS); }
    function pause(p) { paused = p; var b = $('.qb-bar i'); if (b) b.style.animationPlayState = p ? 'paused' : 'running'; }
    card.addEventListener('mouseenter', function () { pause(true); });
    card.addEventListener('mouseleave', function () { pause(false); });
    card.addEventListener('focusin', function () { pause(true); });
    card.addEventListener('focusout', function () { pause(false); });
    [].forEach.call(card.querySelectorAll('.qb-btn'), function (b) { b.addEventListener('click', function () { set(i + +b.getAttribute('data-d')); tick(); }); });
    var sx = null;
    card.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    card.addEventListener('touchend', function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) { set(i + (dx < 0 ? 1 : -1)); tick(); } sx = null; });
    restartBar(); tick();
  }
  function go() { [].forEach.call(document.querySelectorAll('.qb-card'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
