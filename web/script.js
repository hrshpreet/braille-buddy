// Path to your JSON file
const jsonFilePath = '../progress.json';

// Fetch and process the JSON data
fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
        const keys = document.querySelectorAll('.key');
        const { learnt_dict, tested_dict, mistake_dict } = data;

        // Determine the letter with the most mistakes
        const maxMistakes = Math.max(...Object.values(mistake_dict));
        const mostMistakesLetter = Object.keys(mistake_dict).find(
            letter => mistake_dict[letter] === maxMistakes && maxMistakes > 0
        );

        keys.forEach(key => {
            const letter = key.textContent.toLowerCase();

            // Apply colors based on the conditions
            if (learnt_dict[letter]) {
                if (tested_dict[letter]) {
                    key.style.backgroundColor = 'lightgreen'; // Learnt and tested
                } else {
                    key.style.backgroundColor = 'lime';
                }
            }
            if (letter === mostMistakesLetter) {
                key.style.backgroundColor = 'red'; // Most mistakes and mistakes > 0
            }
        });
    })
    .catch(error => console.error('Error loading JSON:', error));



fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
        const learntDict = data.learnt_dict;
        const mistakeDict = data.mistake_dict;
        const testedDict = data.tested_dict;

        const lettersLearnt = Object.values(learntDict).filter(value => value).length;
        const lettersTested = Object.values(testedDict).filter(value => value).length;
        const totalMistakes = Object.values(mistakeDict).reduce((sum, val) => sum + val, 0);

        document.getElementById('letters-learnt').textContent = lettersLearnt;
        document.getElementById('letters-tested').textContent = lettersTested;
        document.getElementById('total-mistakes').textContent = totalMistakes;
    })
    .catch(error => console.error('Error loading JSON:', error));




// Summary Section


fetch(jsonFilePath)
  .then(response => response.json())
  .then(data => {
    const learntDict = data.learnt_dict;
    const mistakeDict = data.mistake_dict;
    const testedDict = data.tested_dict;

    let maxMistakes = 0;
    let mostMistakes = 'N/A';
    let mostTested = 'N/A';
    let maxTests = 0;
    let totalPracticed = 0;
    const latestLearnt = [];
    const strongLetters = [];

    Object.keys(learntDict).forEach(letter => {
      if (mistakeDict[letter] > maxMistakes) {
        maxMistakes = mistakeDict[letter];
        mostMistakes = letter;
      }

      if (testedDict[letter] > maxTests) {
        maxTests = testedDict[letter];
        mostTested = letter;
      }

      if (testedDict[letter]) totalPracticed++;

      if (learntDict[letter]) {
        latestLearnt.push(letter);
        if (mistakeDict[letter] === 0) {
          strongLetters.push(letter);
        }
      }
    });

    // Sort and limit latest learnt to top 3
    latestLearnt.sort().reverse();
    const latestLearntTop3 = latestLearnt.slice(0, 3);

    // Update summary section
    document.getElementById('most-mistakes').textContent = mostMistakes;
    document.getElementById('latest-learnt').textContent = latestLearntTop3.join(', ') || 'N/A';
    document.getElementById('most-tested').textContent = mostTested;
    document.getElementById('total-practiced').textContent = totalPracticed;
    document.getElementById('strong-letters').textContent = strongLetters.join(', ') || 'N/A';
  })
  .catch(error => console.error('Error loading JSON:', error));






// Detailed Report


fetch(jsonFilePath)
  .then(response => response.json())
  .then(data => {
    const tableBody = document.querySelector('#progress-table tbody');
    const learntDict = data.learnt_dict;
    const mistakeDict = data.mistake_dict;
    const testedDict = data.tested_dict;

    let maxMistakes = 0;
    let weakLetter = 'N/A';

    Object.keys(learntDict).forEach(letter => {
      const row = document.createElement('tr');

      // Calculate the weak area
      if (mistakeDict[letter] > maxMistakes) {
        maxMistakes = mistakeDict[letter];
        weakLetter = letter;
      }

      // Create table cells
      row.innerHTML = `
        <td>${letter}</td>
        <td>${learntDict[letter] ? 'Yes' : 'No'}</td>
        <td>${testedDict[letter] ? 'Yes' : 'No'}</td>
        <td>${mistakeDict[letter]}</td>
      `;

      // Highlight weak areas if mistakes >= 3
      if (mistakeDict[letter] >= 3) {
        row.classList.add('highlight');
      }

      // Append the row
      tableBody.appendChild(row);
    });

    // Update the weak letter suggestion
    document.getElementById('weak-letter').textContent = maxMistakes >= 3 ? weakLetter : 'N/A';
  })
  .catch(error => console.error('Error loading JSON:', error));




// Sort table by column
function sortTable(columnIndex) {
    const table = document.getElementById('progress-table');
    const rows = Array.from(table.rows).slice(1); // Exclude header row
    const isNumeric = columnIndex === 3; // Sort mistakes numerically
    const isAscending = table.dataset.sortedColumn === String(columnIndex) 
      ? table.dataset.sorted !== 'asc' // Toggle sort order
      : true; // Default to ascending for a new column
  
    rows.sort((a, b) => {
      const valA = isNumeric ? parseInt(a.cells[columnIndex].innerText) || 0 : a.cells[columnIndex].innerText.toLowerCase();
      const valB = isNumeric ? parseInt(b.cells[columnIndex].innerText) || 0 : b.cells[columnIndex].innerText.toLowerCase();
  
      if (valA > valB) return isAscending ? 1 : -1;
      if (valA < valB) return isAscending ? -1 : 1;
      return 0;
    });
  
    // Append sorted rows back to the table
    rows.forEach(row => table.tBodies[0].appendChild(row));
  
    // Update sort state
    table.dataset.sorted = isAscending ? 'asc' : 'desc';
    table.dataset.sortedColumn = columnIndex;
  }
  