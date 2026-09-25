/**
 * PWP Python Studio - Interactive Showcase Engine
 * Powers interactive simulators, modal viewers, theme toggling & galleries.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initCopyButtons();
  initLightbox();
  initCodeModal();
  initSimulators();
});

/* ==========================================================================
   Theme Management
   ========================================================================== */
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
  const storedTheme = localStorage.getItem('pwp-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('pwp-theme', next);
      updateThemeIcon(next);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#themeToggle i');
  if (icon) {
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
  }
}

/* ==========================================================================
   Navigation & Smooth Scroll
   ========================================================================== */
function initNavigation() {
  const navLinks = document.querySelectorAll('.nav-item a');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      if (window.pageYOffset >= sectionTop) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });

  // Project Tabs Filtering
  const tabBtns = document.querySelectorAll('.tab-btn');
  const projectCards = document.querySelectorAll('.project-card');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;

      projectCards.forEach(card => {
        if (target === 'all' || card.dataset.project === target) {
          card.style.display = 'grid';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   Copy to Clipboard
   ========================================================================== */
function initCopyButtons() {
  const copyBtns = document.querySelectorAll('.copy-btn');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.dataset.copyText;
      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalIcon = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check" style="color: var(--accent-emerald);"></i>';
        setTimeout(() => {
          btn.innerHTML = originalIcon;
        }, 1800);
      });
    });
  });
}

/* ==========================================================================
   Screenshot Lightbox Modal
   ========================================================================== */
function initLightbox() {
  const backdrop = document.getElementById('lightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const closeBtn = document.getElementById('lightboxClose');

  if (!backdrop) return;

  document.querySelectorAll('.zoomable-shot').forEach(el => {
    el.addEventListener('click', () => {
      const src = el.dataset.fullSrc || el.getAttribute('src');
      const caption = el.dataset.caption || el.getAttribute('alt') || 'Project Screenshot';
      lightboxImg.src = src;
      lightboxCaption.textContent = caption;
      backdrop.classList.add('open');
    });
  });

  const closeModal = () => backdrop.classList.remove('open');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', e => {
    if (e.target === backdrop) closeModal();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && backdrop.classList.contains('open')) {
      closeModal();
    }
  });

  // Thumbnail clicks on project cards
  document.querySelectorAll('.thumb-item').forEach(thumb => {
    thumb.addEventListener('click', function () {
      const card = this.closest('.project-visuals');
      const mainImg = card.querySelector('.main-screenshot-img');
      const mainZoom = card.querySelector('.zoomable-shot');
      const targetSrc = this.dataset.src;
      const targetAlt = this.dataset.caption;

      if (mainImg) {
        mainImg.src = targetSrc;
        mainImg.alt = targetAlt;
      }
      if (mainZoom) {
        mainZoom.dataset.fullSrc = targetSrc;
        mainZoom.dataset.caption = targetAlt;
      }

      card.querySelectorAll('.thumb-item').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
    });
  });
}

/* ==========================================================================
   Code Preview Modal
   ========================================================================== */
const sampleCodeSnippets = {
  calc: `# 01_Smart_Calculator: AST Safe Evaluation
class SafeEvaluator(ast.NodeVisitor):
    ALLOWED_OPERATORS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg,
    }
    ALLOWED_FUNCTIONS = {
        'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
        'tan': math.tan, 'log': math.log10, 'ln': math.log,
        'fact': math.factorial
    }
    def evaluate(self, expression: str) -> float:
        parsed = ast.parse(expression, mode='eval')
        return self.visit(parsed.body)`,

  payroll: `# 02_Employee_Payroll_System: Salary Calculation Formula
def calculate_payroll(basic, ot_hrs, ot_rate, bonus, allowances, tax_pct, ded):
    ot_pay = ot_hrs * ot_rate
    gross_salary = basic + ot_pay + bonus + allowances
    tax_amount = (tax_pct / 100.0) * gross_salary
    total_deductions = tax_amount + ded
    net_salary = gross_salary - total_deductions
    return {
        "ot_pay": ot_pay,
        "gross": gross_salary,
        "tax": tax_amount,
        "deductions": total_deductions,
        "net": net_salary
    }`,

  grade: `# 03_Student_Grade_Analyzer: Grade Calculation & Subject Check
def calculate_result(marks_list):
    total = sum(marks_list)
    percentage = (total / (len(marks_list) * 100)) * 100
    has_failed_subject = any(m < 40 for m in marks_list)

    if has_failed_subject:
        grade = "F"
        status = "FAIL (Below 40 in subject)"
    elif percentage >= 90: grade, status = "A+", "PASS"
    elif percentage >= 80: grade, status = "A", "PASS"
    elif percentage >= 70: grade, status = "B+", "PASS"
    elif percentage >= 60: grade, status = "B", "PASS"
    elif percentage >= 50: grade, status = "C", "PASS"
    elif percentage >= 40: grade, status = "D", "PASS"
    else: grade, status = "F", "FAIL"

    return total, percentage, grade, status`,

  inventory: `# 04_Inventory_Tracker: Stock Evaluation & Low-Stock Alerts
def prepare_item(item_id, name, qty, price, reorder_level):
    stock_value = qty * price
    if qty <= 0:
        status = "OUT OF STOCK"
    elif qty <= reorder_level:
        status = "LOW STOCK"
    else:
        status = "IN STOCK"

    return {
        "id": item_id,
        "name": name,
        "quantity": qty,
        "unit_price": price,
        "stock_value": stock_value,
        "reorder_level": reorder_level,
        "status": status
    }`,

  logs: `# 05_Log_File_Analyzer: Regex Log Line Parser
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2})\\s+'
    r'(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\\s+'
    r'(?P<message>.*)$'
)

def parse_log_line(line: str):
    match = LOG_PATTERN.match(line.strip())
    if match:
        return match.groupdict()
    return None`
};

function initCodeModal() {
  const codeModal = document.getElementById('codeModal');
  const codeContent = document.getElementById('codeModalContent');
  const codeTitle = document.getElementById('codeModalTitle');
  const closeBtn = document.getElementById('codeModalClose');

  if (!codeModal) return;

  document.querySelectorAll('.btn-view-code').forEach(btn => {
    btn.addEventListener('click', () => {
      const codeKey = btn.dataset.code;
      const title = btn.dataset.title || 'Python Source Snippet';
      codeTitle.textContent = title;
      codeContent.textContent = sampleCodeSnippets[codeKey] || '# Code snippet unavailable';
      codeModal.classList.add('open');
    });
  });

  const close = () => codeModal.classList.remove('open');
  if (closeBtn) closeBtn.addEventListener('click', close);
  codeModal.addEventListener('click', e => {
    if (e.target === codeModal) close();
  });
}

/* ==========================================================================
   Interactive Simulators Hub
   ========================================================================== */
function initSimulators() {
  const simNavBtns = document.querySelectorAll('.sim-nav-btn');
  const simPanels = document.querySelectorAll('.sim-panel');

  simNavBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      simNavBtns.forEach(b => b.classList.remove('active'));
      simPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const target = btn.dataset.sim;
      const panel = document.getElementById(`sim-${target}`);
      if (panel) panel.classList.add('active');
    });
  });

  // Buttons in project cards that launch simulator
  document.querySelectorAll('.btn-simulator').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const simTarget = btn.dataset.sim;
      const targetNavBtn = document.querySelector(`.sim-nav-btn[data-sim="${simTarget}"]`);
      if (targetNavBtn) {
        targetNavBtn.click();
        const simSection = document.getElementById('simulators');
        if (simSection) {
          simSection.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  setupCalculatorSim();
  setupPayrollSim();
  setupGradeSim();
  setupInventorySim();
  setupLogSim();
}

/* 1. Calculator Simulator */
function setupCalculatorSim() {
  let currExpr = '0';
  let historyList = [];
  const display = document.getElementById('calcInput');
  const prevDisplay = document.getElementById('calcPrev');
  const historyContainer = document.getElementById('calcHistory');

  function updateDisplay() {
    if (display) display.textContent = currExpr;
  }

  document.querySelectorAll('.calc-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.dataset.val;
      const action = btn.dataset.action;

      if (action === 'clear') {
        currExpr = '0';
        if (prevDisplay) prevDisplay.textContent = '';
      } else if (action === 'backspace') {
        currExpr = currExpr.length > 1 ? currExpr.slice(0, -1) : '0';
      } else if (action === 'equals') {
        try {
          // Normalize expression for safe js eval
          let sanitized = currExpr
            .replace(/×/g, '*')
            .replace(/÷/g, '/')
            .replace(/π/g, 'Math.PI')
            .replace(/e/g, 'Math.E')
            .replace(/sqrt\(/g, 'Math.sqrt(')
            .replace(/sin\(/g, 'Math.sin(')
            .replace(/cos\(/g, 'Math.cos(')
            .replace(/tan\(/g, 'Math.tan(')
            .replace(/log\(/g, 'Math.log10(')
            .replace(/ln\(/g, 'Math.log(');

          // Handle percentage
          sanitized = sanitized.replace(/(\d+(?:\.\d+)?)%/g, '($1/100)');

          const result = Function(`'use strict'; return (${sanitized})`)();
          const formattedRes = Number.isInteger(result) ? result : Number(result.toFixed(6));

          if (prevDisplay) prevDisplay.textContent = `${currExpr} =`;
          historyList.unshift(`${currExpr} = ${formattedRes}`);
          if (historyList.length > 5) historyList.pop();

          if (historyContainer) {
            historyContainer.innerHTML = historyList.map(item => `
              <div class="calc-hist-item" onclick="document.getElementById('calcInput').textContent = '${item.split('=')[1].trim()}';">
                <span>${item.split('=')[0]}</span>
                <strong>= ${item.split('=')[1]}</strong>
              </div>
            `).join('');
          }

          currExpr = String(formattedRes);
        } catch (err) {
          currExpr = 'Error';
          setTimeout(() => { currExpr = '0'; updateDisplay(); }, 1500);
        }
      } else if (val) {
        if (currExpr === '0' && !isNaN(val) && val !== '.') {
          currExpr = val;
        } else {
          currExpr += val;
        }
      }
      updateDisplay();
    });
  });
}

/* 2. Payroll Simulator */
function setupPayrollSim() {
  const form = document.getElementById('payrollForm');
  if (!form) return;

  function calculate() {
    const basic = parseFloat(document.getElementById('payBasic').value) || 0;
    const otHrs = parseFloat(document.getElementById('payOtHrs').value) || 0;
    const otRate = parseFloat(document.getElementById('payOtRate').value) || 0;
    const allowances = parseFloat(document.getElementById('payAllowances').value) || 0;
    const bonus = parseFloat(document.getElementById('payBonus').value) || 0;
    const taxPct = parseFloat(document.getElementById('payTaxPct').value) || 0;
    const ded = parseFloat(document.getElementById('payDeductions').value) || 0;

    const otPay = otHrs * otRate;
    const gross = basic + otPay + allowances + bonus;
    const taxVal = (taxPct / 100) * gross;
    const totalDed = taxVal + ded;
    const net = gross - totalDed;

    document.getElementById('resPayGross').textContent = `₹${gross.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById('resPayOt').textContent = `₹${otPay.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById('resPayTax').textContent = `₹${taxVal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById('resPayDeductions').textContent = `₹${totalDed.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById('resPayNet').textContent = `₹${net.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  }

  form.querySelectorAll('input').forEach(inp => {
    inp.addEventListener('input', calculate);
  });
  calculate();
}

/* 3. Student Grade Simulator */
function setupGradeSim() {
  const inputs = [
    document.getElementById('gradeS1'),
    document.getElementById('gradeS2'),
    document.getElementById('gradeS3'),
    document.getElementById('gradeS4'),
    document.getElementById('gradeS5')
  ];

  function evaluateGrades() {
    const marks = inputs.map(i => parseFloat(i ? i.value : 0) || 0);
    const total = marks.reduce((a, b) => a + b, 0);
    const pct = (total / 500) * 100;
    const hasFail = marks.some(m => m < 40);

    let grade = 'F';
    let statusText = hasFail ? 'FAIL (Subject < 40)' : 'PASS';
    let statusClass = hasFail ? 'fail' : 'pass';

    if (!hasFail) {
      if (pct >= 90) grade = 'A+';
      else if (pct >= 80) grade = 'A';
      else if (pct >= 70) grade = 'B+';
      else if (pct >= 60) grade = 'B';
      else if (pct >= 50) grade = 'C';
      else if (pct >= 40) grade = 'D';
      else {
        grade = 'F';
        statusText = 'FAIL';
        statusClass = 'fail';
      }
    }

    const maxMark = Math.max(...marks);
    const minMark = Math.min(...marks);
    const highSub = `Subject ${marks.indexOf(maxMark) + 1} (${maxMark})`;
    const lowSub = `Subject ${marks.indexOf(minMark) + 1} (${minMark})`;

    const gradeBadge = document.getElementById('resGradeBadge');
    const statusPill = document.getElementById('resGradeStatus');
    const totalEl = document.getElementById('resGradeTotal');
    const pctEl = document.getElementById('resGradePct');
    const highEl = document.getElementById('resGradeHigh');
    const lowEl = document.getElementById('resGradeLow');

    if (gradeBadge) gradeBadge.textContent = grade;
    if (statusPill) {
      statusPill.textContent = statusText;
      statusPill.className = `grade-status-pill ${statusClass}`;
    }
    if (totalEl) totalEl.textContent = `${total} / 500`;
    if (pctEl) pctEl.textContent = `${pct.toFixed(2)}%`;
    if (highEl) highEl.textContent = highSub;
    if (lowEl) lowEl.textContent = lowSub;
  }

  inputs.forEach(i => {
    if (i) i.addEventListener('input', evaluateGrades);
  });
  evaluateGrades();
}

/* 4. Inventory Tracker Simulator */
function setupInventorySim() {
  let inventory = [
    { id: 'ITM-101', name: 'Logitech MX Master 3S', cat: 'Peripherals', qty: 14, price: 8499, reorder: 5 },
    { id: 'ITM-102', name: 'Mechanical Keychron K2', cat: 'Keyboards', qty: 3, price: 6999, reorder: 5 },
    { id: 'ITM-103', name: 'Dell UltraSharp 27" 4K', cat: 'Monitors', qty: 8, price: 34500, reorder: 3 },
    { id: 'ITM-104', name: 'USB-C Anker Fast Cable', cat: 'Accessories', qty: 0, price: 799, reorder: 10 },
    { id: 'ITM-105', name: 'SanDisk 1TB NVMe SSD', cat: 'Storage', qty: 19, price: 6200, reorder: 4 },
  ];

  const tbody = document.getElementById('inventoryTableBody');
  const searchInput = document.getElementById('invSearch');
  const addBtn = document.getElementById('invAddBtn');

  function renderTable(items) {
    if (!tbody) return;
    tbody.innerHTML = items.map(item => {
      const val = item.qty * item.price;
      let status = 'in-stock';
      let statusLabel = 'IN STOCK';
      if (item.qty === 0) {
        status = 'out-of-stock';
        statusLabel = 'OUT OF STOCK';
      } else if (item.qty <= item.reorder) {
        status = 'low-stock';
        statusLabel = 'LOW STOCK';
      }

      return `
        <tr>
          <td><strong>${item.id}</strong></td>
          <td>${item.name}</td>
          <td>${item.cat}</td>
          <td>${item.qty}</td>
          <td>₹${item.price.toLocaleString('en-IN')}</td>
          <td><strong>₹${val.toLocaleString('en-IN')}</strong></td>
          <td><span class="status-tag ${status}">${statusLabel}</span></td>
        </tr>
      `;
    }).join('');

    const totalVal = items.reduce((acc, curr) => acc + (curr.qty * curr.price), 0);
    const totalItems = items.length;
    const lowStockCount = items.filter(i => i.qty <= i.reorder).length;

    const valEl = document.getElementById('invTotalVal');
    const itemsEl = document.getElementById('invTotalItems');
    const alertEl = document.getElementById('invAlerts');

    if (valEl) valEl.textContent = `₹${totalVal.toLocaleString('en-IN')}`;
    if (itemsEl) itemsEl.textContent = totalItems;
    if (alertEl) alertEl.textContent = lowStockCount;
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      const filtered = inventory.filter(i => 
        i.name.toLowerCase().includes(query) ||
        i.id.toLowerCase().includes(query) ||
        i.cat.toLowerCase().includes(query)
      );
      renderTable(filtered);
    });
  }

  if (addBtn) {
    addBtn.addEventListener('click', () => {
      const name = prompt('Enter Item Name:');
      if (!name) return;
      const cat = prompt('Enter Category:', 'Electronics') || 'General';
      const qty = parseInt(prompt('Enter Stock Quantity:', '10'), 10) || 1;
      const price = parseFloat(prompt('Enter Unit Price (₹):', '1500')) || 100;
      const reorder = parseInt(prompt('Enter Reorder Level:', '5'), 10) || 5;
      const newId = `ITM-${100 + inventory.length + 1}`;

      inventory.push({ id: newId, name, cat, qty, price, reorder });
      renderTable(inventory);
    });
  }

  renderTable(inventory);
}

/* 5. Log File Analyzer Simulator */
function setupLogSim() {
  const sampleLogs = [
    { time: '2026-09-25 10:14:02', level: 'INFO', msg: 'System worker initialized on pid 4190' },
    { time: '2026-09-25 10:14:15', level: 'INFO', msg: 'API gateway connected to upstream cluster' },
    { time: '2026-09-25 10:15:30', level: 'WARNING', msg: 'Memory utilization exceeded 78% threshold' },
    { time: '2026-09-25 10:16:02', level: 'INFO', msg: 'User session authentication successful [UID: 92500116005]' },
    { time: '2026-09-25 10:17:05', level: 'ERROR', msg: 'Database connection timeout on pool replica-02' },
    { time: '2026-09-25 10:17:12', level: 'ERROR', msg: 'Query failed: SELECT * FROM transactions WHERE status = pending' },
    { time: '2026-09-25 10:18:40', level: 'CRITICAL', msg: 'Storage disk volume /data/analytics reached 98% capacity' },
    { time: '2026-09-25 10:19:01', level: 'INFO', msg: 'Automated garbage collection completed in 42ms' },
    { time: '2026-09-25 10:20:18', level: 'WARNING', msg: 'API rate limit threshold warning for client 192.168.1.104' },
    { time: '2026-09-25 10:21:45', level: 'ERROR', msg: 'SSL Handshake failure during webhook dispatch' }
  ];

  const logConsole = document.getElementById('logConsole');
  const levelFilter = document.getElementById('logLevelFilter');
  const searchInput = document.getElementById('logSearch');

  function renderLogs() {
    if (!logConsole) return;
    const selectedLevel = levelFilter ? levelFilter.value : 'ALL';
    const query = searchInput ? searchInput.value.toLowerCase() : '';

    const filtered = sampleLogs.filter(l => {
      const matchLevel = selectedLevel === 'ALL' || l.level === selectedLevel;
      const matchQuery = !query || l.msg.toLowerCase().includes(query) || l.time.includes(query);
      return matchLevel && matchQuery;
    });

    logConsole.innerHTML = filtered.map(l => `
      <div class="log-entry level-${l.level}">
        <span style="opacity: 0.65;">[${l.time}]</span>
        <strong>[${l.level}]</strong>
        <span>${l.msg}</span>
      </div>
    `).join('');

    const total = sampleLogs.length;
    const errors = sampleLogs.filter(l => l.level === 'ERROR' || l.level === 'CRITICAL').length;
    const errorPct = ((errors / total) * 100).toFixed(1);

    const totalEl = document.getElementById('logStatTotal');
    const errEl = document.getElementById('logStatErrors');
    const rateEl = document.getElementById('logStatRate');

    if (totalEl) totalEl.textContent = total;
    if (errEl) errEl.textContent = errors;
    if (rateEl) rateEl.textContent = `${errorPct}%`;
  }

  if (levelFilter) levelFilter.addEventListener('change', renderLogs);
  if (searchInput) searchInput.addEventListener('input', renderLogs);
  renderLogs();
}
